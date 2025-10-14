import requests
from bs4 import BeautifulSoup

def get_data(event, context):
    endpoint = "https://u.today/search/node?keys=btc"

    response = requests.get(endpoint)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        btc_cards = soup.select("div.news__item")

        data = []

        for card in btc_cards:
            title_tag = card.find("a", class_="news__item-body")
            author_tag = card.find("a", class_="humble humble--author")
            date_tag = card.find("div", class_="humble")

            title = title_tag.get_text(strip=True) if title_tag else None
            link = title_tag["href"] if title_tag and title_tag.has_attr("href") else None
            author = author_tag.get_text(strip=True) if author_tag else None
            date = date_tag.get_text(strip=True) if date_tag else None

            data.append([title, link, author, date])

        return data
