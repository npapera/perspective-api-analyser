import json
from datetime import datetime as dt

today = dt.today().strftime('%H%M_%d-%m-%Y')
batchId = "B1-SS10"
batchFileName = f"{batchId}_DT100"
outputDir = f"s2/prep/{batchId}/{batchFileName}"

def transform():
    file = open('data\s2\B1-SS10_data100_2125_17-05-2023.json')
    data = json.load(file)

    jsonList = []
    for i in data:
        jsonElem = {"Text": "", "LanguageCode": "en"}
        text = i['textOriginal']
        text = text.replace("\n", "")
        text = text.replace("\r", "")
        text = text.replace("\t", "")
        jsonElem["Text"] = text
        jsonList.append(jsonElem)
    
    write_data(jsonList, outputDir)


def write_data(dataIn, outDir):

    filename = f'data/{outDir}_{today}.json'
    
    with open(filename, "w") as outfile:
        for i in dataIn:
            outfile.write(json.dumps(i))
            outfile.write('\n')

    print(f'Printed out {len(dataIn)} elements to {filename}')

transform()