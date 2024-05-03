from dataclasses import dataclass
from typing import Dict
import yaml
from filelocations import config_file


class MongooseConfig:
    name: str
    mongoose_id:str
    def __init__(self,mongoose_id,name,**properties):
        self.mongoose_id=mongoose_id
        self.name=name
        self.properties=properties

class GBusSinkConfig(MongooseConfig):
    def __init__(self, mongoose_id, name, waterlevel, headroom, type,**properties):
        self.waterlevel=waterlevel
        self.headroom=headroom
        self.type=type
        super().__init__(mongoose_id, name, **properties)
        


def loadConfig(mongoose_id:str, src:str=None,config_cls:type=None) -> MongooseConfig:
    if config_cls is None:
        config_cls = MongooseConfig
    src = src or config_file
    with open(src) as f:
        data = yaml.load(f,Loader=yaml.CSafeLoader)
    try:
        return config_cls(mongoose_id=mongoose_id,**data[mongoose_id])
    except KeyError as x:
        raise Exception(f'Not a valid mongoose id: "{mongoose_id}"') from x

def loadAllConfig(src:str=None) -> Dict[str,MongooseConfig]:
    src = src or config_file
    with open(src) as f:
        data = yaml.load(f)
    for k in data:
        data[k] = MongooseConfig(
            mongoose_id=k,
            **data[k])
    return data