from Noa.Hooks import Hook,before,after
from lxml import etree
import math

class Utils(object):
    def __init__(self,import_data,output_data):
        self.import_data=import_data
        self.output_data=output_data
    
    def output_file(self,content,file_name,cover=True):
        g=lambda: 'w' if cover else 'a'
        with open(file_name,g()) as f:
            f.write(str(content))
        return(True)


class OsmConvert(Utils):
    #将osm格式的文件解析为json。

    @before('process')
    def input(self):
        scale=self.import_data['scale']
        html=etree.parse(self.import_data['file_name'])
        self.minlat = float(str(html.xpath('//bounds/@minlat')[0]))
        self.maxlat = float(str(html.xpath('//bounds/@maxlat')[0]))
        self.minlon = float(str(html.xpath('//bounds/@minlon')[0]))
        self.maxlon = float(str(html.xpath('//bounds/@maxlon')[0]))
        print(self.minlat)
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
        print(way_dict)
        info_dict=dict(node_info=node_dict,way_info=way_dict)
        return (info_dict)


    @before('process')
    def output(self):
        pass