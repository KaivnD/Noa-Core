from LocationConvertApiTasker.LocationConvertApiTasker import *
import_data={'location':[114.21892734521,29.575429778924,'WGS84ll']}
output_data={'file_name':'text.txt'}
a=LocationConvertApiTasker(import_data,output_data)
print(a.run())
