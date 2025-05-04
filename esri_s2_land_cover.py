'''
ESRI Land Cover Sentinel 2 (Planetary Computer)
'''
import glob
import pystac
import planetary_computer
import rioxarray
import rasterio
from rasterio.merge import merge

utm_zones = [
    "10U",
    "11U",
    "12U",
    "13U",
    "14U",
    "10T",
    "11T",
    "12T",
    "13T",
    "14T",
    "10S",
    "11S",
    "12S",
    "13S",
    "14S",
    "12R",
    "13R",
    "14R",
]
for utm_zone in utm_zones:
    ITEM_URL = f"https://planetarycomputer.microsoft.com/api/stac/v1/collections/io-lulc/items/{utm_zone}-2020"
    # Load the individual item metadata and sign the assets
    item = pystac.Item.from_file(ITEM_URL)

    signed_item = planetary_computer.sign(item)
        # Open one of the data assets (other asset keys to use: 'input_quality')
    asset_href = signed_item.assets["data"].href
    ds = rioxarray.open_rasterio(asset_href)
    ds.rio.to_raster(f'./output/ESRI_LandCover_{utm_zone}.tif')
# Trova tutti i file TIFF nella cartella

# Specifica il percorso della cartella contenente i file Excel
FOLDER_PATH = './output/*.tif'  # Sostituisci con il percorso corretto

# Trova tutti i file Excel nella cartella
tif_files = glob.glob(FOLDER_PATH)

# Crea una lista per memorizzare i dataset raster
src_files_to_mosaic = []

# Apri ciascun file TIFF e aggiungilo alla lista
for tif_file in tif_files:
    src = rasterio.open(tif_file)
    #src_files_to_mosaic.append(src)

# Esegui il merge dei raster
mosaic, out_trans = merge(tif_files)

# Metadati del raster unito
out_meta = src.meta.copy()
out_meta.update({
    'driver': 'GTiff',
    'height': mosaic.shape[1],
    'width': mosaic.shape[2],
    'transform': out_trans
})

# Salva il raster unito in un nuovo file TIFF
OUTPUT_FILE = r'output_folder\ESRI_LandCover_merged.tif'  # Sostituisci con il percorso corretto
with rasterio.open(OUTPUT_FILE, 'w', **out_meta) as dest:
    dest.write(mosaic)

print(f"File TIFF unito salvato come: {OUTPUT_FILE}")

# Chiudi i file raster aperti
for src in src_files_to_mosaic:
    src.close()
