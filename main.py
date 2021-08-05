import json, os, requests, sys

ENCODING = 'utf-8'
ENTERPRISE_ATTACK_JSON_FILE = 'enterprise-attack.json'

def download_enterprise_attack_json():
    ENTERPRISE_ATTACK_JSON_URL = 'https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json'
    enterprise_attack_json = requests.get(ENTERPRISE_ATTACK_JSON_URL).json()

    with open(ENTERPRISE_ATTACK_JSON_FILE, 'w', encoding=ENCODING) as f:
        json.dump(enterprise_attack_json, f, ensure_ascii=False, indent=4)

def get_techniques(term):
    if (not os.path.isfile(ENTERPRISE_ATTACK_JSON_FILE)):
        download_enterprise_attack_json()

    techniques = []

    with open(ENTERPRISE_ATTACK_JSON_FILE, encoding=ENCODING) as f:
        enterprise_attack_json = json.load(f)

        for data in enterprise_attack_json.get('objects'):
            is_attack_pattern = data.get('type') == 'attack-pattern'
            is_deprecated = data.get('x_mitre_deprecated', False)
            is_in_description = term in data.get('description', '')
            
            external_references = data.get('external_references', [{}])[0]
            external_url = external_references.get('url', '')
            is_technique = 'techniques' in external_url

            if (is_attack_pattern and not is_deprecated and is_in_description and is_technique):
                techniques.append({
                    'id': external_references.get('external_id', ''),
                    'name': data.get('name'),
                    'url': external_url,
                })

    techniques = sorted(techniques, key=lambda t: t.get('id'))

    for t in techniques:
        print(f"[ {t.get('id').ljust(9, ' ')} ] {t.get('name').ljust(75, ' ')} ({t.get('url')})")

get_techniques(sys.argv[1])