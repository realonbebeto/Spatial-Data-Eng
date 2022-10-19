# Fraym Interview Solution

* Data Exploration
* PostGIS Database Establishment
* Downloading, Reading and Loading Data from S3 
* Query Writing and Python Encapsulation 

## Code and Resources Used 
**Python Version:** 3.8  
**Packages:** requirements.txt 


## Data Exploration
Understanding the relationship of the 3 files:

*	DHS records are clustered and clusters have locations (LONG, LAT)
*   And clusters exist within regions(have bounds)

## * PostGIS Database Establishment
For a spatial postgres database, 2 extensions are created using

*	postgis
*   postgis topology

## Downloading, Reading and Loading Data from S3 to DB
The 3 files have different needs for loading to the:

*	uga_dhs_2016.csv is loaded from a pandas dataframe
*   ug_clusters.csv is loaded from a geopandas dataframe after re-establishing point geometry from the LATNUM and LONGNUM and setting the CRS to match the one in the regions
*   uga_regions.geojson is loaded from a geopandas dataframe 


## Query Writing and Python Encapsulation
The query in the filter_count Python function, which takes in 2 parameters achieves a count of records after filters by way of:

*   assigning ug_clusters to their respective regions(uga_regions.csv) via a inner join
*   then it follows by attaching the preceding database view above to the dhs 2016 data
*   Finally, a count is performed on the any resulting column (no column is UNIQUE) and return the result(int)

## Result
How many males in the Northern region have ever heard of AIDS?

*   1232
