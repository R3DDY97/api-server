#!/usr/bin/env python3
'''handle database for api server'''

import os
import json
import sqlite3
from urllib.parse import unquote

GEO_DATA = os.path.abspath('src/in_geo1.json')
GEO_DB = os.path.abspath('src/geo_data.db')

def load_database():
    '''load  indian cities pincodes and GEO coords'''
    with open(GEO_DATA, "r") as geo_file:
        geo_dict = json.load(geo_file)
    return geo_dict

GEO_DICT = load_database()

# def create_response_body(req_query):
#     '''returns response body'''
#     print(req_query)
#     query = unquote(req_query.title())
#     if not query:
#         return "check the entered station code"
#     fetched = GEO_DICT.get(query, False) or  "NA"
#     print(json.dumps({query:fetched}))
#     return json.dumps({query:fetched})

def create_connection():
    '''return sqlite3 db cursor obj '''
    con = sqlite3.connect(GEO_DB)
    cur = con.cursor()
    return cur

CUR = create_connection()

def create_response_body(req_query):
    '''returns  query related response JS0N'''
    CUR.execute("SELECT * FROM geo WHERE city LIKE '%{}%'".format(unquote(req_query)))
    response_list = CUR.fetchall()
    response_dict = {i[0]:{"city": i[0], "state": i[1], "pincode": i[2],
                           "latitude": i[3], "longitude": i[4]} for i in response_list}
    return json.dumps(response_dict)
    # with open("{}.json".format(req_query), "w+") as res:
    #     json.dump(response_dict, res)
    # res_json = os.path.abspath("{}.json".format(req_query))
    # return res_json
