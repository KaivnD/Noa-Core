from Noa.ApiTasker.LocationConvertApiTasker import *
import_data={'location':[114.21892734521,29.575429778924,'WGS84ll']}
a=LocationConvertApiTasker(import_data,'txt')
print(a.run())
