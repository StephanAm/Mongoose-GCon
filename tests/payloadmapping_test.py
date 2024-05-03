import unittest
from bus.payloads import STATUS, Status

class PayloadSerializationTests(unittest.TestCase):
    def test_StatusMessageSerializesCorrectly(self):
        msg = Status("my-id",STATUS.DOWN)
        res = msg.serialize()
        self.assertTrue(res)

    def test_StatusMessageDeserializesCorrectly(self):
        src='{"id": "my-id", "status": "DOWN"}'
        res = Status.deserialize(src)
        self.assertTrue(isinstance(res.status,STATUS))
        self.assertEqual(STATUS.DOWN, res.status)

        