import json
from datetime import datetime as dt

today = dt.today().strftime('%H%M_%d-%m-%Y')
batchId = "B1-SS1"
batchFileName = f"{batchId}_DT100"
inputDir = f"data/s2/prep/{batchId}/out/output.json"
refDir = f"data/s2/B1-SS1_data100_2343_16-05-2023.json"
negSentOut = f"data/analysis/NS_{batchFileName}_{today}.json"
outputDir = f"data/analysis/PANS_{batchFileName}_{today}.json"

def check_errors(negSent_File = False, output_File = False):
    inputFile = open(inputDir, 'r')
    inputData = inputFile.readlines()
    jsonList = []
    inputList = []
    for line in inputData:
        temp = json.loads(line)
        if 'ErrorCode' not in line:
            if temp['Sentiment'] == 'NEGATIVE':
                jsonList.append(temp)
    
    for i in jsonList:
        temp = {}
        temp["Index"] = i["Line"]
        temp["Sentiment"] = i["Sentiment"]
        temp["SentimentScore"] = i["SentimentScore"]
        inputList.append(temp)

    if negSent_File:
        write_json(inputList, negSentOut)

    outputList = []
    refFile = open(refDir, "r")
    refData = json.load(refFile)
    for i in inputList:
        temp2 = refData[i["Index"]]
        temp2["Index"] = i["Index"]
        temp2["Sentiment"] = i["Sentiment"]
        temp2["SentimentScore"] = i["SentimentScore"]
        outputList.append(temp2)

    if output_File:
        write_json(outputList, outputDir)
    
def write_data(input, output):
    with open(output, "w") as outfile:
        for i in range(len(input)):
            outfile.write(input[i])
            outfile.write('\n')
    print(f'Printed out {len(input)} elements to {output}')

def write_json(input, output):
    json_formatted_str = json.dumps(input, indent=2)
    with open(output, "w") as outfile:
        outfile.write(json_formatted_str)
    print(f'Printed out {len(input)} elements to {output}')

check_errors(negSent_File = True, output_File = True)