from gexcel import ExcelBase

from pprint import pprint


class module(object):
    def __init__(self, ):
        weekend, camp, stripe = ExcelBase().ongoing()
        pprint(stripe)
        
m = module()