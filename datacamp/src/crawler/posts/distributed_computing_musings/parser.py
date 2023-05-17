import re
from src.crawler.parser_base import ParserBase, ParserBaserMeta


class Parser(ParserBase, metaclass=ParserBaserMeta):

    def parse_title(self):
        return self.soup.select('div[class="entry-container"] [class="entry-title"]')[0].text

    def parse_publish_date(self):
        return self.soup.select('div[class="entry-container"] [class="entry-date published"]')[0].text

    def parse_tags(self):
        return [tag.text for tag in self.soup.select('div[class="entry-container"] [class="post-categories"] li')]

    def parse_starting_text(self):
        return self.soup.select('div[class="entry-container"] [class="entry-content"]')[0].text.strip()[:1024]
