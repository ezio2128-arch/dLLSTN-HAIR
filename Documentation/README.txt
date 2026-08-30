TN Character Rebuild - Community Shaders Addon v0.6
===================================================

TARGET
- Skyrim AE 1.6.1170
- Community Shaders 1.8.3
- Hair Specular 1.1.2 (required)

WHAT CHANGED FROM v0.5
- Removed the bundled/modified CommunityShaders.dll.
- Removed TN Adaptive 80 from this package. AD80 stays independent.
- Removed the SharedData.hlsli replacement.
- Reworked TN Medieval Hair to use shader-local preset constants.
- The addon now overwrites only Shaders/Hair/Hair.hlsli and TangentShift.dds.

WHY
Community Shaders 1.8.3 compiles Feature C++ classes into CommunityShaders.dll. It does not
provide a public external Feature-registration ABI for arbitrary third-party Feature classes.
The previous TN sliders therefore required a custom CommunityShaders.dll and a modified
constant-buffer layout. This v0.6 avoids that coupling and is safe to layer over stock CS.

MO2 ORDER
1. Community Shaders 1.8.3
2. Hair Specular 1.1.2
3. Community Shaders True North Settings
4. TN Adaptive 80 (your existing addon/build, if used)
5. TN Character Rebuild - CS Addon v0.6
6. TN Smooth Motion Blur, optional

INSTALL
Install the ZIP in MO2. The FOMOD asks for Balanced, Cinematic, or Extreme.
Cinematic reproduces the v0.5 default TN values (all 1.0).

MENU
This standalone shader-only build does NOT add a separate TN Medieval Hair section to the END
menu. Hair Specular's normal controls remain available and continue to work. A new live TN UI
would require rebuilding CommunityShaders.dll or an official external feature API from CS.

UNINSTALL
Disable/remove this addon in MO2. Hair Specular's original shader underneath becomes active again.
No save-game data is written.
