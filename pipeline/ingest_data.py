#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from tqdm.auto import tqdm
from sqlalchemy import create_engine

year=2021
month=1

prefix='https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
url=f'{prefix}/yellow_tripdata_{year}-{month:02d}.csv.gz'


dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]

def run():
    
    pg_user='root'
    pg_pass='root'
    pg_host= 'localhost'
    pg_port=5432
    pg_db='ny_taxi'

    # df = pd.read_csv(
    #     url,

    #     dtype=dtype,
    #     parse_dates=parse_dates
    # )
    # engine = create_engine('postgresql://{pg_user}:{pg_pass}@{pg_host}:5432/{pg_db}')
    engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')
    print (engine)

    # print(pd.io.sql.get_schema(df, name={target_table}, con=engine))

  
    chunksize=100000
    df_iter = pd.read_csv(
        url,
        dtype=dtype,
        parse_dates=parse_dates,
        iterator=True,
        chunksize=chunksize
    )
    first=True
    target_table='yellow_taxi_data_1'
    for df_chunk in tqdm(df_iter):
        print ("Chunk started")
        
        if first:
            df_chunk.head(0).to_sql(name=target_table, con=engine, if_exists='replace')
            print ('Table Header added')
            first=False
            print ("Header already exist")

        df_chunk.to_sql(name=target_table, con=engine, if_exists='append')



if __name__ == '__main__':
    run()




