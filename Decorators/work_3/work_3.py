import os
import time
import datetime
from functools import wraps
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


KEYWORDS = ['дизайн', 'фото', 'web', 'python']
PARSER = 'html.parser'
URL = 'https://habr.com/ru/articles/'
LOG_FILE = 'habr_parser.log'

HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/120.0.0.0 Safari/537.36'
    ),
    'Accept-Language': 'ru-RU,ru;q=0.9,en;q=0.8',
}


def logger(path):

    def __logger(old_function):
        @wraps(old_function)
        def new_function(*args, **kwargs):
            result = old_function(*args, **kwargs)

            def truncate(obj):
                s = repr(obj)
                return s if len(s) <= 300 else s[:300] + '... [truncated]'

            log_line = (
                f'{datetime.datetime.now()} | '
                f'{old_function.__name__} | '
                f'args: {truncate(args)}, kwargs: {truncate(kwargs)} | '
                f'result: {truncate(result)}\n'
            )

            with open(path, 'a', encoding='utf-8') as log_file:
                log_file.write(log_line)

            return result

        return new_function

    return __logger



@logger(LOG_FILE)
def fetch_page(url: str) -> str:
    response = requests.get(url, headers=HEADERS, timeout=15)
    response.raise_for_status()
    return response.text


@logger(LOG_FILE)
def contains_keyword(text: str, keywords: list[str]) -> bool:
    lower_text = text.lower()
    return any(keyword.lower() in lower_text for keyword in keywords)


@logger(LOG_FILE)
def parse_articles(html: str) -> list[dict]:
    soup = BeautifulSoup(html, PARSER)
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


@logger(LOG_FILE)
def fetch_article_full_text(url: str) -> str:
    html = fetch_page(url)
    soup = BeautifulSoup(html, PARSER)
    content_block = (
            soup.find('div', class_='tm-article-presenter__content')
            or soup.find('div', class_='article-formatted-body')
            or soup.find('div', class_='formatted')
            or soup.find('div', class_='content')
    )

    if content_block:
        return content_block.get_text(' ', strip=True)

    article = soup.find('article')
    return article.get_text(' ', strip=True) if article else ''


@logger(LOG_FILE)
def main() -> None:
    print('Загружаю список статей с Хабра')
    try:
        html = fetch_page(URL)
    except requests.RequestException as error:
        print(f'Ошибка при загрузке страницы: {error}')
        return

    articles = parse_articles(html)
    print(f'Всего статей на странице: {len(articles)}')
    print(f'Ключевые слова для поиска: {KEYWORDS}\n')

    matched = []

    for i, article in enumerate(articles, start=1):
        print(f'[{i}/{len(articles)}] Проверяю: {article["title"][:50]}...')

        if contains_keyword(article['preview'], KEYWORDS):
            matched.append(article)
            print('найдено в preview')
            continue

        try:
            full_text = fetch_article_full_text(article['url'])
            if contains_keyword(full_text, KEYWORDS):
                matched.append(article)
                print('найдено в полном тексте статьи')
            else:
                print('ключевых слов нет')
        except requests.RequestException as error:
            print(f'не удалось загрузить статью: {error}')

    print('\n' + '=' * 60)
    if not matched:
        print('Подходящих статей не найдено.')
        return

    print(f'Найдено подходящих статей: {len(matched)}\n')
    for article in matched:
        print(f"{article['date']} – {article['title']} – {article['url']}")


if __name__ == '__main__':
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)

    main()