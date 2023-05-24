import json
from datetime import datetime as dt

today = dt.today().strftime('%H%M_%d-%m-%Y')

def make_json(input, output):
    json_formatted_str = json.dumps(input, indent=2)

    filename = f'data/{output}{today}.json'
    
    with open(filename, "w") as outfile:
        outfile.write(json_formatted_str)

    print(f'Printed out {len(input)} elements to {filename}')
