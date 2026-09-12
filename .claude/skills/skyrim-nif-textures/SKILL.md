---
name: skyrim-nif-textures
description: Skyrim SE/AE mesh and texture engineering workflow for NIF, PyNifly/NifSkope-style inspection, texture paths, DDS assets and shader/material consistency. Use when creating or repairing meshes, chain props, armor/weapon visuals, texture sets, normals, masks, or path/shader problems.
---

# Skyrim NIF and Textures

## Mesh rules

- Determine whether an asset is source, reference, generated, or game-ready.
- Preserve Skyrim-compatible node hierarchy and transforms expected by the target use.
- Verify texture paths from the actual NIF/project data; do not infer them from filenames alone.
- For skinned assets, verify skeleton/bone bindings. For attached props, verify the target node and scale in the actual skeleton.
- If using PyNifly or NifSkope-like tools, record what was verified and with which tool.

## Texture rules

Before editing:
1. identify each map's role;
2. inspect resolution, alpha usage, and current compression/format if tooling allows;
3. preserve naming/path conventions used by the mod;
4. avoid changing format/compression unless there is a specific reason.

For a new visual family, define a deliberate material identity:
- base/albedo character,
- rough/specular response as supported by the shader setup,
- normal detail,
- metal/aged/daedric cues where appropriate,
- readable silhouette before microdetail.

Do not claim a texture "looks correct" without rendering it on the intended mesh/material or testing in game.

## Chain assets

For chain-like props:
- model readable links or an appropriate continuous representation rather than placeholder sticks;
- avoid impossible scale relative to hand/forearm;
- maintain a clear proximal attachment and distal direction;
- keep collision/physics representation separate from visual link density when practical;
- do not copy proprietary game assets from reference titles. Recreate an original asset from design cues only.

## Validation

- path/structure checks -> `STATICALLY VALID`;
- rendered material/mesh comparison -> `VISUALLY VERIFIED`;
- observed in Skyrim -> `IN-GAME VERIFIED`.
