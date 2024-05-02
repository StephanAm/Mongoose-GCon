import unittest
from bus.bustypes import BUS_TYPE, busFromTopic, topicFromBus


class BusTypesFixture(unittest.TestCase):

    _cases = (
        (BUS_TYPE.COMMAND,"/mongoose/command"),
        (BUS_TYPE.GBUS,"/mongoose/gbus"),
        (BUS_TYPE.LOG,"/mongoose/log"),
        (BUS_TYPE.SYSTEM,"/mongoose/panic"),
        (BUS_TYPE.STATUS,"/mongoose/status"),
    )
    def test_topicFromBus(self):
        for bus,topic in self._cases:
            r = topicFromBus(bus)
            self.assertEqual(r,topic)
    
    def test_busFromTopic(self):
        for bus,topic in self._cases:
            r = busFromTopic(topic)
            self.assertEqual(r,bus)


    _fail_cases = {
        "/mongoose/invalid", #invalid queue specifier
        "mongoose/command",
        "/mongoose/invalid/command",
        "command",
        
    }
    
    def test_busFromTopic_failsForBadCases(self):
        for topic in self._fail_cases:
            self.assertRaises(ValueError,lambda:busFromTopic(topic))