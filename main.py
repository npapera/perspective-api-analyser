import json
import os
import time
import logging

from dotenv import load_dotenv
from googleapiclient import discovery
from utils.json_writer import make_json

load_dotenv()
DEVELOPER_KEY = os.getenv("API_KEY")
minIndex = 0
maxIndex = 2992
totalIndex = maxIndex - minIndex
batchId = 'B1-SS1'
batchFile = f'PANS_{batchId}_DT{totalIndex}_{minIndex}-{maxIndex}'
outputDir = f'analysis/{batchFile}'

logging.basicConfig(filename=f'tmp/{batchFile}.log',
                    level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger=logging.getLogger(__name__)

def commentAnalyser(text, cansIndex):

    jsonItem = {}
    jsonItem["textOriginal"] = text
    jsonItem["Index"] = cansIndex

    try:
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
        toxicScore = holdThis['attributeScores']['TOXICITY']['summaryScore']['value']
        sevToxicScore = holdThis['attributeScores']['SEVERE_TOXICITY']['summaryScore']['value']
        idAttackScore = holdThis['attributeScores']['IDENTITY_ATTACK']['summaryScore']['value']
        insultScore = holdThis['attributeScores']['INSULT']['summaryScore']['value']
        profanityScore = holdThis['attributeScores']['PROFANITY']['summaryScore']['value']
        threatScore = holdThis['attributeScores']['THREAT']['summaryScore']['value']

        jsonItem["TOXICITY"] = toxicScore
        jsonItem["SEVERE_TOXICITY"] = sevToxicScore
        jsonItem["TOXICITY"] = idAttackScore
        jsonItem["INSULT"] = insultScore
        jsonItem["PROFANITY"] = profanityScore
        jsonItem["THREAT"] = threatScore

    except Exception as e:
        print(f"Unexpected Error: {e}")
        logger.error(e)

    return jsonItem

def main():
    to_json = False
    file = open('data/analysis/CANS_B1-SS1_DT100_2250_24-05-2023.json')
    data = json.load(file)
    all_data = []
    for i in range(minIndex, maxIndex):
        logger.info(f"Processing comment at Index: {i}")
        all_data.append(commentAnalyser(data[i]['textOriginal'], i))
        time.sleep(1)
        print(f"Data analysed by perspective at Index: {i}")
        logger.info(f"Finished analysing comment at Index: {i}")

    if to_json:
        make_json(all_data, outputDir)

if __name__ == "__main__":
    main()