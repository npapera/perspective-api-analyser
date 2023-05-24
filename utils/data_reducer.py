import json
from datetime import datetime as dt
from iteration_utilities import unique_everseen


today = dt.today().strftime('%H%M_%d-%m-%Y')
batchId = "B1-SS1"
batchFileName = f"{batchId}_DT100"
fixDir = f"data/s2/prep/{batchId}/out/fix/FIX_{batchFileName}_0314_22-05-2023.json"
distDir = f"data/s2/prep/{batchId}/out/fix/REDFIX_{batchFileName}_{today}.json"

def check_errors(err_File = False, fix_File = False):
    fixDataList = []
    fixFile = open(fixDir, "r")
    fixData = fixFile.readlines()
    for line in fixData:
        fixDataList.append(line.strip())

    fixDataList = list(unique_everseen(fixDataList))
    print(len(fixDataList))
    write_data(fixDataList, distDir)
    
def write_data(input, output):
    with open(output, "w") as outfile:
        for i in range(len(input)):
            outfile.write(input[i])
            outfile.write('\n')
    print(f'Printed out {len(input)} elements to {output}')

check_errors(fix_File=True)