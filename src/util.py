import json

def load_json_file(filepath):
    with open(filepath) as f:
        for row in json.load(f):
            yield row

def create_user_table(conn):
    pass