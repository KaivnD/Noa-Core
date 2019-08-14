from Noa.Hooks import Hook
import urllib.request,json,configparser,sys,os

class Tasker(object):
    def __init__(self, import_data, output_data):
        self.import_data = import_data
        self.output_data = output_data
        self.import_data['config_data'] = self.read_config()

    @Hook
    def read_config(self):
        self.config_data={}
        config = configparser.ConfigParser()
        config.readfp(open(self.config_location+'/config.ini'))
        opts=config.options('config')
        for i in opts:
            self.config_data[i]=config.get("config",i)
        return(self.config_data)
    
    def output_file(self,content,file_name,cover=True):
        g=lambda: 'w' if cover else 'a'
        with open(file_name,g()) as f:
            f.write(str(content))
        return(True)


class ApiTasker(Tasker):

    @Hook
    def process(self):
        res = urllib.request.Request(self.url)
        result = urllib.request.urlopen(res).read().decode('utf-8')
        try:
            self.api_data=json.loads(result)
        except:
            self.api_data=result

    def run(self):
        self.process()
        self.result=True
        return(self.result)
