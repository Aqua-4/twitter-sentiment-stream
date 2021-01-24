import json
import pandas as pd
import yaml
import re
from datetime import datetime, timedelta
import os
from insight_utils import *


CONFIG = yaml.safe_load(open('config.yaml', "r", encoding='utf-8'))
queries = yaml.safe_load(open('queries.yaml', "r", encoding='utf-8'))
url = CONFIG.get('variables')['connection_string']
engine = create_engine(url)


# drop_duplicate_query = """
# DELETE FROM tweet_dump
#     WHERE rowid NOT IN
#     (
#     SELECT MIN(rowid)
#     FROM tweet_dump
#     GROUP BY txt
#     )
# """
# drop_duplicate_query = queries.get('drop_duplicate_query').get('query')
# engine.execute(drop_duplicate_query)


class Methods:

    def __get_engine(self, FormHandler):
        return FormHandler.connect_engine(self)

    def get_meta(self):
        return CONFIG['meta']

    def get_data(self):
        # read csv from data folder
        path = os.path.join("static", "data", "data.csv")
        df = pd.read_csv(path)
        # return csv JSON
        return df.to_json(orient="records")

    def get_donut(self):
        # return json.dumps({'img': get_donut_bs64()})
        return json.dumps(get_donut_json())

    def get_pie(self):
        return json.dumps({'img': get_pie_bs64()})
