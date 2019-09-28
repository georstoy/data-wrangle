#!/usr/bin/env python
'''
Import a list of MongoDb collections from source files.
The collections list is specified in COLLECTIONS
The database and source files info is taken from a config file
Sample config: database.yml.sample
'''
import csv
import yaml
import datetime as dt
from pymongo import MongoClient

CONFIG_FILE = 'database.yml'
COLLECTIONS = ['autos']

def read_config(file):
    with open(file, 'r') as cfg_file:
        cfg = yaml.safe_load(cfg_file)
    return cfg

def read_headers(filename):
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
    return headers
        
def read(filename):
    data = []
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for line in reader:
            data.append(line)    
    return data

def get_db(cfg):
    uri = cfg['uri']
    for param in ['cluster', 'user', 'password']:
        uri = uri.replace('<'+param+'>', cfg[param])
    client = MongoClient(uri)
    db = client[cfg['dbname']]
    return db

def announce(message):
    l.write(str(dt.datetime.now())+': '+message)
    print(message)            

if __name__ == "__main__":
    l = open('import_log', 'a')
    cfg = read_config(CONFIG_FILE)
    db = get_db(cfg)

    for coll_name, datafile in cfg['collections']:
        if coll_name in COLLECTIONS:
            data = read(datafile)
            coll = db[coll_name]
            announce('importing '+coll_name+' from '+datafile+'\n')
            coll.insert(data)