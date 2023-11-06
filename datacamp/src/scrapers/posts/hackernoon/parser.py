from src.scrapers.parser_base import ParserBase, ParserBaserMeta


class HackernoonArticleParser(ParserBase, metaclass=ParserBaserMeta):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.header = self.soup.select_one('section')

    def parse_author_username(self):
        return self.header.select_one('a[href*="hackernoon.com/u"]').text.strip()

    def parse_publish_date(self):
        return self.header.select_one('a[href*="hackernoon.com/archives"]').text.strip()

    def parse_starting_text(self):
        return self.soup.select_one('article').text[:64]

    def parse_tags(self):
        return [a_tag.text for a_tag in self.header.select('a[href*="hackernoon.com/tagged/"]')]

    def parse_title(self):
        return self.header.select_one('h1').text.strip()
