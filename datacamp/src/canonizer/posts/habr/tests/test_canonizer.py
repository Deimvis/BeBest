import json
import unittest
import lib
from typing import Dict, Sequence
from src.canonizer.posts.habr.canonizer import HabrPostsCanonizer


class TestHabrPostsCanonizer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.real_data = json.dumps({
            'author_username': 'k0rsakov',
            'complexity': 'Средний',
            'hubs': ['Python *', 'Big Data *', 'Хранилища данных *', 'Data Engineering *'],
            'reading_time': '6 мин',
            'starting_text': 'Оглавление:ПроблематикаРешениеПример решения проблематики описанной выше:Установка AirflowПишем шаблонный DAGИзменение его под шаблонГенерация DAGСоздание \'генератора\' DAGМасштабированиеРекомендацииИтогПроблематикаТиповая задача для\xa0дата‑инженера\xa0— это перенести данные из\xa0реплики/боевой OLTP DB в\xa0аналитическое хранилище.В\xa0данной задаче обычно нужно переносить несколько таблиц и принцип их переноса является одинаковым. Ввиду чего необходимо создавать DAG с\xa0небольшими изменениями в\xa0коде.Чаще всего это происходит так: дата‑инженер заходит в\xa0типовой DAG и выполняет следующие действия:Cmd+ACmd+CCmd+VПоменял пару строчек в DAG, совершил опечатку/неверно скопировал/что-то ещеРешениеГенерация DAG по типовому DAG (шаблону).Создаем шаблон, изменяем автоматически все необходимые поля и радуемся пускам в прод.Пример решения проблематики описанной вышеНиже будет поэтапно расписано как можно просто сделать фабрику DAG, благодаря которой можно смело пускать в прод полученные DAG.Используемые технологии:Все операции выполнял',
            'tags': [],
            'title': 'Генерация DAG в Apache Airflow',
            'publish_datetime': '2023-03-16T03:04:05.000Z',
            'url': 'https://habr.com/ru/articles/722688/',
            'views': '3K'
        }, ensure_ascii=False)

    def test_smoke(self):
        _ = HabrPostsCanonizer(output_consumer=lib.consumers.DummyConsumer(), logs_consumer=lib.consumers.DummyConsumer())

    def test_canonize(self):
        with lib.consumers.BufferedConsumer() as output_consumer, \
                lib.consumers.BufferedConsumer() as logs_consumer:
            canonizer = HabrPostsCanonizer(output_consumer=output_consumer, logs_consumer=logs_consumer)
            canonizer.canonize(self.real_data)
            output = output_consumer.buffer.read_all()
            logs = logs_consumer.buffer.read_all()
            self.assertEqual(len(output), 1)
            self.assertEqual(self._count_errors(logs), 0)

    def _count_errors(self, logs: Sequence[Dict]):
        cnt = 0
        for log in logs:
            cnt += log['level'] == 'ERROR'
        return cnt
