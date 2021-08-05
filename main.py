import json, requests

ENTERPRISE_ATTACK_JSON_FILE = 'enterprise-attack.json'

def download_enterprise_attack_json():
    ENTERPRISE_ATTACK_JSON_URL = 'https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json'
    enterprise_attack_json = requests.get(ENTERPRISE_ATTACK_JSON_URL).json()

    with open(ENTERPRISE_ATTACK_JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(enterprise_attack_json, f, ensure_ascii=False, indent=4)

download_enterprise_attack_json()