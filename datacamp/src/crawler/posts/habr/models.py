import bs4
import regex_spm
from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel


class Article(BaseModel):
    author_username: Optional[str]
    complexity: Optional[str]
    hubs: List[str]
    reading_time: str
    starting_text: str
    tags: List[str]
    title: str
    publish_datetime: str
    url: str
    views: str


    @staticmethod
    def from_tag(tag: bs4.element.Tag, ctx: Dict) -> 'Article':
        assert 'url' in ctx
        url = ctx['url']
        title = tag.select_one('[class*="tm-title"]').text.strip()
        publish_datetime = tag.select_one('[class="tm-article-datetime-published"]').select_one('time')['datetime']
        views = tag.select_one('[class="tm-icon-counter__value"]').text.strip()
        starting_text = tag.select_one('[id="post-content-body"]').text.strip()[:1024]
        reading_time = tag.select_one('span[class="tm-article-reading-time__label"]').text.strip()

        author_username = None
        author_username_tag = tag.select_one('a[class="tm-user-info__username"]')
        if author_username_tag is not None:
            author_username = author_username_tag.text.strip()

        complexity = None
        complexity_tag = tag.select_one('[class="tm-article-complexity__label"]')
        if complexity_tag is not None:
            complexity = complexity_tag.text.strip()

        hubs = []
        info_tags = tag.select_one('[class="tm-article-snippet__hubs"]').select('a')
        for info_tag in info_tags:
            match regex_spm.fullmatch_in(info_tag['href']):
                case r'.*\/hub\/.*':
                    hubs.append(info_tag.text)

        tags = []
        lists = tag.select_one('[class="tm-article-presenter__meta"]').select('[class^="tm-separated-list "]')
        for list_ in lists:
            list_title = list_.select_one('[class="tm-separated-list__title"]').text.strip()
            match list_title:
                case 'Теги:':
                    tags = [a_tag.text for a_tag in list_.select('a')]

        return Article(
            author_username=author_username,
            complexity=complexity,
            hubs=hubs,
            reading_time=reading_time,
            starting_text=starting_text,
            tags=tags,
            title=title,
            publish_datetime=publish_datetime,
            url=url,
            views=views,
        )
