# TN Character Rebuild 0.6 — White Hair Bypass + Performance

Código fuente integrado para Community Shaders 1.8.3 / Skyrim AE 1.6.1170.

Incluye:

- TN Medieval Hair dentro de Hair Specular.
- Presets Balanced, Cinematic y Extreme sin cambiar sus valores de la v0.5.1.
- Controles en tiempo real para intensidad, separación, fibras finas, cavidad y reflejos.
- Persistencia en `SettingsUser.json`.
- Shader reversible: OFF devuelve el comportamiento de Hair Specular sin la reconstrucción TN.
- Exclusión automática de cabello blanco y gris neutro: TN Medieval Hair no modifica su cavidad ni su compresión de reflejos.
- Ruta TN optimizada: reemplaza tres evaluaciones trigonométricas `sin()` por una variación UV de bajo coste y añade salidas tempranas.

No incluye TN Adaptive 80 (AD80).

El workflow genera el artifact instalable `TN-Character-Rebuild-06-CS183-MO2`.

## Orden MO2

1. Community Shaders 1.8.3
2. Hair Specular 1.1.2
3. Community Shaders True North Settings
4. TN Character Rebuild 0.6
5. TN Adaptive 80, opcional y separado
6. TN Smooth Motion Blur, opcional

## Nota sobre cabello blanco

La exclusión se hace automáticamente usando el color final del material del cabello. El objetivo es conservar el Hair Specular original en blancos, plateados y grises neutros, mientras TN Medieval Hair sigue actuando en cabellos negros, castaños, rojizos y rubios con cromaticidad apreciable.
