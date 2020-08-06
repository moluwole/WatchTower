from configparser import ConfigParser
import os
import shutil
from .utils import Display

from .exception import ConfigFileNotFoundError


class LoadConfig(object):
    def __init__(self, path=os.environ["PWD"]):
        if not os.path.exists(path):
            Display().print("ERROR", str(ConfigFileNotFoundError()))
            raise ConfigFileNotFoundError()

        self.path = os.path.abspath(path)
        self.config = ConfigParser()
        self.config.read(self.path)

    def setup(self, path: str = os.environ["PWD"]) -> bool:
        setup_path = os.path.dirname(os.path.realpath(__file__))
        path = os.path.abspath(path)
        source_file = os.path.join(setup_path, ".watchtower.ini")

        target_file = os.path.join(path, ".watchtower.ini")
        if os.path.isfile(target_file):
            Display().print("ERROR", "Config file exists")
            return False

        shutil.copy(source_file, target_file)
        Display().print("SUCCESS", "Config Setup successfully")
