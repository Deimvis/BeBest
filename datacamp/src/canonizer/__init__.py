from . import (  # noqa
    base,
    helpers,
    manager,
    posts,
)

from .base import CanonizerBase  # noqa
from .manager import CanonizersManager  # noqa
from .posts import DCMPostsCanonizer, HabrPostsCanonizer, HackernoonPostsCanonizer, MediumPostsCanonizer # noqa
from .vacancies import HHAPIPostsCanonizer  # noqa


ALL_CANONIZERS = [DCMPostsCanonizer, HabrPostsCanonizer, HackernoonPostsCanonizer, MediumPostsCanonizer, HHAPIPostsCanonizer]
canonizers_manager = CanonizersManager(ALL_CANONIZERS)
