#!/usr/bin/env python3
'''handle database for api server'''

import os
import json
from urllib.parse import unquote

GEO_DATA = os.path.abspath('src/in_geo1.json')

def load_database():
    '''load  indian cities pincodes and GEO coords'''
    with open(GEO_DATA, "r") as geo_file:
        geo_dict = json.load(geo_file)
    return geo_dict

GEO_DICT = load_database()

def create_response_body(req_query):
    '''returns response body'''
    print(req_query)
    query = unquote(req_query.title())
    if not query:
        return "check the entered station code"
    fetched = GEO_DICT.get(query, False) or  "NA"
    print(json.dumps({query:fetched}))
    return json.dumps({query:fetched})
