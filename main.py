import requests
from bs4 import BeautifulSoup

KEYWORDS = ['дизайн', 'фото', 'web', 'python', 'программирование']


class GetArticlesFromHabr:

    def __init__(self, KEYWORDS):
        self.KEYWORDS = KEYWORDS

    def get_articles_list(self):
        target_keywords = set([word.capitalize() for word in KEYWORDS])
        response = requests.get('https://habr.com/ru/all/')
        bs = BeautifulSoup(response.text, 'html.parser')
        class_element = bs.find_all('article', {'class': 'post'})
        for article in class_element:
            hubs = set(map(lambda hub: hub.text, article.find_all('a', {'class': 'hub-link'})))
            title_el = article.find('a', {'class': 'post__title_link'})
            title = title_el.text
            title_list = title.split(' ')
            word_in_title = set([word.capitalize().strip('.,;:?!"()') for word in title_list])
            preview_text = article.find('div', {'class': 'post__text'}).text
            preview_list = preview_text.split(' ')
            preview_words = set([word.capitalize().strip('.,;:!?"()') for word in preview_list])
            if target_keywords.intersection(hubs) or target_keywords.intersection(word_in_title)\
                    or target_keywords.intersection(preview_words):
                time_el = article.find('span', {'class': 'post__time'})
                time = time_el.text
                self.title_link = title_el.attrs.get('href')
                print(f'Дата публикации: {time}; название статьи: {title}; ссылка: {self.title_link}')
                self.get_article_sentences_with_keywords()

    def get_article_sentences_with_keywords(self):
        article_text_link = requests.get(self.title_link)
        soup = BeautifulSoup(article_text_link.text, 'html.parser')
        article_text_elem = soup.find('div', {'id': 'post-content-body'})
        article_text = article_text_elem.text.split('.')
        for sentence in article_text:
            for word in sentence.strip().split():
                result = word.strip('()?",').lower()
                for tag in KEYWORDS:
                    if result == tag.lower():
                        print(f'Найденное совпадение в статье:\n{sentence}')


main = GetArticlesFromHabr(KEYWORDS)
main.get_articles_list()
