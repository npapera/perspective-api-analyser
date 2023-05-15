import json
import os

from dotenv import load_dotenv
from googleapiclient import discovery

load_dotenv()
DEVELOPER_KEY = os.getenv("API_KEY")

client = discovery.build(
  "commentanalyzer",
  "v1alpha1",
  developerKey=DEVELOPER_KEY,
  discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
  static_discovery=False,
)

analyze_request = {
  'comment': { 'text': 'friendly greetings from python' },
  'requestedAttributes': {'TOXICITY': {}}
}

response = client.comments().analyze(body=analyze_request).execute()
print(json.dumps(response, indent=2))