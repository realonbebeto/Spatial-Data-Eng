from sqlalchemy import create_engine, text
from config import settings

DATABASE_URL = f'postgresql+psycopg2://{settings.database_username}:{settings.database_password}@{settings.database_host}:{settings.database_port}/{settings.database_name}'

engine = create_engine(DATABASE_URL)


def filter_count(region: str, sex: str) -> int:
    """
    filter_count runs to count the number of records in the database based 
    on two features who have ever heard of AIDS

    Params:
    region (string): area of interest for the survey e.g. 'Northern, 'Central'
    sex (string): gender of interest e.g. 'male' or 'female'

    Returns:
    count(int): the number of records based on region and sex
    """
    query = text("""SELECT COUNT(r.v001) 
                    FROM (SELECT dhs.v001, dhs.sex, d.name, dhs.v751 
                            FROM ug_dhs dhs JOIN (SELECT DISTINCT a.v001, b.name
                        FROM ug_clusters a
                        JOIN ug_regions b
                    ON ST_contains(b.geometry, a.geometry)) as d
                    ON dhs.v001=d.v001
                    WHERE dhs.sex=:sex AND dhs.v751=1 AND d.name=:region) AS r""").bindparams(region=region, sex=sex)
    count = engine.execute(query).fetchall()[0][0]
    return count


if __name__ == '__main__':
    region = 'Northern'
    sex = 'male'
    print(filter_count(region, sex))
