import geopandas as gpd

# Funzione per caricare un GeoJSON, trasformarlo e salvarlo
def transform_geojson(input_file, output_file, target_crs="EPSG:4326"):
    # Carica il GeoJSON in un GeoDataFrame
    gdf = gpd.read_file(input_file)
    gdf.crs = "EPSG:6875"
    # Controlla il CRS corrente
    print("CRS corrente:", gdf.crs)

    # Trasforma il GeoDataFrame nel CRS target
    gdf = gdf.to_crs(target_crs)

    # Salva il GeoDataFrame trasformato come GeoJSON
    gdf.to_file(output_file, driver='GeoJSON')
    
    print(f"GeoJSON trasformato e salvato come {output_file}")

# Esempio di utilizzo
input_geojson = 'input.geojson'  # Sostituisci con il percorso del tuo file GeoJSON
output_geojson = 'output.geojson'  # Sostituisci con il percorso del file di output

transform_geojson(input_geojson, output_geojson)
