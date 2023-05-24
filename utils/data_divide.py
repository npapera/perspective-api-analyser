import os
import math

from datetime import datetime as dt

today = dt.today().strftime('%H%M_%d-%m-%Y')
batchId = "B1-SS1"
batchFileName = f"{batchId}_DT100"
inputDir = f"data/s2/prep/{batchId}/B1-SS1_DT100_2331_21-05-2023.json"
parentDir = f"C:/Users/nerip/github/perspective-api-analyser/data/s2/prep/B1-SS1/split/"
batchDir = ""
divIndexList = []

def split_data():

    file = open(inputDir, 'r')
    lines = file.readlines()
    jsonList = []
    for line in lines:
        jsonList.append(line.strip())
    print(len(jsonList))

    divCount = 1
    jobDirCount = 1
    outputDir = f"data/s2/prep/{batchId}/split/{batchFileName}_DIV{divCount}.json"
    indexMin = 0
    indexMax = 50
    indexDiv = math.ceil(len(jsonList)/50)
    for i in range(0, indexDiv):
        tempList = []
        if len(jsonList)-(indexMax+50*i) >= 0:
            tempList = jsonList[indexMin+50*i:indexMax+50*i+1]
        else:
            tempList = jsonList[indexMin+50*i:len(jsonList)+1]

        if i%25==0:
            batchDir = f"J{jobDirCount}"
            path = os.path.join(parentDir, batchDir)
            os.mkdir(path)
            print(f'\nCreated new folder: {batchDir}')
            jobDirCount+=1

        outputDir = f"data/s2/prep/{batchId}/split/{batchDir}/{batchFileName}_DIV{divCount}.json"
        write_data(tempList, outputDir)

        divCount+=1

def write_data(input, output):
    with open(output, "w") as outfile:
        for i in range(len(input)):
            outfile.write(input[i])
            outfile.write('\n')
    print(f'Printed out {len(input)} elements to {output}')

split_data()