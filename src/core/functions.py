import json
from typing import get_type_hints


def load_json(file_name):
    with open(file_name.strip(), 'r', encoding='utf-8') as file:
        return json.load(file)

def get_type_hints_without_underscore(cls):
    annotations = get_type_hints(cls)
    result = {}
    for key, value in annotations.items():
        start_index = 0
        if key[0]=='_':
            start_index = 1
        result[key[start_index:]] = value
    return result