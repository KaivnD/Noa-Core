from OSMApiTasker.OSMApiTasker import *
import_data={'location':'114.21892734521,29.575429778924',
            'width':2000,
            'height':1500}
#长度，宽度单位为米。
a=OSMApiTasker(import_data,'txt')
print(a.run())
