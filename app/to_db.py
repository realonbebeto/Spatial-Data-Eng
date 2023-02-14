import geopandas as gpd
import pandas as pd
import boto3
from config import settings
from sqlalchemy import create_engine

BUCKET_NAME = 'ds-interview-sandbox'
DATABASE_URL = f'postgresql+psycopg2://{settings.database_username}:{settings.database_password}@{settings.database_host}:{settings.database_port}/{settings.database_name}'
engine = create_engine(DATABASE_URL)

# Commented out because of local run
# client = boto3.client('s3')
# s3 = boto3.resource('s3')
# bucket = s3.Bucket(BUCKET_NAME)

# # Download the files
# for obj in bucket.objects.filter(Prefix='shared/ug'):
#     key = obj.key
#     bucket.download_file(key, f"./{key.split('/')[-1]}")


def boolify(val: int):
    if val > 0:
        return 'yes'
    elif val == 0:
        return 'no'
    else:
        return None


# Renaming Cols
cols = {"v001": "cluster_id",
        "v002": "household_no",
        "v003": "respondent_line",
        "v012": "respondent_age",
        "v133": "education_ages",
        "v535": "married",
        "adult_radio_regular": "adult_radio_regular",
        "v751": "hiv_aware",
        "sex": "sex", }


# Read DHS
dhs = pd.read_csv(
    "~/Documents/kazispaces/desrc/Spatial-Data-Eng/data/uga_dhs_2016.csv")
dhs = dhs.rename(columns=cols)
dhs['married'] = dhs.married.apply(lambda x: boolify(x))
dhs['hiv_aware'] = dhs.hiv_aware.apply(lambda x: boolify(x))
dhs['adult_radio_regular'] = dhs.adult_radio_regular.apply(
    lambda x: boolify(x))

# Read Custers
ug_clusters = pd.read_csv(
    "~/Documents/kazispaces/desrc/Spatial-Data-Eng/data/ug_clusters.csv")
ug_clusters = ug_clusters.rename(columns={"v001": "cluster_id"})
ug_clusters = gpd.GeoDataFrame(
    ug_clusters, geometry=gpd.points_from_xy(ug_clusters.LONGNUM, ug_clusters.LATNUM))
ug_clusters.columns = [x.lower() for x in ug_clusters.columns]
ug_clusters = ug_clusters.set_crs(4326, allow_override=True)

# Read regions
regions = gpd.read_file(
    "~/Documents/kazispaces/desrc/Spatial-Data-Eng/data/uga_regions.geojson")
regions.columns = [x.lower() for x in regions.columns]

# Merge Regions and Cluster
clus_reg = ug_clusters.sjoin(regions, how="left")


# Merge DHS and Regions and Clusters
out = dhs.merge(clus_reg, how="left", on="cluster_id")
out = out[['cluster_id', 'household_no',
           'respondent_line', 'respondent_age', 'education_ages', 'married', 'adult_radio_regular', 'hiv_aware', 'sex', 'geometry', 'name', 'iso_code',
           'iso2_code']]
out = gpd.GeoDataFrame(out, crs="EPSG:4326", geometry=out.geometry)

# Publish to DB
out.to_postgis("ug_dhs", engine, if_exists='append')
