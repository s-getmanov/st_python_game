
from utils import randbool

class Clouds(object):
    
    class Cloud_cell(object):
        def __init__(self, sym):
            self.value =  sym 

    def __init__(self, h, w, legend):
        self.h = h
        self.w = w
        self.legend = legend
        self.cells = [[self.Cloud_cell(self.legend.none) for i in range(self.w)] for j in range(self.h)]
    
    def check_bounds(self, x ,y):
        if (x < 0 or y < 0 or x >= self.h or y >= self.w):
            return False
        return True

    def getCell(self, h, w):
        if self.check_bounds(h, w):
            return self.cells[h][w].value
        return self.legend.none
    
    def notNone(self, h, w):
        return not self.getCell(h, w) == self.legend.none
    
    def isCloud(self, h, w):
        return not self.getCell(h, w) == self.legend.cloud
    
    def isthundercloud(self, h, w):
        return not self.getCell(h, w) == self.legend.thundercloud

    def update(self, pr_cloud, pr_thundercloud):
        for row in self.cells:
            for cell in row:
                if randbool(pr_cloud):
                    cell.value = self.legend.cloud
                elif randbool(pr_thundercloud):
                    cell.value = self.legend.thundercloud
                else:
                    cell.value = self.legend.none

    def export_data(self):
        return {                
                "cells":[[self.legend.encode_symbol(i.value) for i in j] for j in self.cells] ,                        
                }
    
    def import_data(self, data):
        self.cells =  [[ self.Cloud_cell(self.legend.decode_symbol(i)) for i in j] for j in data["cells"]] 
       
        