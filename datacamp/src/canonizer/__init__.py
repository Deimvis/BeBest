from . import (  # noqa
    base,
    helpers,
    manager,
    posts,
)

from .base import CanonizerBase  # noqa
from .manager import CanonizersManager  # noqa
from .posts import HabrPostsCanonizer  # noqa


ALL_CANONIZERS = [HabrPostsCanonizer]
canonizers_manager = CanonizersManager(ALL_CANONIZERS)
