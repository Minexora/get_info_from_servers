import os
import sys
import json
import glob
import argparse
from dotenv import load_dotenv


class Config:
    """ Config içerisinde;
            - file_config: Object
            - argv_conf: List
            - env_config: Object
    
    """
    __conf_obj = {}
    __parser = argparse.ArgumentParser()
    __base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def __init__(self) -> None:
        self.__file_read()
        self.__arguman_parse()
        self.__env_read()

    def __call__(self):    
        self.__file_read()
        self.__arguman_parse()
        self.__env_read()
        return  self.__conf_obj        

    def __file_read(self):
        if os.path.isfile('config/conf.json'):
            with open(os.path.join(self.__base_dir, 'config/conf.json'), 'r', encoding='utf-8') as json_file:
                json_data = json_file.read()
                self.__conf_obj["file_config"] = json.loads(json_data) if json_data else {}
        else:
            self.__conf_obj["file_config"] = {}

    def __arguman_parse(self):
        if len(sys.argv) > 1:
            # self.__conf_obj['argv_conf'] = self.__parser.parse_args(sys.argv)
            self.__conf_obj['argv_conf'] = sys.argv[1:]
        else:
            self.__conf_obj['argv_conf'] = []

    def __env_read(self):
        load_dotenv()
        self.__conf_obj["env_config"] = dict(os.environ)

    # def get_config(self):
    #     return self.__conf_obj

    def print_json_file(self, config):
        with open(os.path.join(self.__base_dir, 'config/conf.json'), 'w', encoding='utf-8') as json_file:
            json_file.write(json.dumps(config, indent=2))

# config_class = Config()
# config = config_class.get_config()

# if __name__ == "__main__":
#     config = Config()()
#     config["file_config"]["Deneme"] = 5
#     config.print_json_file(config['file_config'])
#     print(config)