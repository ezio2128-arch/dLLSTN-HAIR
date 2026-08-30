# TN Character Rebuild 0.5.2 — Thin Separators

Código fuente integrado para Community Shaders 1.8.3 / Skyrim AE 1.6.1170.

Incluye:

- TN Medieval Hair dentro de Hair Specular.
- Presets Balanced, Cinematic y Extreme reajustados para separadores más finos.
- Controles en tiempo real para intensidad, separación, fibras finas, cavidad y reflejos.
- Persistencia en `SettingsUser.json`.
- Shader reversible: OFF devuelve el comportamiento de Hair Specular sin la reconstrucción TN.
- Perfil visual nuevo: micro-líneas oscuras más finas que dividen el cabello en fibras más creíbles, con cuerpo general más suave y menos aspecto rugoso.

No incluye TN Adaptive 80 (AD80).

El workflow genera el artifact instalable `TN-Character-Rebuild-052-CS183-MO2`.

## Orden MO2

1. Community Shaders 1.8.3
2. Hair Specular 1.1.2
3. Community Shaders True North Settings
4. TN Character Rebuild 0.5.2
5. TN Adaptive 80, opcional y separado
6. TN Smooth Motion Blur, opcional

## Nota

Este ajuste se centra en la iluminación del pelo, no en reemplazar alphas o texturas base. La idea es acercar el look a separadores finos y fibras más suaves usando el shader, sin cambiar el peinado ni la cobertura alpha.
