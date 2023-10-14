#!/usr/bin/env python3
# custom-iris.py
# Custom Wazuh integration script to send alerts to DFIR-IRIS

import sys
import json
import requests
from requests.auth import HTTPBasicAuth

# Function to search for and extract the "message" field
def find_message_field(data):
    if isinstance(data, dict):
        if "message" in data:
            return data["message"]
        for key, value in data.items():
            result = find_message_field(value)
            if result is not None:
                return result
    elif isinstance(data, list):
        for item in data:
            result = find_message_field(item)
            if result is not None:
                return result
    return None

# Read parameters when integration is run
alert_file = sys.argv[1]
api_key = sys.argv[2]
hook_url = sys.argv[3]

# Read the alert file
with open(alert_file) as f:
    alert_json = json.load(f)

# Extract field information
alert_id = alert_json["id"]
alert_timestamp = alert_json["timestamp"]
alert_level = alert_json["rule"]["level"]
alert_title = alert_json["rule"]["description"]
alert_description = find_message_field(alert_json["data"])
agent_name = alert_json["agent"]["name"]
agent_ip = alert_json["agent"]["ip"]
agent_id = alert_json["agent"]["id"]
rule_id = alert_json["rule"]["id"]
rule_fires = alert_json["rule"]["firedtimes"]
alert_data = alert_json["data"]
alert_message = find_message_field(alert_json["data"])

# Convert Wazuh rule levels -> IRIS severity
if(alert_level < 5):
    severity = 2
elif(alert_level >= 5 and alert_level < 7):
    severity = 3
elif(alert_level >= 7 and alert_level < 10):
    severity = 4
elif(alert_level >= 10 and alert_level < 13):
    severity = 5
elif(alert_level >= 13):
    severity = 6
else:
    severity = 1

# Generate request
# Reference: https://docs.dfir-iris.org/_static/iris_api_reference_v2.0.1.html#tag/Alerts/operation/post-case-add-alert
payload = json.dumps({
    "alert_title": alert_title,
    "alert_description": f"""Agent ID: {agent_id}
Agent IP: {agent_ip}
Agent Name: {agent_name}

Alert Details: {alert_description}
""",
    "alert_source": "Wazuh",
    "alert_source_ref": alert_id,
    "alert_source_link": "WAZUH_URL",
    "alert_severity_id": severity, 
    "alert_status_id": 2, # 'New' status
    "alert_source_event_time": alert_timestamp,
    "alert_note": "",
    "alert_tags": "wazuh," + agent_name,
    "alert_customer_id": 1, # '1' for default 'IrisInitialClient'
    "alert_source_content": alert_json # raw log
})

# Send request to IRIS
response = requests.post(hook_url, data=payload, headers={"Authorization": "Bearer " + api_key, "content-type": "application/json"})

sys.exit(0)
