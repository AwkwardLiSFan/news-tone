# program to print out the data in the .json file
import json

with open('articleData_telegraph.json', encoding='utf-8') as json_data:
    jsonData = json.load(json_data)

# converts json to Newline Delimited JSON
result = [json.dump(record, sys.stdout, indent=2, ensure_ascii=False) for record in jsonData]
print(len(jsonData))

# output the data
json.dump(jsonData, sys.stdout, indent=2, ensure_ascii=False)
