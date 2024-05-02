from dataclasses import dataclass
import yaml

@dataclass
class MongooseConfig:
    interface: dict




def load(src:str) -> MongooseConfig:
    with open(src) as f:
        data = yaml.load(f)
    return MongooseConfig(**data)