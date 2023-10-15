import re
from src.scrapers.parser_base import ParserBase, ParserBaserMeta


class MediumArticleParser(ParserBase, metaclass=ParserBaserMeta):

    def parse_title(self):
        return self.soup.select('h1[class*="pw-post-title"]')[0].text

    def parse_author_username(self):
        if self._is_published():
            return self.soup.find_all('span', string='Published in')[0].parent.parent.parent.parent.parent.parent.select('p')[0].text
        else:
            return self.soup.find_all('span', string=re.compile(r'^[A-Z][a-z]{2} \d{1,2}.*'))[0].parent.parent.parent.parent.parent.parent.select('a[href*="/@"]')[0].text

    def parse_publisher(self):
        if self._is_published():
            return self.soup.find_all('span', string='Published in')[0].parent.select('p')[0].text
        raise RuntimeError('Article was not published')

    def parse_publish_date(self):
        if self._is_published():
            header = self.soup.find_all('span', string='Published in')[0].parent.parent.parent
            match_result = re.fullmatch(r'^.*([0-9]{1,2} days? ago).*$', header.text)
            if match_result is not None:
                return match_result.group(1)
            return header.select('span')[-1].text
        else:
            return self.soup.find_all('span', string=re.compile(r'^[A-Z][a-z]{2} \d{1,2}.*'))[0].text

    def parse_tags(self):
        return [tag.text for tag in self.soup.select('a[href*="https://medium.com/tag/"], a[href*="/tag/"]')]

    def _is_published(self):
        return len(self.soup.find_all('span', string='Published in')) > 0
