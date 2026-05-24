import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


KEYWORDS = ['дизайн', 'фото', 'web', 'python']

URL = 'https://habr.com/ru/articles/'

HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/120.0.0.0 Safari/537.36'
    ),
    'Accept-Language': 'ru-RU,ru;q=0.9,en;q=0.8',
}


def fetch_page(url: str) -> str:
    response = requests.get(url, headers=HEADERS, timeout=15)
    response.raise_for_status()
    return response.text


def contains_keyword(text: str, keywords: list[str]) -> bool:
    lower_text = text.lower()
    return any(keyword.lower() in lower_text for keyword in keywords)


def parse_articles(html: str) -> list[dict]:
    soup = BeautifulSoup(html, 'html.parser')
    articles = []

    for article_tag in soup.find_all('article'):
        title_tag = article_tag.find('h2')
        if not title_tag:
            continue
        link_tag = title_tag.find('a')
        if not link_tag:
            continue

        title = link_tag.get_text(strip=True)
        href = link_tag.get('href', '')
        full_url = urljoin(URL, href)

        time_tag = article_tag.find('time')
        date = time_tag.get_text(strip=True) if time_tag else '—'

        preview = article_tag.get_text(' ', strip=True)

        articles.append({
            'title': title,
            'url': full_url,
            'date': date,
            'preview': preview,
        })

    return articles


def main() -> None:
    try:
        html = fetch_page(URL)
    except requests.RequestException as error:
        print(f'Ошибка при загрузке страницы: {error}')
        return

    articles = parse_articles(html)
    matched = [
        article for article in articles
        if contains_keyword(article['preview'], KEYWORDS)
    ]

    if not matched:
        print('Подходящих статей не найдено.')
        return

    for article in matched:
        print(f"{article['date']} – {article['title']} – {article['url']}")


if __name__ == '__main__':
    main()