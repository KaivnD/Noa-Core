from Noa.Core.Utils import *
import_data={'file_name':'temp/test.osm','scale':1}
output_data={'file_name':'test.3dm'}
a=OsmConvert(import_data,output_data)
a.run()
