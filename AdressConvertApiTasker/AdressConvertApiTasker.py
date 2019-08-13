from Noa.Core import ApiTasker
from Noa.Hooks import precall_register, postcall_register
import os,sys

class AdressConvertApiTasker(ApiTasker):
    @precall_register('read_config')
    def config_location(self):
        self.config_location=os.path.split(os.path.abspath(__file__))[0]

    @precall_register('process')
    def input(self):
        self.url=self.import_data['config_data']['url']
        self.url=self.url+'ak={}&output=json&coordtype=bd09ll&location={}'.format(self.import_data['config_data']['ak'],self.import_data['location'])

    @postcall_register('process')
    def output(self):
        if self.api_data['status'] == 0:
            self.result=self.api_data
            return(self.result)
        else:
            return('Error!')
