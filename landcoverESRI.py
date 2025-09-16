import pystac
import planetary_computer
import rioxarray
import geopandas as gpd

from shapely.geometry import shape
from rasterio.features import shapes
from rasterio.features import shapes 

#item_url = "https://planetarycomputer.microsoft.com/api/stac/v1/collections/esa-worldcover/items/ESA_WorldCover_10m_2021_v200_N39W003"
item_url = "https://planetarycomputer.microsoft.com/api/stac/v1/collections/io-lulc/items/33T-2020"

# Load the individual item metadata and sign the assets
item = pystac.Item.from_file(item_url)

signed_item = planetary_computer.sign(item)

# Open one of the data assets (other asset keys to use: 'input_quality')
asset_href = signed_item.assets["data"].href
ds = rioxarray.open_rasterio(asset_href)
utm_crs = ds.rio.estimate_utm_crs()
geojson = gpd.read_file("clip_box.geojson")

# Trasforma il GeoDataFrame da WGS84 (EPSG:4326) al CRS UTM stimato
geojson_utm = geojson.to_crs(utm_crs)
minx, miny, maxx, maxy = geojson_utm.total_bounds
ds = ds.rio.clip_box(
    minx=minx,
    miny=miny,
    maxx=maxx,
    maxy=maxy,
)
# Riproietta a WGS84
#data_array_wgs84 = ds.rio.reproject("EPSG:4326")  # EPSG:4326 è WGS84
'''# Ottieni il bounding box dal GeoJSON
minx, miny, maxx, maxy = geojson_utm.total_bounds

# Ritaglia il DataArray usando il bounding box
clipped_data = ds.sel(
    x=slice(minx, maxx),  # Adatta i nomi delle coordinate se necessario
    y=slice(miny, maxy)
)
'''
ds = ds.rio.reproject("EPSG:4326")

##### Convert in Geotiff
ds.rio.to_raster('land_cover.tif')


#ds = ds.rio.clip(geojson_utm.geometry)


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
legend_ESA = {
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

legend_ESRI = {
    0: "No data",
    1: "Water",
    2: "Trees",
    3: "Grass",
    4: "Flooded vegetation",
    5: "Crops",
    6: "Scrub",
    7: "Built area",
    8: "Bare",
    9: "Snow/Ice",
    10: "Clouds"
}

# Mappare le classi ai nomi corrispondenti nella legenda
gdf['classification'] = gdf['class'].map(legend_ESRI)

# Export the GeoDataFrame as GeoJSON
gdf.to_file("output_LandCover_ESRI.geojson", driver='GeoJSON')