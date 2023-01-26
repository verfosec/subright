import json

import requests
from colorama import Fore as colorize


def crtsh_enumerator(domain: str, silent: bool):
    subdomains = []
    BASE_URL = f'https://crt.sh/?q={domain}&output=json'

    response = requests.get(BASE_URL)
    json_data = json.loads(response.text)

    if response.status_code != 200:
        if silent is not True:
            print(colorize.RED+'[-]', colorize.LIGHTRED_EX+BASE_URL,
                  '\tStatus code:', response.status_code)
        return subdomains

    for jd in json_data:
        subdomains.extend(jd['common_name'].split())
        subdomains.extend(jd['name_value'].split())

    # Convert to set to remove repeated values then convert it to list
    return list(set(subdomains))
