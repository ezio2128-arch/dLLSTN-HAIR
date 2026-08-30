# TN Character Rebuild - CS 1.8.3 Addon v0.6

Standalone MO2 addon for **Community Shaders 1.8.3** + **Hair Specular 1.1.2**.

## What this version does
- Removes the integrated **TN Adaptive 80 (AD80)** from the package.
- Does **not** ship a custom `CommunityShaders.dll`.
- Does **not** replace `Shaders/Common/SharedData.hlsli`.
- Only overrides Hair Specular shader assets:
  - `Shaders/Hair/Hair.hlsli`
  - `Shaders/Hair/TangentShift.dds`

## Included presets
- Balanced
- Cinematic (recommended; matches the v0.5 default TN values)
- Extreme

## MO2 load order
1. Community Shaders 1.8.3
2. Hair Specular 1.1.2
3. Community Shaders True North Settings
4. TN Adaptive 80 (optional, separate mod)
5. TN Character Rebuild - CS Addon v0.6
6. TN Smooth Motion Blur (optional)

## GitHub Actions
The workflow at `.github/workflows/build-mo2.yml` packages the files into:
`TN-Character-Rebuild-CS183-Addon-v0.6-MO2.zip`

Upload the repository contents to GitHub root, then run **Actions -> Build TN Character Rebuild CS183 Addon v0.6 MO2**.
