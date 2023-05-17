import re
from src.crawler.parser_base import ParserBase, ParserBaserMeta


class Parser(ParserBase, metaclass=ParserBaserMeta):

    def parse_title(self):
        return self.soup.select('h1[class*="pw-post-title"]')[0].text

    def parse_author_username(self):
        if self._is_published():
            return self.soup.find_all('span', text='Published in')[0].parent.parent.parent.parent.parent.parent.select('p')[0].text
        else:
            return self.soup.find_all('span', text=re.compile(r'^[A-Z][a-z]{2} \d{1,2}.*'))[0].parent.parent.parent.parent.parent.parent.select('a[href*="/@"]')[0].text

    def parse_publisher(self):
        if self._is_published():
            return self.soup.find_all('span', text='Published in')[0].parent.select('p')[0].text
        raise RuntimeError('Article was not published')

    def parse_publish_date(self):
        if self._is_published():
            return self.soup.find_all('span', text='Published in')[0].parent.parent.parent.select('span')[-1].text
        else:
            return self.soup.find_all('span', text=re.compile(r'^[A-Z][a-z]{2} \d{1,2}.*'))[0].text

    def parse_tags(self):
        return [tag.text for tag in self.soup.select('a[href*="https://medium.com/tag/"]')]

    def _is_published(self):
        return len(self.soup.find_all('span', text='Published in')) > 0
