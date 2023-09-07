from utils import rand_cell

class Helicopter(object):
    def __init__(self, h, w, currentLegend):
        th, tw = rand_cell(h, w)
        self.h = th
        self.w = tw
        self.h_size = h
        self.w_size = w
        self.tank = 0
        self.max_tank = 1
        self.legend = currentLegend 
        self.score = 0   
        self.lives = 20    
    
    def mave_to(self, dh, dw):
        nh, nw = self.h + dh, self.w + dw
        if (nh>=0 and nw>=0 and nh<self.h_size and nw<self.w_size):
            self.h, self.w = nh, nw
            
    def fill_tank(self):
         self.tank = self.max_tank
  
    def export_data(self):
        return {"h":self.h,
                "w":self.w,
                "tank":self.tank,
                "max_tank":self.max_tank,
                 "score":self.score,
                 "lives":self.lives,            
                }
    
    def import_data(self, data):
        self.h = data["h"] or 0
        self.w = data["w"] or 0
        self.tank = data["tank"] or 0
        self.max_tank = data["max_tank"] or 1
        self.score = data["score"]  or 0 
        self.lives = data["lives"]  or 20
