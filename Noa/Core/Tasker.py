from Noa.Hooks import Hook
import urllib.request
import json,configparser

class ApiTasker(object):

    def __init__(self, import_data, output_data):
        self.import_data = import_data
        self.output_data = output_data
        self.import_data['config_data'] = self.read_config()

    def read_config(self):
        self.config_data={}
        config = configparser.ConfigParser()
        config.readfp(open(r'config.ini'))
        opts=config.options('config')
        for i in opts:
            self.config_data[i]=config.get("config",i)
        return(self.config_data)

    @Hook
    def process(self):
        res = urllib.request.Request(self.url)
        result = urllib.request.urlopen(res).read().decode('utf-8')
        self.api_data=json.loads(result)

    def run(self):
        self.process()
        return(self.result)
