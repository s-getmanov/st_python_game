from utils import rand, rand_cell, randbool, randtree, rand01, rand_101
from enum import Enum
import os
import json

TREE_BONUS      = 100
UPGREDE_COST    = 2000 
LIVE_COST       = 5000 
     
class Map(object): 

    class Map_cell(object):
        def __init__(self, sym):
            self.value =  sym  

    class Directions(Enum):
        TOP_DOWN = 1
        LEF_RIGHT = 2  
    
    def __init__(self, settings, helicopter, clouds):
        self.w = settings.w
        self.h = settings.h
        self.legend = settings.legend
        self.cells = [[self.Map_cell(self.legend.cell) for i in range(self.w)] for j in range(self.h)]
        self.level = settings.start_level
        self.helicopter = helicopter
        self.clouds = clouds
        
        self.generate_forest(30)
        self.generate_river(self.Directions.TOP_DOWN, 10)
        self.generate_river(self.Directions.LEF_RIGHT, 10)
        self.generate_upgrade_shop()
        self.generate_hospital()
    
    def setCell(self, h, w, value):
        if self.check_bounds(h, w):
            self.cells[h][w].value = value
        
    def getCell(self, h, w):
        if self.check_bounds(h, w):
            return self.cells[h][w].value
        return self.legend.border
        
    def __nextWaterCell(self, ch, cw, direction):
        
        if direction == self.Directions.TOP_DOWN:
           return (ch + rand01(), cw +  rand_101())
        else:
           return (ch +  rand_101(), cw + rand01())
    
    def isRiver(self, h, w):
        if self.check_bounds(h, w):
            return (self.getCell(h, w) == self.legend.water)
        return False
    
    def isTree(self, h, w):
        if self.check_bounds(h, w):
            c_cell = self.getCell(h, w)
            return ( c_cell == self.legend.tree1 or c_cell == self.legend.tree2 or c_cell == self.legend.tree3 )
        return False
    
    def isFire(self, h, w):
        if self.check_bounds( h, w):
            return (self.getCell(h, w) == self.legend.fire )
        return False
    
    def isUpShop(self, h, w):
        if self.check_bounds( h, w):
            return (self.getCell(h, w) == self.legend.upgrade )
        return False
    
    def isHospital(self, h, w):
        if self.check_bounds( h, w):
            return (self.getCell(h, w) == self.legend.hospital )
        return False
    
    def isCell(self, h, w):
        if self.check_bounds(h, w):
            return ( self.getCell(h, w) == self.legend.cell )
        return False

    def treeExist(self):
        for row in self.cells:
            for cell in row:
                if cell.value == (self.legend.tree1 or self.legend.tree2 or self.legend.tree3):
                    return True
        return False
    
    def cellExist(self):
        for row in self.cells:
            for cell in row:
                if cell.value == self.legend.cell:
                    return True
        return False

    def randtree(self):
        r = rand(1,3)
        if r == 1:
            return self.legend.tree1
        elif r == 2:
            return self.legend.tree2
        elif r == 3:
            return self.legend.tree3
        return self.legend.tree1 

    def print_status_bar(self, helicopter):
        print(f"{self.legend.barrel}{helicopter.tank}/{helicopter.max_tank} | {self.legend.score}{helicopter.score} | {self.legend.live}{helicopter.lives} |      {self.legend.level}{self.level}") 

    def print_map(self):
        self.process_helicopter(self.helicopter, self.clouds)
        self.print_status_bar(self.helicopter)
        print(self.legend.border*(self.w+2))
        ih = 0        
        for row in self.cells:
            print(self.legend.border, end = "")
            iw = 0
            for cell in row:
                if self.clouds.notNone(ih, iw):
                    print(self.clouds.getCell(ih, iw), end = "") 
                elif self.helicopter.h == ih and self.helicopter.w == iw:
                    print(self.legend.helic, end = "")
                else:
                    print(cell.value, end = "")
                iw +=1 
            print(self.legend.border, end = "")               
            print()
            ih +=1
        print(self.legend.border*(self.w+2))
                
    def check_bounds(self, x ,y):
        if (x < 0 or y < 0 or x >= self.h or y >= self.w):
            return False
        return True
    
    def generate_forest(self, probability):
        for row in self.cells:
            for cell in row:
                if randbool(probability):
                    cell.value = self.randtree()
    
    def generate_river(self, direction, min_area):
        #Река начинается с краю поля и продолжается до другого края. 
        # direction - указывает направление - сверху вниз или слева направо
        # min_area - минимальная площадь. Река генерируется или до достижения края, но если не достигнута минимальная площадь, генерацию продолжаем.        
        curr_area = 0       
        
        if direction == self.Directions.TOP_DOWN:
            rh = 0
            rw = rand(0,self.w-1)
        elif direction == self.Directions.LEF_RIGHT:
            rw = 0
            rh = rand(0,self.h-1)
        self.cells[rh][rw].value = self.legend.water

        while True:
            
            t_rh,t_rw = self.__nextWaterCell(rh, rw, direction)
            
            if not self.check_bounds(t_rh,t_rw): 
                if curr_area >= min_area:
                    break
                continue

            rh, rw = t_rh, t_rw
            if not self.isRiver(rh,rw):
                self.cells[rh][rw].value = self.legend.water 
                curr_area += 1

    def generate_tree(self):
        while True:
            if not self.cellExist():
                break
            th, tw = rand_cell(self.h, self.w)        
            if self.isCell(th, tw):
                self.setCell( th, tw, self.randtree())
                break
    
    def generate_fire(self):
        while True:
            if not self.treeExist():
                break
            th, tw = rand_cell(self.h, self.w)        
            if self.isTree(th, tw):
                self.setCell( th, tw, self.legend.fire)
                break
            
    def generate_upgrade_shop(self):
        while True:
            th, tw = rand_cell(self.h, self.w)
            if not self.isHospital(th, tw):
                self.setCell( th, tw, self.legend.upgrade)
                break

    def generate_hospital(self):
        while True:
            th, tw = rand_cell(self.h, self.w)
            if not self.isUpShop(th, tw):
                self.setCell( th, tw, self.legend.hospital)
                break

    def updateFire(self):
        for row in self.cells:
            for cell in row:
                if cell.value == self.legend.fire:
                   cell.value = self.legend.cell
        for i in range(self.level):
            self.generate_fire()

    def updateClouds(self):
        self.clouds.update(10, 3)

    def process_helicopter(self, helic, clouds):
        currenv_val = self.getCell(helic.h, helic.w)
        if currenv_val == self.legend.water:
            helic.fill_tank()
        elif currenv_val == self.legend.fire and helic.tank > 0:
            helic.tank -=1
            helic.score +=TREE_BONUS
            self.setCell(helic.h, helic.w, self.randtree())
        elif currenv_val ==  self.legend.upgrade and helic.score >=UPGREDE_COST:
            helic.max_tank +=1
            helic.score = helic.score - UPGREDE_COST
        elif currenv_val ==  self.legend.hospital and helic.score >=LIVE_COST:
            helic.lives +=100
            helic.score = helic.score - LIVE_COST
        
        if clouds.getCell(helic.h, helic.w) == clouds.legend.thundercloud:
           helic.lives -=1  
           if helic.lives <= 0:
               os.system("cls")
               print(f"Game over! You score is {helic.score}")
               exit(0)

    def level_up(self):
        self.level +=1

    def export_data(self):
        return {                
                "cells":[[self.legend.encode_symbol(i.value) for i in j] for j in self.cells] , 
                "level":self.level              
                }
    
    def import_data(self, data):
        self.cells =  [[ self.Map_cell(self.legend.decode_symbol(i)) for i in j] for j in data["cells"]] 
        self.level = data["level"] or 1

    def save_data(self, tick):
        data = {
            "map": self.export_data(),
            "helikopter":self.helicopter.export_data(),
            "clouds":self.clouds.export_data(),
            "tick":tick,
        }
        with open("level.json", "w", encoding='UTF-8') as lvl:
            json.dump(data, lvl)

    def load_data(self):
        with open("level.json", "r", encoding='UTF-8') as lvl:
            data = json.load(lvl)
            self.import_data(data["map"])
            self.helicopter.import_data(data["helikopter"])
            self.clouds.import_data(data["clouds"])
            tick = data["tick"] 
        return tick
    

