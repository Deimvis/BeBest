import json
import time
import unittest
import lib
from typing import Dict, Sequence
from src.canonizer.posts.medium.canonizer import MediumPostsCanonizer


class TestMediumPostsCanonizer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.real_data = json.dumps({
            'author_username': 'Gergely Szerovay',
            'publisher': 'Angular Addicts',
            'title': 'Angular Addicts #18: Angular 17’s New control flow and View transitions, Incremental static regeneration & more',
            'tags': ['Angular', 'Rxjs', 'Ngrx', 'Typescript', 'JavaScript'],
            'publish_date': 'Oct 3',
            'url': 'https://medium.com/angularaddicts/angular-addicts-18-angular-17s-new-control-flow-and-view-transitions-incremental-static-85f7bc98ffa2',
        }, ensure_ascii=False)

    def test_smoke(self):
        _ = MediumPostsCanonizer(output_consumer=lib.consumers.DummyConsumer(), logs_consumer=lib.consumers.DummyConsumer())

    def test_canonize(self):
        with lib.consumers.BufferedConsumer() as output_consumer, \
                lib.consumers.BufferedConsumer() as logs_consumer:
            canonizer = MediumPostsCanonizer(output_consumer=output_consumer, logs_consumer=logs_consumer)
            canonizer.canonize(self.real_data)
            output = output_consumer.buffer.read_all()
            logs = logs_consumer.buffer.read_all()
            self.assertEqual(len(output), 1)
            self.assertEqual(self._count_errors(logs), 0)

        with lib.consumers.BufferedConsumer() as output_consumer, \
                lib.consumers.BufferedConsumer() as logs_consumer:
            canonizer = MediumPostsCanonizer(output_consumer=output_consumer, logs_consumer=logs_consumer)
            data_json = json.loads(self.real_data)
            data_json['publish_date'] = '1 day ago'
            data = json.dumps(data_json, ensure_ascii=False)
            canonizer.canonize(data)
            output = output_consumer.buffer.read_all()
            logs = logs_consumer.buffer.read_all()
            self.assertEqual(len(output), 1)
            self.assertEqual(self._count_errors(logs), 0)
            self.assertAlmostEqual(output[0]['publish_timestamp'], int(time.time()) - 24 * 60 * 60, delta=60*60)

    def _count_errors(self, logs: Sequence[Dict]):
        cnt = 0
        for log in logs:
            cnt += log['level'] == 'ERROR'
        return cnt
