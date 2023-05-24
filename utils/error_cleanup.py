import json
from datetime import datetime as dt

today = dt.today().strftime('%H%M_%d-%m-%Y')
batchId = "B1-SS1"
batchFileName = f"{batchId}_DT100"
inputDir = f"data/s2/prep/{batchId}/out/output.json"
refDir = f"data/s2/prep/{batchId}/B1-SS1_DT100_2331_21-05-2023.json"
errOut = f"data/s2/prep/{batchId}/out/errors/ERR_{batchFileName}_{today}.json"
fixOut = f"data/s2/prep/{batchId}/out/fix/FIX_{batchFileName}_{today}.json"

def check_errors(err_File = False, fix_File = False):
    errFile = open(inputDir, 'r')
    errData = errFile.readlines()
    jsonList = []
    errIndexList = []
    for line in errData:
        if "ErrorCode" in line:
            jsonList.append(json.loads(line))
    
    for i in jsonList:
        errIndexList.append(i["Line"])

    if err_File:
        write_data(jsonList, errOut)

    jsonList = []
    fixDataList = []
    refFile = open(refDir, "r")
    refData = refFile.readlines()
    for line in refData:
        jsonList.append(line.strip())
    
    for i in errIndexList:
        fixDataList.append(jsonList[i])

    if fix_File:
        write_data(fixDataList, fixOut)

    # write_data(jsonList, outputDir)
    
def write_data(input, output):
    with open(output, "w") as outfile:
        for i in range(len(input)):
            outfile.write(input[i])
            outfile.write('\n')
    print(f'Printed out {len(input)} elements to {output}')

check_errors(fix_File=True)