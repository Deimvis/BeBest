from collections import defaultdict
from typing import Iterable, Type
from lib.sources import SourceName
from lib.resources import ResourceName
from .base import ControllerBase


class ControllersManager:
    def __init__(self, Controllers: Iterable[Type[ControllerBase]]):
        self._Controllers = Controllers
        self._resource_name2Controller = {
            Controller.RESOURCE_NAME: Controller for Controller in Controllers
        }

    def find_Controller(self, resource_name: str) -> Type[ControllerBase]:
        assert resource_name in ResourceName.all()
        return self.resource_name2Controller[resource_name]

    @property
    def Controllers(self):
        return self._Controllers

    @property
    def resource_name2Controller(self):
        return self._resource_name2Controller

