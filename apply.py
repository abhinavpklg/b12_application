import os
import json
import hmac
import hashlib
import requests
import datetime

CANDIDATE_NAME = "Abhinav Manoj Pandey" 
CANDIDATE_EMAIL = "abhinavp.us@gmail.com"
RESUME_LINK = "https://drive.google.com/file/d/1rSorv-o7e-6Jub63Ah5yHyPuNOaCcv3q/view?usp=sharing"

# GitHub Action secrets for the Run Link
server_url = os.getenv('GITHUB_SERVER_URL')
repo = os.getenv('GITHUB_REPOSITORY')
run_id = os.getenv('GITHUB_RUN_ID')
action_run_link = f"{server_url}/{repo}/actions/runs/{run_id}"
repo_link = f"{server_url}/{repo}"

# Constructing the Payload
payload_dict = {
    "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z"),
    "name": CANDIDATE_NAME,
    "email": CANDIDATE_EMAIL,
    "resume_link": RESUME_LINK,
    "repository_link": repo_link,
    "action_run_link": action_run_link
}

# Canonicalize JSON, Must be UTF-8, Keys sorted, No extra whitespace
payload_json_str = json.dumps(payload_dict, sort_keys=True, separators=(',', ':'))
payload_bytes = payload_json_str.encode('utf-8')

#Signing the Payload
secret = b"abhinav_b12_application"
signature = hmac.new(secret, payload_bytes, hashlib.sha256).hexdigest()

#Sending Request
url = "https://b12.io/apply/submission"
headers = {
    "Content-Type": "application/json",
    "X-Signature-256": f"sha256={signature}"
}

print(f"Sending payload: {payload_json_str}")
print(f"Signature: {signature}")

try:
    response = requests.post(url, data=payload_bytes, headers=headers)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")
    
    if response.status_code == 200:
        print("\nSUCCESS! Here is your receipt:")
        print(response.json().get('receipt'))
    else:
        print("Submission failed.")
        exit(1)

except Exception as e:
    print(f"An error occurred: {e}")
    exit(1)