from dataclasses import dataclass
import yaml

# should be an absolute path for release. figure out a mechanism
_DEFAULT_CONFIG="./config.yaml"


@dataclass
class MongooseConfig:
    interface: dict




def loadConfig(src:str=None) -> MongooseConfig:
    src = src or _DEFAULT_CONFIG
    with open(src) as f:
        data = yaml.load(f)
    return MongooseConfig(**data)