import json
import sys
from pkgutil import simplegeneric

@simplegeneric
def get_items(obj):
    while False:
        yield None  # no items

@get_items.register(dict)
def _(obj):
    return obj.items()  # json object

@get_items.register(list)
def _(obj):
    return enumerate(obj) # json string

def strip_whitespace(json_data):
    for key, value in get_items(json_data):
        if hasattr(value, 'strip'): # json string
            json_data[key] = value.strip()
        else:
            strip_whitespace(value) # recursive call

with open('independent/articleData_Independent.json', encoding='utf-8') as json_data:
    jsonData = json.load(json_data)

# converts json to Newline Delimited JSON
# result = [json.dump(record, sys.stdout, indent=2, ensure_ascii=False) for record in jsonData]

# stripping data of extra newlines
strip_whitespace(jsonData)

print(jsonData)
#json.dump(jsonData, sys.stdout, indent=2, ensure_ascii=False)
