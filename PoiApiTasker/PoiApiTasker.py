from Noa.Core import ApiTasker
from Noa.Hooks import precall_register, postcall_register
import sys,os,urllib.parse

class PoiApiTasker(ApiTasker):
    @precall_register('read_config')
    def config_location(self):
        self.config_location=os.path.split(os.path.abspath(__file__))[0]


    @precall_register('process')
    def input(self):
        func={'region':self.region_url,
              'round':self.round_url,
              'bounds':self.bounds_url}
        self.url=self.import_data['config_data']['url']
        self.url=func[self.import_data['search_type']]()


    def region_url(self):
        url=self.url+'&query={}&ak={}&region={}'.format(urllib.parse.quote(self.import_data['query']),self.import_data['config_data']['ak'],self.import_data['type_data'])
        return(urllib.parse.quote(url))

    def round_url(self):
        url=self.url+'&query={}&ak={}&radius={}&location={}'.format(urllib.parse.quote(self.import_data['query']),self.import_data['config_data']['ak'],self.import_data['type_data'],self.import_data['location'])
        print(url)
        return(url)

    def bounds_url(self):
        url=self.url+'&query={}&ak={}&bounds={}'.format(urllib.parse.quote(self.import_data['query']),self.import_data['config_data']['ak'],self.import_data['type_data'])
        return(urllib.parse.quote(url))


    @postcall_register('process')
    def output(self):
        print (self.api_data)
        if self.api_data['status'] == 0:
            with open('a.txt','w') as f:
                f.write(str(self.api_data))
        else:
            return('Error!')
