"""Builds the DDS textures + animation key tables for the Living Lands Skyrim SE main-menu mod.

Same timeline as the 30 s video (loop):
  0-5 s lit & flickering | 5-5.9 flame dies | 5.3-9.5 candle light -> moonlight
  9.5-20 s moonlit table | 20-24.2 candle relights itself | 24.2-30 lit & flickering
"""
import cv2, numpy as np, math, struct, os, sys

SRC1 = sys.argv[1]; SRC2 = sys.argv[2]; OUT = sys.argv[3]
os.makedirs(OUT, exist_ok=True)
W, H = 1920, 1080
TEX_W, TEX_H = 2048, 1024        # the menu plane maps UV 0..1 to a 16:9 area (squashed 2:1 texture)
T = 30.0


def load(path):
    a = cv2.imread(path); h, w = a.shape[:2]
    cw = int(round(h * 16 / 9)); x0 = (w - cw) // 2
    return cv2.resize(a[:, x0:x0 + cw], (W, H), interpolation=cv2.INTER_LANCZOS4)


img1, img2 = load(SRC1), load(SRC2)

# --- flameless candle-lit base + flame light layer (diff) -------------------
mask = np.zeros((H, W), np.uint8)
y0, y1, x0, x1 = 10, 150, 1520, 1720
mask[y0:y1, x0:x1] = (img1[y0:y1, x0:x1, 0] > 165).astype(np.uint8) * 255
mask = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 13)))
base1 = cv2.inpaint(img1, mask, 6, cv2.INPAINT_TELEA)
soft = cv2.GaussianBlur(mask, (0, 0), 2.5).astype(np.float32)[..., None] / 255
base1 = (base1 * soft + img1 * (1 - soft)).astype(np.float32)
diff = img1.astype(np.float32) - base1

# --- align both images to a shared in-between geometry (removes double contours when cross-fading)
def prep(im):
    g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY).astype(np.float32)
    g = cv2.GaussianBlur(g, (0, 0), 1.2)
    mu = cv2.GaussianBlur(g, (0, 0), 12)
    sd = np.sqrt(cv2.GaussianBlur((g - mu) ** 2, (0, 0), 12)) + 4
    return np.clip((g - mu) / sd * 40 + 128, 0, 255).astype(np.uint8)

dis = cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM)
dis.setPatchSize(16); dis.setPatchStride(4); dis.setVariationalRefinementIterations(10)
p1, p2 = prep(img1), prep(img2)
F12 = cv2.GaussianBlur(dis.calc(p1, p2, None), (0, 0), 3)
F21 = cv2.GaussianBlur(dis.calc(p2, p1, None), (0, 0), 3)
GX, GY = np.meshgrid(np.arange(W, dtype=np.float32), np.arange(H, dtype=np.float32))
def warp(im, F, s):
    return cv2.remap(im.astype(np.float32), GX - s * F[..., 0], GY - s * F[..., 1], cv2.INTER_CUBIC,
                     borderMode=cv2.BORDER_REFLECT)

moon = warp(img2, F21, 0.5)
warm_nf = warp(base1, F12, 0.5)             # candle-lit, flame removed
warm_full = warp(img1, F12, 0.5)            # candle-lit with flame (static fallback)

