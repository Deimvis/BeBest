from . import (  # noqa
    base,
    manager,
)

from .base import ControllerBase  # noqa
from .manager import ControllersManager  # noqa
from .posts import PostsController  # noqa
from .vacancies import VacanciesController  # noqa

ALL_CONTROLLERS = [PostsController, VacanciesController]
controllers_manager = ControllersManager(ALL_CONTROLLERS)
