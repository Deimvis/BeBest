import json
import time
import traceback
from typing import Dict

from lib.resources import ResourceName
from src.controller.base import ControllerBase
from .model import VacancyRecord


class VacanciesController(ControllerBase):
    RESOURCE_NAME = ResourceName.VACANCY

    def store(self, record: Dict) -> None:
        vacancy_record = VacancyRecord(**record)
        try:
            self._store(vacancy_record)
        except Exception as error:
            self.write_error(json.dumps({
                'error': str(error),
                'traceback': traceback.format_exc(),
                'context': {'unique_key': vacancy_record.unique_key()},
            }))

    def _store(self, vacancy_record: VacancyRecord) -> None:
        stored_vacancy_record = self._get_same_stored(vacancy_record)
        if stored_vacancy_record is None:
            self._insert(vacancy_record)
        else:
            self._merge(stored_vacancy_record, vacancy_record)

    def _get_same_stored(self, vacancy_record: VacancyRecord) -> VacancyRecord | None:
        select_ = self.storage.select(where=vacancy_record.unique_key())
        if len(select_) == 0:
            return
        return VacancyRecord(**select_[0])

    def _insert(self, vacancy_record: VacancyRecord) -> None:
        vacancy_record.insert_timestamp = int(time.time())
        self.storage.insert([vacancy_record.table_record()])

    def _merge(self, stored_vacancy_record: VacancyRecord, new_vacancy_record: VacancyRecord) -> None:
        new_vacancy_record.insert_timestamp = int(time.time())
        self.storage.update(set_=new_vacancy_record.table_record(), where=new_vacancy_record.unique_key())
