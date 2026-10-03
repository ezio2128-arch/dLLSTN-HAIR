# Living Lands – Menú principal animado para Skyrim Special Edition

Reemplaza el fondo del menú principal por el video "Living Lands" (loop de 30 s):
vela encendida con la llama parpadeando → la llama se apaga → la luz de vela se funde en luz de luna →
mesa a oscuras (10 s) → la vela se enciende sola → vuelve a empezar.

Basado en la técnica del mod *Daggerfall-Style Animated Main Menu Screen*: se reemplaza
`meshes/interface/logo/logo.nif` (y `logo01ae.nif`, la variante Anniversary Edition) y se añaden texturas propias.

> **Importante:** Skyrim no puede reproducir un MP4 de fondo en el menú sin un plugin SKSE.
> Este mod reproduce la secuencia **dentro del motor** con capas de textura animadas
> (fundido de alpha entre dos imágenes + una llama animada), no con un video.
> Fue generado y comprobado a nivel de archivos (NIF/DDS válidos), pero **no pude abrir Skyrim para probarlo**;
> por eso incluyo variantes de respaldo (abajo).

## Contenido
| Carpeta | Qué es |
|---|---|
| `Animated/` | Versión principal (3 capas animadas). Instala **esta** primero. |
| `Animated_FlipDepth/` | Solo 2 archivos `.nif`. Cámbialos por los de `Animated` **solo si** con la principal no ves el fundido/llama (ver abajo). |
| `Static_Fallback/` | Versión sin animación (solo la imagen de la vela). Es el método exacto del mod de referencia: la más segura. |
| `tools/` | Scripts y código para regenerar todo. |

## Instalación
Con Vortex / Mod Organizer 2: comprime la carpeta (`meshes` y `textures` en la raíz del zip) e instálala como mod.
A mano: copia el contenido de `Animated/` dentro de `Skyrim Special Edition/Data/`.
Desactiva/desinstala cualquier otro mod que reemplace `meshes\interface\logo\logo.nif`
(por ejemplo el de Daggerfall) – el último en cargarse gana.

## Si algo no se ve bien
1. **Solo se ve la mesa a oscuras (luna) y nunca la vela / no hay llama:** el orden de capas está al revés
   en tu cámara. Copia los dos `.nif` de `Animated_FlipDepth/meshes/interface/logo/` encima de los de `Animated`.
2. **Pantalla negra o nada funciona:** instala `Static_Fallback` en lugar de `Animated`.
3. Si ves la imagen más oscura/clara de lo esperado: las capas usan un shader de efecto (sin iluminación de escena),
   así que debería verse igual que el video; avísame con una captura y ajusto.

## Notas técnicas
* Texturas 2048×1024 (el plano del menú mapea UV 0–1 a un área 16:9, por eso la imagen 16:9 va "aplastada" a 2:1), BGRA8 sin comprimir con mipmaps.
* Las dos imágenes se alinean a una geometría intermedia (desplazamiento máx. ~1–2 px) para que el fundido no muestre doble contorno.
* Capas: `moon` (mesa a oscuras, base) · `warm` (mesa con vela, sin llama; alpha animado) · `flame` (sprite aditivo con inclinación/escala animadas).
* Todo se repite cada 30 s (controladores NIF en bucle).
* Se eliminan del NIF el logo 3D, la gema y las llamas originales.

## Regenerar
```
python3 tools/make_assets.py 1.jpg 2.jpg work      # texturas + tablas de animación
# compilar tools/build_nif.cpp contra nifly (https://github.com/ousnius/nifly) y:
build_nif anim logo_original.nif logo.nif work/keys.txt work/layout.txt "textures\livinglandsmenu"
```
(`anim` | `animflip` | `static`). Se necesita el `logo.nif` del mod Daggerfall como plantilla.
