import pystac
import planetary_computer
import rioxarray
import geopandas as gpd

from shapely.geometry import shape
from rasterio.features import shapes
from rasterio.features import shapes 

#item_url = "https://planetarycomputer.microsoft.com/api/stac/v1/collections/esa-worldcover/items/ESA_WorldCover_10m_2021_v200_N39W003"
item_url = "https://planetarycomputer.microsoft.com/api/stac/v1/collections/io-lulc/items/10S-2020"

# Load the individual item metadata and sign the assets
item = pystac.Item.from_file(item_url)

signed_item = planetary_computer.sign(item)

# Open one of the data assets (other asset keys to use: 'input_quality')
asset_href = signed_item.assets["map"].href
ds = rioxarray.open_rasterio(asset_href)

##### Convert in Geotiff
ds.rio.to_raster('land_cover.tif')



#### Convert GeoDataframe

# Convert the raster to a numpy array
raster_array = ds.squeeze().values  # Rimuovi le dimensioni singole
transform = ds.rio.transform()  # Ottieni la trasformazione

# Create shapes and get the corresponding values
mask = raster_array != 0  # Exclude null values if necessary
shapes_gen = shapes(raster_array, mask=mask, transform=transform)

# Create lists to hold geometries and class values
geometries = []
classes = []

for geom, value in shapes_gen:
    geometries.append(shape(geom))  # Convert to Shapely geometry
    classes.append(value)  # Append the class value

# Create a GeoDataFrame
gdf = gpd.GeoDataFrame({
    'geometry': geometries,
    'class': classes
}, crs='EPSG:4326')  

# Aggiungere la legenda
legend = {
    10: "Tree cover",
    20: "Shrubland",
    30: "Grassland",
    40: "Cropland",
    50: "Built-up",
    60: "Bare/sparse vegetation",
    70: "Snow and ice",
    80: "Permanent water bodies",
    90: "Herbaceous wetland",
    95: "Mangroves",
    100: "Moss and lichen"
}

# Mappare le classi ai nomi corrispondenti nella legenda
gdf['classification'] = gdf['class'].map(legend)

# Export the GeoDataFrame as GeoJSON
gdf.to_file("output.geojson", driver='GeoJSON')