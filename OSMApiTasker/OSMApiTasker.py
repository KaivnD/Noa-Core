from Noa.Core import ApiTasker
from Noa.Hooks import precall_register, postcall_register
import sys,os,math

class OSMApiTasker(ApiTasker):
    @precall_register('read_config')
    def config_location(self):
        self.config_location=os.path.split(os.path.abspath(__file__))[0]

    @precall_register('process')
    def input(self):
        self.url=self.import_data['config_data']['url']
        self.url=self.url+'?bbox={}'.format(self.location_convert())

    @postcall_register('process')
    def output(self):
        file_name=self.output_data['file_name']
        self.output_file(self.api_data,file_name)

    def location_convert(self):
        width=float(self.import_data['width'])
        height=float(self.import_data['height'])
        x=float(self.import_data['location'].split(',')[0])
        y=float(self.import_data['location'].split(',')[1])
        r=int(self.import_data['config_data']['planet_radius'])
        return('{},{},{},{}'.format(x-180*height/math.pi/r,y-180*width/math.pi/r,x+180*height/math.pi/r,y+180*width/math.pi/r))