# --- DDS writer (uncompressed BGRA8 + mip chain) -----------------------------
def write_dds(path, bgra):
    h, w = bgra.shape[:2]
    mips = [bgra]
    while mips[-1].shape[0] > 1 or mips[-1].shape[1] > 1:
        m = mips[-1]
        nw, nh = max(1, m.shape[1] // 2), max(1, m.shape[0] // 2)
        mips.append(cv2.resize(m, (nw, nh), interpolation=cv2.INTER_AREA))
    hdr = struct.pack('<4sI', b'DDS ', 124)
    hdr += struct.pack('<IIIII', 0x2100F | 0x0, h, w, w * 4, 0)
    hdr += struct.pack('<I', len(mips)) + b'\0' * 44
    hdr += struct.pack('<II4sIIIII', 32, 0x41, b'\0\0\0\0', 32, 0x00FF0000, 0x0000FF00, 0x000000FF, 0xFF000000)
    hdr += struct.pack('<IIIII', 0x401008, 0, 0, 0, 0)
    with open(path, 'wb') as f:
        f.write(hdr)
        for m in mips:
            f.write(np.ascontiguousarray(m).astype(np.uint8).tobytes())

def to_tex(im, w=TEX_W, h=TEX_H):
    im = cv2.resize(np.clip(im, 0, 255).astype(np.uint8), (w, h), interpolation=cv2.INTER_AREA if w < im.shape[1] else cv2.INTER_LANCZOS4)
    return np.dstack([im, np.full((h, w), 255, np.uint8)])

write_dds(f'{OUT}/llm_moon.dds', to_tex(moon))
write_dds(f'{OUT}/llm_warm.dds', to_tex(warm_nf))
write_dds(f'{OUT}/llm_warm_flame.dds', to_tex(warm_full))

# flame sprite (additive light), window around the wick
FX0, FY0, FS = 1560, 10, 128
win = np.clip(diff[FY0:FY0 + FS, FX0:FX0 + FS], 0, 255)
win = cv2.resize(win, (256, 256), interpolation=cv2.INTER_CUBIC)
write_dds(f'{OUT}/llm_flame.dds', np.dstack([np.clip(win, 0, 255).astype(np.uint8), np.full((256, 256), 255, np.uint8)]))
cv2.imwrite(f'{OUT}/preview_moon.png', to_tex(moon)[..., :3]); cv2.imwrite(f'{OUT}/preview_warm.png', to_tex(warm_nf)[..., :3])
cv2.imwrite(f'{OUT}/preview_flame.png', win.astype(np.uint8))

# --- animation key tables ----------------------------------------------------
def smooth(x):
    x = min(max(x, 0.0), 1.0); return x * x * (3 - 2 * x)
rng = np.random.RandomState(7)
KS = [15, 24, 39, 57, 81, 114, 159]
PH = rng.uniform(0, 2 * math.pi, (4, len(KS)))
AM = np.array([1.0, 0.8, 0.6, 0.5, 0.35, 0.25, 0.15])
def noise(ch, t):
    return sum(a * math.sin(2 * math.pi * k * t / T + p) for a, k, p in zip(AM, KS, PH[ch])) / AM.sum() * 1.6

T_DIE, T_MORPH, T_MOON, T_IGN = 5.0, 5.3, 9.5, 20.0
def warm_alpha(t):
    if t < T_MORPH: return 1.0
    if t < T_IGN: return 1.0 - smooth((t - T_MORPH) / (T_MOON - T_MORPH))
    return smooth((t - T_IGN - 0.3) / 3.6)

def flame_state(t):
    """returns (scale, theta_img_deg)"""
    th = 5.0 * noise(0, t); n1 = noise(1, t)
    if t < T_DIE:
        f = 1.0; lean = 0.0
    elif t < T_IGN:
        f = 1 - smooth((t - T_DIE) / 0.9)
        gust = math.sin(math.pi * min(1, (t - T_DIE) / 0.9))
        lean = -22 * gust
        f = f * (1 + 0.35 * math.sin(2 * math.pi * 11 * t) * gust) if f > 0 else 0.0
    else:
        f = smooth((t - T_IGN) / 1.8) ** 1.4
        flut = 1 + 0.25 * math.sin(2 * math.pi * 9 * t) * (1 - f)
        f = 1.0 if t >= T_IGN + 1.8 else min(1.0, f * flut); lean = 0.0
    s = (f ** 0.8) * (1 + 0.10 * n1)
    return max(s, 0.001), th + lean

with open(f'{OUT}/keys.txt', 'w') as k:
    k.write(f'{T}\n')
    N = int(T * 10)
    k.write(f'alpha {N}\n')                                  # warm-layer alpha, 10 Hz
    for i in range(N + 1):
        t = i / 10; k.write(f'{t:.4f} {warm_alpha(min(t, T)):.5f}\n')
    N = int(T * 20)
    k.write(f'flame {N}\n')                                  # flame scale + lean, 20 Hz
    for i in range(N + 1):
        t = i / 20; s, th = flame_state(t % T)
        k.write(f'{t:.4f} {s:.5f} {th:.4f}\n')
    # loop closure: last key == first key
# pivot (wick root) and window, normalised image coordinates, for the NIF builder
with open(f'{OUT}/layout.txt', 'w') as f:
    f.write(f'{1606/W} {86/H} {FX0/W} {FY0/H} {(FX0+FS)/W} {(FY0+FS)/H}\n')
print('assets ok')
