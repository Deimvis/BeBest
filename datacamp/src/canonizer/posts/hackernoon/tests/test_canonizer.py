import json
import unittest
import lib
from typing import Dict, Sequence
from src.canonizer.posts.hackernoon.canonizer import HackernoonPostsCanonizer


class TestHabrPostsCanonizer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.real_data = json.dumps({
            "author_username": "mirotalk",
            "publish_date": "2023/11/02",
            "starting_text": "This HTML and JavaScript code creates a virtual background effec",
            "tags": [
                "programming",
                "webrtc",
                "virtualbackground",
                "video-streaming",
                "video-conference",
                "live-streaming-video",
                "virtual-meetings",
                "online-privacy"
            ],
            "title": "Creating Real-Time Virtual Backgrounds With BodyPix and Webcam in HTML and JavaScript",
            "url": "https://hackernoon.com/creating-real-time-virtual-backgrounds-with-bodypix-and-webcam-in-html-and-javascript"
        }, ensure_ascii=False)

    def test_smoke(self):
        _ = HackernoonPostsCanonizer(output_consumer=lib.consumers.DummyConsumer(), logs_consumer=lib.consumers.DummyConsumer())

    def test_canonize(self):
        with lib.consumers.BufferedConsumer() as output_consumer, \
                lib.consumers.BufferedConsumer() as logs_consumer:
            canonizer = HackernoonPostsCanonizer(output_consumer=output_consumer, logs_consumer=logs_consumer)
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
