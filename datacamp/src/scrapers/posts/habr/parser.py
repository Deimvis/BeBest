from src.scrapers.parser_base import ParserBase, ParserBaserMeta


class HabrPostsParser(ParserBase, metaclass=ParserBaserMeta):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.article_tag = self.soup.select_one('article')

    def parse_title(self):
        return self.article_tag.select_one('[class*="tm-title"]').text.strip()

    def parse_publish_datetime(self):
        return self.article_tag.select_one('[class="tm-article-datetime-published"]').select_one('time')['datetime']

    def parse_views(self):
        return self.article_tag.select_one('[class="tm-icon-counter__value"]').text.strip()

    def parse_starting_text(self):
        return self.article_tag.select_one('[id="post-content-body"]').text.strip()[:64]

    def parse_reading_time(self):
        return self.article_tag.select_one('span[class="tm-article-reading-time__label"]').text.strip()

    def parse_author_username(self):
        author_username_tag = self.article_tag.select_one('a[class="tm-user-info__username"]')
        if author_username_tag is not None:
            return author_username_tag.text.strip()

    def parse_complexity(self):
        complexity_tag = self.article_tag.select_one('[class="tm-article-complexity__label"]')
        if complexity_tag is not None:
            return complexity_tag.text.strip()

    def parse_hubs(self):
        hubs = []
        info_tags = self.article_tag.select_one('[class="tm-publication-hubs"]').select('a')
        for info_tag in info_tags:
            if '/hubs/' in info_tag['href']:
                hubs.append(info_tag.text)
        return hubs

    def parse_tags(self):
        tags = []
        lists = self.article_tag.select_one('[class="tm-article-presenter__meta"]').select('[class^="tm-separated-list "]')
        for list_ in lists:
            list_title = list_.select_one('[class="tm-separated-list__title"]').text.strip()
            match list_title:
                case 'Теги:':
                    tags = [a_tag.text for a_tag in list_.select('a')]
        return tags
