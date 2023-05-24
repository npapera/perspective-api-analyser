import json
import os
import time

from dotenv import load_dotenv
from googleapiclient import discovery
from utils.json_writer import make_json

load_dotenv()
DEVELOPER_KEY = os.getenv("API_KEY")

outputDir = 'test'

def commentAnalyser(text, to_json=False):
    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=DEVELOPER_KEY,
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_discovery=False,
    )

    analyze_request = {
        'comment': { 'text': text },
        'requestedAttributes': {
            'TOXICITY': {},
            'SEVERE_TOXICITY': {},
            'IDENTITY_ATTACK': {},
            'INSULT': {},
            'PROFANITY': {},
            'THREAT': {},
        }
    }

    response = client.comments().analyze(body=analyze_request).execute()

    holdThis = response
    # print(response)
    toxicScore = holdThis['attributeScores']['TOXICITY']['summaryScore']['value']
    sevToxicScore = holdThis['attributeScores']['SEVERE_TOXICITY']['summaryScore']['value']
    idAttackScore = holdThis['attributeScores']['IDENTITY_ATTACK']['summaryScore']['value']
    insultScore = holdThis['attributeScores']['INSULT']['summaryScore']['value']
    profanityScore = holdThis['attributeScores']['PROFANITY']['summaryScore']['value']
    threatScore = holdThis['attributeScores']['THREAT']['summaryScore']['value']

    
    
    if to_json:
        make_json(response, outputDir)

def main():
    file = open('data\s2\-11YXFg2TbQ_1429_12-05-2023.json')
    data = json.load(file)
    for i in range(0,10):
        commentAnalyser(data[i]['textOriginal'], to_json=False)
        print()
        time.sleep(2)

if __name__ == "__main__":
    main()