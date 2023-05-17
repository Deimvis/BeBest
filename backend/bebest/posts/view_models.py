from dataclasses import dataclass
from typing import List, Self
from .models import Post


@dataclass
class PostView:
    canonized_url: str
    source_name: str
    title: str
    starting_text: str
    author_username: str | None

    def has_author(self) -> bool:
        if self.source_name == Post.SourceName.DCM:
            return False
        return self.author_username is not None and self.author_username != ''

    @property
    def beautiful_source_name(self) -> str:
        match self.source_name:
            case Post.SourceName.HABR:
                return 'Habr'
            case Post.SourceName.MEDIUM:
                return 'Medium'
            case Post.SourceName.DCM:
                return 'Distributed Computing Musings'


    @staticmethod
    def from_post(post: Post) -> Self:
        title = post.title.capitalize()
        if len(title) > 100:
            title = title[:97] + '...'
            print(title)
        return PostView(
            canonized_url=post.canonized_url,
            source_name=post.source_name,
            title=title,
            starting_text=post.starting_text.capitalize(),
            author_username=post.author_username,
        )
