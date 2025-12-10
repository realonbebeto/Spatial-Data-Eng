from config import settings
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

DATABASE_URL = f"postgresql+psycopg2://{settings.database_username}:{settings.database_password}@{settings.database_host}:{settings.database_port}/{settings.database_name}"

engine = create_engine(DATABASE_URL)


def filter_count(region: str, sex: str, hiv: str = "yes") -> int:
    """
    filter_count runs to count the number of records in the database based
    on two features who have ever heard of AIDS

    Params:
    region (string): area of interest for the survey e.g. 'Northern, 'Central'
    sex (string): gender of interest e.g. 'male' or 'female'
    hiv (string): if person is hiv aware e.g. 'yes' or 'no'

    Returns:
    count(int): the number of records based on region and sex
    """
    query = text("""SELECT COUNT(*) 
                    FROM ug_dhs
                    WHERE sex=:sex AND hiv_aware=:hiv AND name=:region""").bindparams(
        region=region, sex=sex, hiv=hiv
    )

    with Session(engine) as session:
        count = session.execute(query).fetchall()[0][0]
    return count


if __name__ == "__main__":
    region = "Northern"
    sex = "male"
    hiv = "yes"
    print(filter_count(region, sex, hiv))
