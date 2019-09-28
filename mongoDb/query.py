#!/usr/bin/env python
"""
Your task is to complete the 'porsche_query' function and in particular the query
to find all autos where the manufacturer field matches "Porsche".
Please modify only 'porsche_query' function, as only that will be taken into account.

Your code will be run against a MongoDB instance that we have provided.
If you want to run this code locally on your machine,
you have to install MongoDB and download and insert the dataset.
"""
from pymongo import MongoClient
import yaml
import pprint

def get_db(db_name):
    
    with open('mongo.yml') as f:
        credentials = yaml.load(f, Loader=yaml.FullLoader)
    try:
        client = MongoClient('mongodb+srv://user:'+credentials['password']+
            '@testcluster-stbzj.mongodb.net/test?retryWrites=true&w=majority')
        print('Successful connection!\n')
    except:
        print('Unsuccessful connection!\n')
    
    print('DBs :'+' '.join(client.database_names()))
    db = client[db_name]
    return db

def porsche_query():
    query = {'manufacturer': 'Porsche'}
    return query

def find_porsche(db, query):
    return db.autos.find(query)


if __name__ == "__main__":
    db = get_db('examples')
    query = porsche_query()
    #query = {}
    results = find_porsche(db, query)

    print("Printing first 3 results\n")
    for car in results[:3]:
        pprint.pprint(car)