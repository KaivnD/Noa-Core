from AdressConvertApiTasker.AdressConvertApiTasker import *
import_data={'location':'31.225696563611,121.49884033194',}
a=AdressConvertApiTasker(import_data,'txt')
print(a.run())
