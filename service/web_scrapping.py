import requests
import logging
from bs4 import BeautifulSoup

def fetch_content(url, selectors):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        content = []
        for selector in selectors:
            elements = soup.select(selector)
            for element in elements:
                text = element.get_text(strip=True)
                if text:
                    content.append(text)
        return '. '.join(content) if content else ''

    except requests.exceptions.RequestException as e:
        logging.info(f"[FETCH_URL][ERROR]: url={url}, {e}")


selectors = ['.detail__summary', '.detail__content']
