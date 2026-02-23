import requests
from bs4 import BeautifulSoup
import re

def scrape_clean_job_text(url: str, max_chars: int = 3000) -> str:
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return f"Error: Status code {response.status_code}"

        soup = BeautifulSoup(response.content, 'html.parser')

        for junk in soup(["script", "style", "nav", "footer", "header", "aside", "iframe"]):
            junk.decompose()

        text = soup.get_text(separator=' ', strip=True)
        text = re.sub(r'\s+', ' ', text)

        return text[:max_chars]

    except Exception as e:
        return f"Scraping Error: {str(e)}"