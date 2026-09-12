# TN Chains animation acceptance

## Reference authority

Use project-provided Witcher reference footage for visual identity/context.
When exact joint biomechanics are obscured, prefer clearer real flexible-weapon references such as rope-dart/meteor-hammer footage.
A readable chained-weapon reference may inform weight/extension rhythm, but exaggerated superhuman amplitude must be reduced.

Do not "remember" the reference. Use actual stored clips/frames when available.

## Required phase structure

1. STANCE
2. ANTICIPATION
3. LOAD
4. TORSO INITIATION
5. SHOULDER INITIATION
6. ELBOW LEAD
7. WRIST ACCELERATION
8. RELEASE
9. CHAIN EXTENSION
10. TENSION
11. IMPACT / PULL
12. FOLLOW-THROUGH
13. RECOVERY

Not every clip needs a separate keyframe for every label, but the temporal ordering must remain readable.

## Biomechanical rules

- pelvis load/reversal begins before torso;
- torso begins before shoulder;
- shoulder begins before elbow;
- elbow leads wrist and remains soft;
- wrist steers the plane late;
- right hand/main weapon remains ready and counterbalances rather than mirroring left arm;
- distal chain mass lags during acceleration;
- release occurs before maximum extension;
- tension occurs after extension;
- pull uses legs/pelvis/back before elbow flexion;
- body recenters before chain fully settles;
- use asymmetry and overlap.

## Automatic rejection conditions

Reject the animation if any of these are visible:
- mechanical perfect-circle arm motion without body contribution;
- tiny/proxy-looking arm or incorrect proportions;
- obvious skeleton/retarget deformation;
- chain represented as rigid sticks in the final visual;
- chain appears magically only at release with no physical pre-state;
- staff/spell/gun presentation;
- all body segments peak simultaneously;
- release, extension and impact occur on the same instant;
- right-hand weapon is unnecessarily holstered or loses the intended combat silhouette;
- severe foot sliding/body snapping introduced by the clip.

## Acceptance evidence

Before export:
- render at least front/3-quarter/side views or an equivalent readable camera set;
- inspect ordered frames around anticipation, release, extension, tension, and recovery;
- write a short comparison showing what matches and what still differs.

The animation is acceptable for integration only after `VISUALLY VERIFIED`.
