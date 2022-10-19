import geopandas as gpd
import pandas as pd
import boto3
from config import settings
from sqlalchemy import create_engine

BUCKET_NAME = 'ds-interview-sandbox'
DATABASE_URL = f'postgresql+psycopg2://{settings.database_username}:{settings.database_password}@{settings.database_host}:{settings.database_port}/{settings.database_name}'
engine = create_engine(DATABASE_URL)

client = boto3.client('s3')
s3 = boto3.resource('s3')
bucket = s3.Bucket(BUCKET_NAME)

# Download the files
for obj in bucket.objects.filter(Prefix='shared/ug'):
    key = obj.key
    bucket.download_file(key, f"./{key.split('/')[-1]}")


# Load regions
gdf = gpd.read_file("./uga_regions.geojson")
gdf.columns = [x.lower() for x in gdf.columns]
gdf.to_postgis("ug_regions", engine)


# Load clusters
df = pd.read_csv("./ug_clusters.csv")
ug_clusters = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.LONGNUM, df.LATNUM))
ug_clusters.columns = [x.lower() for x in ug_clusters.columns]
ug_clusters = ug_clusters.set_crs(4326, allow_override=True)
ug_clusters.to_postgis("ug_clusters", engine)

# Load dhs
df = pd.read_csv("./uga_dhs_2016.csv")
df.columns = [x.lower() for x in df.columns]
df.to_sql("ug_dhs", engine)
