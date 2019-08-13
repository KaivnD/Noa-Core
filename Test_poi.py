from PoiApiTasker.PoiApiTasker import *
import_data={'location':'39.915,116.404',
            'search_type':'round',
            'type_data':'1000',
            'query':'银行'
            }
a=PoiApiTasker(import_data,'txt')
print(a.run())
