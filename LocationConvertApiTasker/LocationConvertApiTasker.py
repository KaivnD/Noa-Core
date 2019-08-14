from Noa.Core import ApiTasker
from Noa.Hooks import precall_register, postcall_register
import sys,os

class LocationConvertApiTasker(ApiTasker):
    @precall_register('read_config')
    def config_location(self):
        self.config_location=os.path.split(os.path.abspath(__file__))[0]


    @precall_register('process')
    def input(self):
        if self.import_data['location'][2]=='WGS84ll':
            self.url=self.import_data['config_data']['url']+'coords={},{}&from=1&to=5&ak={}'.format(self.import_data['location'][0],self.import_data['location'][1],self.import_data['config_data']['ak'])
        elif self.import_data['location'][2]=='GCJ02':
            self.url=self.import_data['config_data']['url']+'coords={},{}&from=3&to=5&ak={}'.format(self.import_data['location'][0],self.import_data['location'][1],self.import_data['config_data']['ak'])
            pass
        else:
            return('Error:Unvalid map code!')

    @postcall_register('process')
    def output(self):
        if self.api_data['status'] == 0:
            self.result=(self.api_data['result'][0]['x'],self.api_data['result'][0]['y'],'BD09ll')
            file_name=self.output_data['file_name']
            self.output_file(self.result,file_name)
            return(self.result)
        else:
            return('Error!')
