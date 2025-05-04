'''
Reprojection (Rasterio - NO COG format only GTiff)
'''

import glob
import os
import rasterio
from rasterio.warp import calculate_default_transform



# Specifica il percorso ai file TIFF
FOLDER_PATH = r'path_to_tiff\*.tif'  # Sostituisci con il percorso corretto

# Trova tutti i file TIFF nella cartella
tif_files = glob.glob(FOLDER_PATH)

# Percorso di output per i file riproiettati
OUTPUT_FOLDER = r'output\reprojected'  # Sostituisci con il percorso corretto

# Riproietta ogni file TIFF
for tif_file in tif_files:
    with rasterio.open(tif_file) as src:
        # Leggi i dati
        data = src.read()
        # Riproietta il raster

        src_crs = src.crs
        transform, width, height = calculate_default_transform(
            src_crs,
            'EPSG:3857', 
            src.width,
            src.height,
            *src.bounds
            )
        kwargs = src.meta.copy()

        kwargs.update({
            'crs': 'EPSG:3857',
            'transform': transform,
            'width': width,
            'height': height})



        # Crea un nuovo file riproiettato
        output_file = os.path.join(OUTPUT_FOLDER, os.path.basename(tif_file))
        # Salva il file riproiettato
        with rasterio.open(
            output_file,
            'w',
            driver='GTiff',
            height=height,
            width=width,
            count=src.count,
            dtype=data.dtype,
            crs='EPSG:3857',
            transform=transform
        ) as dst:
            dst.write(data)
        print(tif_file)

print("Tutti i file TIFF sono stati riproiettati in EPSG:3857.")
