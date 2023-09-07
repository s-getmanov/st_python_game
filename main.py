
from pynput import keyboard

from map import Map
from clouds import Clouds
import time
import os
from helicopter import Helicopter as Helic

MAP_SIZE = (10, 20)
TICK_SLEEP = 0.024
TREE_UPDATE = 100
FIRE_UPDATE = 200
CLOUDS_UPDATE = 300
LEVEL_UP_TIME = 10000
MOVES = {
    'w':(-1,0),
    'd':(0,1),
    's':(1,0),
    'a':(0,-1),
    'a':(0,-1),
    }
class Legend(object):  

    def __init__(self):        
        self.symbols = []

    def encode_symbol(self, symbol):
        return self.symbols.index(symbol)

    def decode_symbol(self, index):
        return self.symbols[index]  

class Legend(Legend):
    def __init__(self):
        #Если поместить в строку - получим проблемы с индексацией символов. Поэтому поместим в список 
        self.symbols = ["🟫", "🟩","🌲","🌳","🌴","🌊","🚑","🏭","🔥","🚁","🛢️","🏆","🚀","🧡"]
        #Для удобства работы с символами продублируем в свойства объекта
        self.border = self.symbols[0]
        self.cell = self.symbols[1]
        self.tree1 = self.symbols[2]
        self.tree2 = self.symbols[3]
        self.tree3 = self.symbols[4]
        self.water = self.symbols[5]
        self.hospital = self.symbols[6]
        self.upgrade = self.symbols[7]
        self.fire = self.symbols[8]
        self.helic = self.symbols[9]
        self.barrel = self.symbols[10]
        self.score = self.symbols[11]
        self.level = self.symbols[12]
        self.live = self.symbols[13]

class LegendClouds(Legend):
    def __init__(self):
        self.symbols = ["⛅", "⚡", " "]
        self.none = " "
        self.cloud = "⛅"  
        self.thundercloud = "⚡"
   
class Settings(object):
    def __init__(self, h ,w, start_level, legend):
        self.w = w
        self.h = h
        self.legend = legend
        self.start_level = start_level
        
currentLegend = Legend()
currentCloudsLegend = LegendClouds()
currenSettings = Settings(*MAP_SIZE, 1, currentLegend)

helic = Helic(20, 20, currentLegend)
clouds = Clouds(*MAP_SIZE, currentCloudsLegend)
game_map = Map(currenSettings, helic, clouds)

tick = 1

def on_release(key):
    global helic, game_map, tick
    comm = key.char.lower()
    if comm in MOVES.keys():
        helic.mave_to(*MOVES[comm])
    elif comm == "f":
        game_map.save_data(tick)
    elif comm == "g":
        tick = game_map.load_data()

keyboard_listener = keyboard.Listener(
   on_press     = None,
   on_release   = on_release
)

keyboard_listener.start()

while True:
    os.system("cls")    
  
    game_map.print_map()       

    tick +=1
    time.sleep(TICK_SLEEP) 

    if tick % TREE_UPDATE == 0:
        game_map.generate_tree()
       
    if tick % FIRE_UPDATE == 0:      
        game_map.updateFire()

    if tick % CLOUDS_UPDATE == 0:      
        game_map.updateClouds()

    #Добавим увеличение сложности игры через количество тиков LEVEL_UP_TIME.
    if tick % LEVEL_UP_TIME == 0:      
        game_map.level_up()




