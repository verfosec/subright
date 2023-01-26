import re

import requests
from bs4 import BeautifulSoup
from colorama import Fore as colorize

from user_agents import random_user_agent


def google_enumerator(domain: str, silent: bool):
    subdomains = []
    BASE_ENGINE_URL = 'https://www.google.com/search'
    query = f'site:*.{domain}'
    request_headers = {'Host': 'www.google.com',
                       'User-Agent': random_user_agent()}

    while len(subdomains) <= 32:  # Google has a query limit
        engine_url = f'{BASE_ENGINE_URL}?q={query}'
        response = requests.get(url=engine_url, headers=request_headers)
        if response.status_code != 200:
            if silent:
                print(colorize.RED+'[-]', colorize.LIGHTRED_EX+engine_url,
                      '\tStatus code:', response.status_code)
            break

        soup = BeautifulSoup(response.text, "html.parser")
        span_tags_value = [i.get_text() for i in soup.find_all('span')]

        clear_value = None
        for i in span_tags_value:
            if re.match(f'.*{domain}', i):
                clear_value = i.split()[0]
                if clear_value not in subdomains:
                    query += f'%20-{clear_value}'
                    subdomains.append(clear_value)
        if clear_value is None:
            break

    page_number = 0
    while True:
        engine_url = f'{BASE_ENGINE_URL}?q={query}&start={page_number}'
        if response.status_code != 200:
            if silent:
                print(colorize.RED+'[-]', colorize.LIGHTRED_EX+engine_url,
                      '\tStatus code:', response.status_code)
            break

        soup = BeautifulSoup(response.text, "html.parser")
        span_tags_value = [i.get_text() for i in soup.find_all('span')]

        clear_value = None
        for i in span_tags_value:
            if re.match(f'.*{domain}', i):
                clear_value = i.split()[0]
                if clear_value not in subdomains:
                    subdomains.append(clear_value)
        if clear_value is None:
            break

        page_number += 10

    # Convert to set to remove repeated values then convert it to list
    return list(set(subdomains))


print(google_enumerator('sony.com', True))
