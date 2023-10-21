# Wazuh-IRIS-integration
![Static Badge](https://img.shields.io/badge/SIEM-Integration-%230000FF) ![Static Badge](https://img.shields.io/badge/SECENG-Cloud-%23800080%20) ![Static Badge](https://img.shields.io/badge/LANGUAGE-Python-%23008000)
Simple Wazuh integration to send alerts to IRIS, as originally described by [nateuribe](https://github.com/nateuribe) in [https://nateuribe.tech/blog/foss-soc/](https://nateuribe.tech/blog/foss-soc/). [nateuribe](https://github.com/nateuribe) deserves all credit so please go and star their repo and follow them. 

## The forked version you are reading updates IRIS alert fields to include alternative information

Main changes are as follows:
- Wazuh Alert Title name now populates to the Iris Alert Title
- Added function to find "message" field in alert JSON, this is used in the API call to add the information to the Iris Alert Description
- Agent and event information now map to the Iris Alert Description for easier visibility



## Requirements
- [Wazuh](https://github.com/wazuh/wazuh) Server
- [IRIS](https://github.com/dfir-iris/iris-web)
- Python
- python-requests

## Installation
```
git clone https://github.com/chadhardcastle/Wazuh-IRIS-integration.git
cd Wazuh-IRIS-integration/
cp custom-iris.py /var/ossec/integrations/custom-iris.py
chmod 750 /var/ossec/integrations/custom-iris.py
chown root:wazuh /var/ossec/integrations/custom-iris.py
```
Add the following snippet into the `/var/ossec/etc/ossec.conf` config file:
```xml
<!--
... Rest of config
-->

<!-- IRIS integration -->
<integration>
    <name>custom-iris.py</name>
    <hook_url>http://IRIS-BASE-URL:8000/alerts/add</hook_url>
    <level>7</level>
    <api_key>APIKEY</api_key>
    <alert_format>json</alert_format>
</integration>
```
Adjust `<hook_url>` and `<api_key>` to your environment, and change `<level>` to the desired threshold for alerts.

Restart the `wazuh-manager` service after modifying the above settings

```
systemctl restart wazuh-manager
```

The IRIS API can be found in the Dashboard under **My Settings**

## Configuration
The script comes preconfigured with a basic payload to create new IRIS alerts.
Use the Alerts API reference to modify this at will (https://docs.dfir-iris.org/_static/iris_api_reference_v2.0.1.html#tag/Alerts/operation/post-case-add-alert).

Here are some notable values you may change:

`alert_source_link` - URL from where the alert came from (Wazuh in this instance)

`alert_note` - Note or comment to add to each alert

`alert_customer_id` - Alerts in IRIS get assigned to "customers"; this is the ID of the customer for which the alerts pertains to.

## Examples

Windows Defender `Mimikatz` detection Alert
![image](https://github.com/chadhardcastle/Wazuh-IRIS-integration/assets/110081755/126a0220-2c33-4715-bb2a-3739d318ef45)

Informational Docker Error Alert
![image](https://github.com/chadhardcastle/Wazuh-IRIS-integration/assets/110081755/ea682b1c-6ed1-4d0e-a8f5-a68ed9671f85)
