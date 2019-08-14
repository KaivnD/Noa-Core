from AdressConvertApiTasker.AdressConvertApiTasker import *
import_data={'location':'31.225696563611,121.49884033194',}
output_data={'file_name':'test.txt'}
a=AdressConvertApiTasker(import_data,output_data)
print(a.run())
