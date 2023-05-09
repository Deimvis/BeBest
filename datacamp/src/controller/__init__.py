from . import (  # noqa
    base,
    manager,
)

from .base import ControllerBase  # noqa
from .manager import ControllersManager  # noqa
from .posts import PostsController

ALL_CONTROLLERS = [PostsController]
controllers_manager = ControllersManager(ALL_CONTROLLERS)
