from Noa.Hooks import Hook,before,after
from lxml import etree
import math,rhino3dm,json

class Utils(object):
    def __init__(self,import_data,output_data):
        self.import_data=import_data
        self.output_data=output_data
    
    def run(self):
        #入口方法
        return(self.process())

    @before('txt_output')
    def txt_pre_deal(self,content,file_name='test',cover=True):
        #预处理数据，用来重写。
        pass

    @Hook
    def txt_output(self,content,file_name='test',cover=True):
    #将数据储存为txt
        g=lambda: 'w' if cover else 'a'
        try:
            with open('{}.txt'.format(file_name),g()) as f:
                f.write(str(content))
        except UnicodeEncodeError:
            with open('{}.txt'.format(file_name),g(),encoding='utf-8') as f:
                f.write(str(content))
        return(True)

    @before('rhino_output')
    def rhino_pre_deal(self,content,file_name='test',cover=True):
        #预处理数据，用来重写。
        pass

    @Hook
    def rhino_output(self,content,file_name='test',cover=True):
    #将数据储存为rhino文件
        self.model.Write(file_name+'.3dm')
        return(True)

    @before('svg_output')
    def svg_pre_deal(self,content,file_name='test',cover=True):
        #预处理数据，用来重写。
        pass

    @Hook
    def svg_output(self,content,file_name='test',cover=True):
    #将数据储存为svg文件
        pass
        return(True)

    @before('dxf_output')
    def dxf_pre_deal(self,content,file_name='test',cover=True):
        #预处理数据，用来重写。
        pass

    @Hook
    def dxf_output(self,content,file_name='test',cover=True):
        #将数据储存为svg文件
        pass
        return(True)
    
    def output_file(self,content,file_name,cover=True):
        #输出方法，建议在output方法中调用该方法。
        file_type=file_name.split('.')[1]
        method_dict={'txt':self.txt_output,
                     '3dm':self.rhino_output,
                     'svg':self.svg_output,
                     'dxf':self.dxf_output}
        result=method_dict[file_type](content,file_name.split('.')[0])
        return(result)

class OsmConvert(Utils):
    #将osm格式的文件解析为json。

    @before('process')
    def input(self):
        #输入方法，将经纬度处理为XY坐标体系。
        scale=self.import_data['scale']
        html=etree.parse(self.import_data['file_name'])
        self.minlat = float(str(html.xpath('//bounds/@minlat')[0]))
        self.maxlat = float(str(html.xpath('//bounds/@maxlat')[0]))
        self.minlon = float(str(html.xpath('//bounds/@minlon')[0]))
        self.maxlon = float(str(html.xpath('//bounds/@maxlon')[0]))
        a = self.maxlat - self.minlat
        b = self.minlat + a / 2.0
        self.c = 3.1415926535897931 * 6371000 / 180.0 * scale
        self.d = 3.1415926535897931 * (math.cos(b * 3.1415926535897931 / 180.0) * 6371000) / 180.0 * scale

    def get_XY(self,lon,lat):
        X = (lon - self.minlon) * self.d
        Y = (lat - self.minlat) * self.c
        return((X,Y))

    @Hook
    def process(self):
        #构建json。
        node_dict={}
        html=etree.parse(self.import_data['file_name'])
        nodes=html.xpath('//node')
        for node in nodes:
            node_id=node.xpath('./@id')[0]
            node_loc=(node.xpath('./@lon')[0],node.xpath('./@lat')[0])
            node_dict[node_id] = dict(loc=self.get_XY(float(node_loc[0]),float(node_loc[1])),info={})
            children_nodes=node.xpath('.//tag')

            if len(children_nodes) != 0:
                for children_node in children_nodes:
                    key=children_node.xpath('./@k')[0]
                    value=children_node.xpath('./@v')[0]
                    node_dict[node_id]['info'][key]=value

        way_dict={}
        ways=html.xpath('//way')
        for way in ways:
            way_id=way.xpath('./@id')[0]
            way_nodes=way.xpath('.//nd/@ref')
            way_nodes=[node_dict[i]['loc'] for i in way_nodes]
            way_dict[way_id]=dict(nodes=way_nodes,info={})
            children_tags=way.xpath('.//tag')
            if len(children_tags) != 0:
                for children_tag in children_tags:
                    key=children_tag.xpath('./@k')[0]
                    value=children_tag.xpath('./@v')[0]
                    way_dict[way_id]['info'][key]=value
        
        self.info_dict=dict(node_info=node_dict,way_info=way_dict)
        return (self.info_dict)


    @after('process')
    def output(self):
        self.output_file(self.info_dict,self.output_data['file_name'])
        pass
    
    @before('txt_output')
    def txt_pre_deal(self,content,file_name='test',cover=True):
        self.info_dict=json.dumps(self.info_dict)
    
    @before('rhino_output')
    def rhino_pre_deal(self,content,file_name='test',cover=True):
        tag_list=[  "aerialway",
                    "aeroway",
                    "amenity",
                    "barrier",
                    "boundary",
                    "building",
                    "craft",
                    "emergency",
                    "geological",
                    "highway",
                    "historic",
                    "landuse",
                    "leisure",
                    "man_made",
                    "military",
                    "natural",
                    "office",
                    "place",
                    "power",
                    "public_transport",
                    "railway",
                    "route",
                    "shop",
                    "sport",
                    "tourism",
                    "waterway"]
        layer_list=[]

        self.model=rhino3dm.File3dm()
        objects=self.model.Objects
        layers=self.model.Layers



        for way in self.info_dict['way_info']:
            temp=self.info_dict['way_info'][way]
            for i in temp['info']:
                if i in tag_list:
                    layer_name='{}${}'.format(i,temp['info'][i])
                    if layer_name not in layer_list:
                        layer_list.append(layer_name)
                        tem_layer=rhino3dm.Layer()
                        tem_layer.Name = layer_name
                        layers.Add(tem_layer)
                    break
  
            line = rhino3dm.Polyline()
            for node in temp['nodes']:
                line.Add(node[0],node[1],0)
            
            object_id = objects.AddPolyline(line)
            '''
            for xxx in objects:
                j=j+1
                if xxx.Attributes.Id == object_id:
                    print(j)
            '''
            print(objects[len(objects)-1].Attributes.Id)
            #print(layers.FindName(layer_name,None).Index)
            objects[len(objects)-1].Attributes.LayerIndex = layers.FindName(layer_name,None).Index
        return(True)

