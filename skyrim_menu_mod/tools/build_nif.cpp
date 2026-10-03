// Builds the Living Lands main-menu NIF (Skyrim SE) from the reference logo.nif
// usage: build_nif <static|anim|animflip> in.nif out.nif keys.txt layout.txt texdir
#include "NifFile.hpp"
#include <cmath>
#include <fstream>
#include <iostream>
#include <set>
using namespace nifly;

struct Keys {
	float T = 30;
	std::vector<std::pair<float, float>> alpha;
	std::vector<std::array<float, 3>> flame;
};

static Keys readKeys(const std::string& path) {
	Keys k;
	std::ifstream f(path);
	f >> k.T;
	std::string tag; int n;
	while (f >> tag >> n) {
		for (int i = 0; i <= n; i++) {
			if (tag == "alpha") { float t, a; f >> t >> a; k.alpha.push_back({t, a}); }
			else { float t, s, th; f >> t >> s >> th; k.flame.push_back({t, s, th}); }
		}
	}
	return k;
}

int main(int argc, char** argv) {
	if (argc < 7) { std::cerr << "args\n"; return 2; }
	std::string mode = argv[1];
	NifFile nif;
	if (nif.Load(argv[2])) { std::cerr << "load failed\n"; return 1; }
	Keys keys = readKeys(argv[4]);
	float lay[6]; { std::ifstream f(argv[5]); for (float& v : lay) f >> v; }
	std::string texdir = argv[6];                // e.g. textures\\livinglands
	auto& hdr = nif.GetHeader();
	NiNode* root = nif.GetRootNode();

	NiShape* plane = nif.FindBlockByName<NiShape>("CasSmRmMid01:9");
	NiShape* cyl = nif.FindBlockByName<NiShape>("Cylinder01");
	if (!plane || !cyl) { std::cerr << "template shapes missing\n"; return 1; }

	std::set<NiObject*> keep;      // children of root that survive
	keep.insert(plane);

	// plane geometry (local coords + uv) -> mapping uv -> local xy
	std::vector<Vector3> pv; std::vector<Vector2> puv;
	nif.GetVertsForShape(plane, pv); nif.GetUvsForShape(plane, puv);
	float uMin = 1e9, uMax = -1e9, vMin = 1e9, vMax = -1e9, xMin = 1e9, xMax = -1e9, yMin = 1e9, yMax = -1e9;
	for (size_t i = 0; i < pv.size(); i++) {
		uMin = std::min(uMin, puv[i].u); uMax = std::max(uMax, puv[i].u);
		vMin = std::min(vMin, puv[i].v); vMax = std::max(vMax, puv[i].v);
		xMin = std::min(xMin, pv[i].x); xMax = std::max(xMax, pv[i].x);
		yMin = std::min(yMin, pv[i].y); yMax = std::max(yMax, pv[i].y);
	}
	// u grows with +x ; v grows toward -y (image top = +y)
	auto lx = [&](float u) { return xMin + (u - uMin) / (uMax - uMin) * (xMax - xMin); };
	auto ly = [&](float v) { return yMax - (v - vMin) / (vMax - vMin) * (yMax - yMin); };
	float planeZ = pv[0].z;

	if (mode == "static") {
		std::string t = texdir + "\\llm_warm_flame.dds";
		nif.SetTextureSlot(plane, t, 0);
	}
	else {
		float dir = (mode == "animflip") ? -1.0f : 1.0f;
		// ---- templates (effect shader + additive alpha from the vanilla flame)
		auto* effTmpl = hdr.GetBlock<BSEffectShaderProperty>(*cyl->ShaderPropertyRef());
		auto* addTmpl = hdr.GetBlock<NiAlphaProperty>(*cyl->AlphaPropertyRef());
		if (!effTmpl || !addTmpl) { std::cerr << "effect template missing\n"; return 1; }

		auto newShader = [&](const std::string& tex) -> BSEffectShaderProperty* {
			auto s = effTmpl->Clone();
			auto* sh = dynamic_cast<BSEffectShaderProperty*>(s.get());
			sh->sourceTexture.get() = tex;
			sh->textureClampMode = 0;   // clamp/clamp + lighting influence 0 (unlit, shows the texture as-is)
			sh->baseColor = Color4(1.0f, 1.0f, 1.0f, 1.0f);
			sh->baseColorScale = 1.0f;
			sh->softFalloffDepth = 0.0f;
			sh->controllerRef.Clear();
			sh->extraDataRefs = NiBlockRefArray<NiExtraData>();
			hdr.AddBlock(std::move(s));
			return sh;
		};
		auto newAlpha = [&](uint16_t flags, uint8_t thr) -> uint32_t {
			auto a = std::make_unique<NiAlphaProperty>();
			a->flags = flags; a->threshold = thr;
			return hdr.AddBlock(std::move(a));
		};
		auto floatCtrl = [&](BSEffectShaderProperty* sh, const std::vector<std::pair<float, float>>& ks, uint32_t var) {
			auto d = std::make_unique<NiFloatData>();
			d->data.SetInterpolationType(LINEAR_KEY);
			for (auto& kv : ks) { NiAnimationKey<float> k; k.type = LINEAR_KEY; k.time = kv.first; k.value = kv.second; d->data.AddKey(k); }
			uint32_t idD = hdr.AddBlock(std::move(d));
			auto it = std::make_unique<NiFloatInterpolator>();
			it->floatValue = ks.front().second; it->dataRef.index = idD;
			uint32_t idI = hdr.AddBlock(std::move(it));
			auto c = std::make_unique<BSEffectShaderPropertyFloatController>();
			c->flags = 0x48; c->frequency = 1.0f; c->phase = 0.0f; c->startTime = 0.0f; c->stopTime = keys.T;
			c->typeOfControlledVariable = var;
			c->targetRef.index = hdr.GetBlockID(sh);
			c->interpolatorRef.index = idI;
			sh->controllerRef.index = hdr.AddBlock(std::move(c));
		};

		// ---- layer 0: moonlit table (re-uses the original plane, opaque effect shader)
		{
			auto* sh = newShader(texdir + "\\llm_moon.dds");
			*plane->ShaderPropertyRef() = NiBlockRef<NiShader>(hdr.GetBlockID(sh));
			plane->AlphaPropertyRef()->Clear();
		}
		// ---- layer 1: candle-lit table (flame removed), alpha animated
		NiShape* warm = nif.CloneShape(plane, "LL_Warm");
		{
			auto* sh = newShader(texdir + "\\llm_warm.dds");
			*warm->ShaderPropertyRef() = NiBlockRef<NiShader>(hdr.GetBlockID(sh));
			*warm->AlphaPropertyRef() = NiBlockRef<NiAlphaProperty>(newAlpha(0x00ED, 0));
			std::vector<Vector3> v = pv; for (auto& p : v) p.z = planeZ + 0.5f * dir;
			nif.SetVertsForShape(warm, v);
			floatCtrl(sh, keys.alpha, 5);
			keep.insert(warm);
		}
		// ---- layer 2: flame sprite, additive, scaled/leaned by a transform controller
		{
			float px = lay[0], py = lay[1], u0 = lay[2], v0 = lay[3], u1 = lay[4], v1 = lay[5];
			float pivX = lx(px), pivY = ly(py);
			// pose node (plane transform at the pivot) -> wiggle node (animated, identity base)
			MatTransform pose = plane->transform;
			Vector3 off = pose.rotation * Vector3(pivX, pivY, 0.0f);
			pose.translation = pose.translation + off * pose.scale;
			NiNode* posen = nif.AddNode("LL_FlamePose", pose, root);
			MatTransform id;
			NiNode* wig = nif.AddNode("LL_Flame", id, posen);
			keep.insert(posen);

			NiShape* fl = nif.CloneShape(plane, "LL_FlameSprite");
			// CloneShape put it under the plane's parent (root) -> move it under the wiggle node
			nif.SetParentNode(fl, wig);
			fl->transform = MatTransform();
			auto* sh = newShader(texdir + "\\llm_flame.dds");
			*fl->ShaderPropertyRef() = NiBlockRef<NiShader>(hdr.GetBlockID(sh));
			*fl->AlphaPropertyRef() = NiBlockRef<NiAlphaProperty>(newAlpha(addTmpl->flags, addTmpl->threshold));
			float xa = lx(u0) - pivX, xb = lx(u1) - pivX, ya = ly(v0) - pivY, yb = ly(v1) - pivY, z = planeZ + 1.0f * dir;
			std::vector<Vector3> v = {Vector3(xb, ya, z), Vector3(xa, ya, z), Vector3(xa, yb, z), Vector3(xb, yb, z)};
			std::vector<Vector2> uv = {Vector2(1, 0), Vector2(0, 0), Vector2(0, 1), Vector2(1, 1)};
			nif.SetVertsForShape(fl, v); nif.SetUvsForShape(fl, uv);
			fl->SetBounds(BoundingSphere(Vector3(0, 0, z), 30.0f));

			// transform controller on the wiggle node: lean (rot about plane normal) + uniform scale
			auto td = std::make_unique<NiTransformData>();
			td->rotationType = LINEAR_KEY;
			td->scales.SetInterpolationType(LINEAR_KEY);
			for (auto& k : keys.flame) {
				float th = -k[2] * 3.14159265f / 180.0f;     // image-clockwise -> local counter-clockwise
				NiAnimationKey<Quaternion> q; q.type = LINEAR_KEY; q.time = k[0];
				q.value = Quaternion(std::cos(th / 2), 0, 0, std::sin(th / 2));
				td->quaternionKeys.push_back(q);
				NiAnimationKey<float> s; s.type = LINEAR_KEY; s.time = k[0]; s.value = k[1];
				td->scales.AddKey(s);
			}
			uint32_t idD = hdr.AddBlock(std::move(td));
			auto ti = std::make_unique<NiTransformInterpolator>();
			ti->translation = Vector3(0, 0, 0); ti->rotation = Quaternion(1, 0, 0, 0); ti->scale = 1.0f;
			ti->dataRef.index = idD;
			uint32_t idI = hdr.AddBlock(std::move(ti));
			auto tc = std::make_unique<NiTransformController>();
			tc->flags = 0x48; tc->frequency = 1.0f; tc->phase = 0.0f; tc->startTime = 0.0f; tc->stopTime = keys.T;
			tc->targetRef.index = hdr.GetBlockID(wig);
			tc->interpolatorRef.index = idI;
			wig->controllerRef.index = hdr.AddBlock(std::move(tc));
		}
	}

	// ---- drop every vanilla scene element (logo, gem, flames...) that is not ours
	for (int i = (int)root->childRefs.GetSize() - 1; i >= 0; --i) {
		auto* o = hdr.GetBlock<NiObject>(root->childRefs.GetBlockRef(i));
		if (o && !keep.count(o)) root->childRefs.RemoveBlockRef(i);
	}
	// remove references first by id (descending order is safe because we only unlink)
	// delete everything not reachable from the root (robust against reference cycles)
	{
		std::set<uint32_t> reach; std::vector<uint32_t> stack{hdr.GetBlockID(root)};
		while (!stack.empty()) {
			uint32_t id = stack.back(); stack.pop_back();
			if (id == NIF_NPOS || reach.count(id)) continue;
			reach.insert(id);
			std::vector<uint32_t> ch; hdr.GetBlock<NiObject>(id)->GetChildIndices(ch);
			for (auto c : ch) stack.push_back(c);
		}
		int cnt = 0;
		for (int i = (int)hdr.GetNumBlocks() - 1; i >= 0; --i)
			if (!reach.count(i)) { hdr.DeleteBlock(i); cnt++; }
		std::cerr << "removed " << cnt << " unreachable blocks\n";
	}
	NifSaveOptions so; so.optimize = false; so.sortBlocks = false;
	if (nif.Save(argv[3], so)) { std::cerr << "save failed\n"; return 1; }
	return 0;
}
