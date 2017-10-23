
# coding: utf-8

# In[452]:

import sqlite3
import pandas as pd
import csv
from pprint import pprint


# ## Creating Adelaide Database

# In[453]:

# name of adelaide database
sqlite_file = 'adelaide.db'

# connect to database
conn = sqlite3.connect(sqlite_file)

# get a cursor object
cur = conn.cursor()


# ## Previewing Data and Identifying Any Potential Issues with Each Table using Pandas

# In[454]:

# read csv to view data

file = pd.read_csv('nodes.csv')
file.head()

# this id is referencing nodes_tags id


# In[455]:

# read csv to view data

file = pd.read_csv('nodes_tags.csv')
file.head()

# this id is primary key for nodes


# In[456]:

# read csv to view data

file = pd.read_csv('ways.csv')
file.head()

# this id is referencing ways_tags id


# In[457]:

# read csv to view data

file = pd.read_csv('ways_nodes.csv')
file.head()

# this id is referencing ways_tags id


# In[458]:

# read Ways_Tags csv to view data

file = pd.read_csv('ways_tags.csv')
file.head()

# this id is the primary key


# ## Creating Tables for Each File from Data.Py Output using SQLite3 Library
# 
# ##### https://discussions.udacity.com/t/creating-db-file-from-csv-files-with-non-ascii-unicode-characters/174958/7
# ##### https://discussions.udacity.com/t/loading-csvs-into-database/314549

# In[459]:

# If re-running code, you must first drop table that pre-existed

cur.execute('DROP TABLE IF EXISTS nodes')
cur.execute('DROP TABLE IF EXISTS nodes_tags')
cur.execute('DROP TABLE IF EXISTS ways')
cur.execute('DROP TABLE IF EXISTS ways_tags')
cur.execute('DROP TABLE IF EXISTS ways_nodes')

# All tables have 'Id' to use as a primary key
# Found schema at below url
# https://gist.github.com/swwelch/f1144229848b407e0a5d13fcb7fbbd6f

# nodes table

cur.execute('''
    CREATE TABLE nodes
    (
    id INTEGER PRIMARY KEY NOT NULL, 
    lat REAL, 
    lon REAL, 
    user TEXT,
    uid INTEGER,
    version INTEGER,
    changeset INTEGER,
    timestamp TEXT
    )
    ''')

# nodes_tags table

cur.execute('''
    CREATE TABLE nodes_tags
    (
    id INTEGER,
    key TEXT,
    value TEXT,
    type TEXT,
    FOREIGN KEY (id) REFERENCES nodes(id)
    )
    ''')

# ways table

cur.execute('''
    CREATE TABLE ways
    (
    id INTEGER PRIMARY KEY NOT NULL, 
    user TEXT, 
    uid INTEGER, 
    version TEXT,
    changeset INTEGER,
    timestamp TEXT
    )
    ''')

# ways_tags table

cur.execute('''
    CREATE TABLE ways_tags
    (
    id INTEGER NOT NULL, 
    key TEXT NOT NULL, 
    value TEXT NOT NULL, 
    type TEXT,
    FOREIGN KEY (id) REFERENCES ways(id)
    )
    ''')

# ways_nodes table

cur.execute('''
    CREATE TABLE ways_nodes
    (
    id INTEGER NOT NULL, 
    node_id INTEGER NOT NULL, 
    position INTEGER NOT NULL,
    FOREIGN KEY (id) REFERENCES ways(id),
    FOREIGN KEY (node_id) REFERENCES nodes(id)
    )
    ''')

conn.commit()


# ## Reading CSVs as dictionary

# In[460]:

# Read in CSV file as dictionary, format the data as a list of tuples
with open('nodes.csv','rb') as fin1:
# csv.DictReader uses first line in file for column headings by default
    dict1 = csv.DictReader(fin1)
    to_db1 = [(i['id'].decode('utf-8'), i['lat'].decode('utf-8'), i['lon'].decode('utf-8'), i['user'].decode('utf-8'), i['uid'].decode('utf-8'), i['version'].decode('utf-8'), i['changeset'].decode('utf-8'), i['timestamp'].decode('utf-8')) for i in dict1]

with open('nodes_tags.csv','rb') as fin2:
    dict2 = csv.DictReader(fin2)
    to_db2 = [(i['id'].decode('utf-8'), i['key'].decode('utf-8'), i['value'].decode('utf-8'), i['type'].decode('utf-8')) for i in dict2]

with open('ways.csv','rb') as fin3:
    dict3 = csv.DictReader(fin3)
    to_db3 = [(i['id'].decode('utf-8'), i['user'].decode('utf-8'), i['uid'].decode('utf-8'), i['version'].decode('utf-8'), i['changeset'].decode('utf-8'), i['timestamp'].decode('utf-8')) for i in dict3]

with open('ways_tags.csv','rb') as fin4:
    dict4 = csv.DictReader(fin4)
    to_db4 = [(i['id'].decode('utf-8'), i['key'].decode('utf-8'), i['value'].decode('utf-8'), i['type'].decode('utf-8')) for i in dict4]

with open('ways_nodes.csv','rb') as fin5:
    dict5 = csv.DictReader(fin5)
    to_db5 = [(i['id'].decode('utf-8'), i['node_id'].decode('utf-8'), i['position'].decode('utf-8')) for i in dict5]
    
conn.commit()


# ## Inserting the formatted data into created tables

# In[461]:

# insert formatted data to dictionary/tables
cur.executemany("INSERT INTO nodes (id, lat, lon, user, uid, version, changeset, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?);", to_db1)
cur.executemany("INSERT INTO nodes_tags (id, key, value, type) VALUES (?, ?, ?, ?);", to_db2)
cur.executemany("INSERT INTO ways (id, user, uid, version, changeset, timestamp) VALUES (?, ?, ?, ?, ?, ?);", to_db3)
cur.executemany("INSERT INTO ways_tags (id, key, value, type) VALUES (?, ?, ?, ?);", to_db4)
cur.executemany("INSERT INTO ways_nodes (id, node_id, position) VALUES (?, ?, ?);", to_db5)

conn.commit()


# In[462]:

conn.close()


# ## Creating & Appending Tables using Pandas Library
# 
# #### https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.to_sql.html
