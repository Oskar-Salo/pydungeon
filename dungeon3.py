""" a roguelike game using pure python3"""

import random

# raw level 

legend = {
        ".":"empty space",
        "#":"a solid wall",
        "D":"a door",
        "W":"a dangerous wolf",
        "S":"a poisonous snake",
        "d":"a huge dragon",
        "@":"the player",
        "k":"a key to open a door",
        ">":"a stair down",
        "<":"a stair up",
        "A":"a good locking amulett",
        "G":"a stone golem",
        "s":"a sharp sword",
        "/":"a pointy spear",
        "0":"a hard shield",
        "q":"a heavy mace"
            }
        
def create_textlevel(maxx=80, maxy=24):
    legend = {".":"floor",
                   "#":"wall",
                   "~":"outer wall",
                   "$":"shop",
                   }
    level = []
    for y in range(maxy):
        line = []
        for x in range(maxx):
            line.append("#") # fill everything with walls
        level.append(line)
    # --- outer walls [~] ---
    for y in range(maxy):
        for x in range(maxx):
            if y== 0 or y == maxy-1: 
                level[y][x] = "~"
            elif x == 0 or x == maxx- 1:
                level[y][x] = "~"
    
    #- -- create 10 rooms (or try it) ----
    for _ in range(6):
        Room(xmin=1, xmax=maxx-2,ymin=1, ymax=maxy-2)
    # --- fill rooms with floor tiles ---
    for r in Room.book.values():
        for y in range(r.y1, r.y2):
            for x in range(r.x1, r.x2):
                level[y][x] = "." # str(r.number)
    # --- connect rooms with corridors 
    maxr = len(Room.book)
    for number in range(maxr-1):
        print("processing room number", number)
        r = Room.book[number]
        r2= Room.book[number + 1]
        
        #mid1 = [ (r.x1+r.x2)//2, (r.y1+r.y2)//2 ]
        #mid2 = [ (r2.x1+r2.x2)//2, (r2.y1+r2.y2)//2 ]
        mid1 = [random.randint(r.x1, r.x2), random.randint(r.y1,r.y2)]
        mid2 = [random.randint(r2.x1, r2.x2), random.randint(r2.y1,r2.y2)]
        #---- make corridor ---
        x1 = mid1[0]
        y1 = mid1[1]
        x2 = mid2[0]
        y2 = mid2[1]
        
        # - search left room 
        if x1 < x2:
            dx = 1
        else:
            dx = -1
        if y1 < y2:
            dy = 1
        else:
            dy = -1
        # --- crawl the corridor ---
        x = x1
        y = y1
        print("dx,dy",dx,dy)
        
        while not (x == x2 and y == y2):
            
            if x != x2:
                x += dx
            if y != y2 and random.random() < 0.1:
                level[y][x] = "."
                y += dy
            level[y][x] = "."
    return level



# create levels
def make_monsters(dungeon):        
    #dungeon = []
    for z, d in enumerate(dungeon):
        #level = []
        for y, line in enumerate(d):
            #row = []
            for x, char in enumerate(line):
                #print("monstermaking", x,y,z, char)
                if char == ".":
                    # create a monster
                    if random.random() < 0.03:
                        what = random.choice(("wolf", "wolf", "wolf", "snake", "snake","golem"))
                        if what == "wolf":
                            Wolf(x,y,z)
                        elif what == "snake":
                            Snake(x,y,z)
                        elif what == "golem":
                            Golem(x,y,z)
                    elif random.random() < 0.01:
                        what = random.choice(("mace","shield","spear","sword"))
                        if what == "mace":
                            Mace(x,y,z)
                        elif what == "shield":
                            Shield(x,y,z)
                        elif what== "spear":
                            Spear(x,y,z)
                        elif what == "sword":
                            Sword(x,y,z)
                    else:
                        # -- check if this is a place to create a door ----
                        if (((dungeon[z][y-1][x] == "#" and dungeon[z][y+1][x] == "#") and
                            (dungeon[z][y][x-1] == "." and dungeon[z][y][x+1] == ".")) or
                           ((dungeon[z][y][x-1] == "#" and dungeon[z][y][x+1] == "#") and
                            (dungeon[z][y-1][x] == "." and dungeon[z][y+1][x] == "."))):
                                if random.random() < 0.05:
                                    Door(x,y,z)
def opendoor(player, door):
    if player.keys > 0:
        player.keys -= 1
        #print("you use one of your keys to open the door")
        message += "you use one of your keys to open the door "
        door.hitpoints = 0
        return
    #print("You must find a key (k) to open the door")
    message += "You must find a key (k) to open the door "
        


class Item():

    number = 0
    store = {}
   
    def __init__(self, x=1, y=1, z=1, carrier=None):
        self.number = Item.number
        Item.number += 1
        Item.store[self.number] = self
        # location 
        self.carrier = carrier
        self.x = x
        self.y = y
        self.z = z
        # bonus
        self.damage_bonus = 0
        self.attack_bonus = 0
        self.defense_bonus = 0
        self.char = "x"
        self.protection = 0
        self.quality = round(random.gauss(0.75, 0.05), 2)
        self.quality = min(1, self.quality)
        self.quality = max(0, self.quality)
        
        self.bonus = int(round(random.gauss(0, 0.6), 0))
        self.overwrite_parameters()
       
    def overwrite_parameters():
        pass

    def __str__(self):
        msg = "\n--------------------{}--------------------------------".format(self.__class__.__name__)
        msg += "\nmy quality is {}%".format(self.quality * 100)
        msg += "\nmy BONUS is " + str(self.bonus)
        msg += "\ndamage = {} {} {} = {}".format(self.damage_bonus, "-" if self.bonus<0 else "+", abs(self.bonus), self.damage_bonus+self.bonus)
        msg += "\ndefense = {} {} {} = {}".format(self.defense_bonus, "-" if self.bonus<0 else "+", abs(self.bonus), self.defense_bonus+self.bonus)
        msg += "\nattack = {} {} {} = {}".format(self.attack_bonus, "-" if self.bonus<0 else "+", abs(self.bonus), self.attack_bonus+self.bonus)
        return msg
        

class Sword(Item):
    
    def overwrite_parameters(self):
        self.char = "s"
        self.attack_bonus = 1
        self.defense_bonus = 2
        self.damage_bonus = 5
       
       
class Spear(Item):
    
    def overwrite_parameters(self):
        self.char = "/"
        self.attack_bonus = 1
        self.defense_bonus = 4
        self.damage_bonus = 2
        #self.protection = 1
        
class Mace(Item):
    
    def overwrite_parameters(self):
        self.char = "q"
        self.attack_bonus = -2
        self.defense_bonus = 1
    
        self.damage_bonus = 5
          
        #self.protection = 2
        
class Shield(Item):
    
    def overwrite_parameters(self):
        self.char="0"
        self.defense_bonus = -1
        self.protection = 6
        
class Monster():
    
    number = 0
    zoo = {}
    
    def __init__(self, x,y,z):
        self.number = Monster.number
        Monster.number += 1
        Monster.zoo[self.number] = self
        self.x = x
        self.y = y
        self.z = z
        self.agility = 0.2
        self.char = "M"
        self.hitpoints = 100
        self.overwrite_parameters()
        
    def ai(self):
        dx, dy = 0,0
        if random.random() < self.agility: #0.45
            dx, dy = random.choice(((1,1), (1,0), (1,-1),
                                    (0,1), (0,0), (0,-1),
                                    (-1,1), (-1,0), (-1,-1)))
        return dx, dy
        
    def overwrite_parameters(self):
        pass


class Room():
    """room in a text array, y axis start with 0 and goes positive down (like pygame)"""
    
    number = 0
    book = {} # dict for all rooms, key is the room number, value is the room instance
    
    def __init__(self, z=0, xmin=0, ymin=0, xmax=100, ymax=100, maxwidth=15, maxheight=10, minheight=3, minwidth=3):
        #self.number = Room.number
        #Room.book[self.number] = self
        #Room.number += 1
        number = Room.number
        
        for v in range(1000):
            print("trying to create room number ", self.number, "attempt ",v)
            x1 = random.randint(xmin, xmax)
            y1 = random.randint(ymin, ymax)
            x2 = x1 + random.randint(minwidth, maxwidth)
            y2 = y1 + random.randint(minheight, maxheight)
            if x2 > xmax or y2 > ymax:
                continue # out of dungeon limits
            print(x1,y1,x2,y2)
            # -- check for intersection with other rooms ---
            ok = True
            for r in Room.book.values():
                if r.number == number:
                    continue
                if r.z != z:
                    continue 
                print("testing with", r.x1, r.y1, r.x2, r.y2)
                ## I must test EACH border piece of one rect if it is inside the other rect
                for y in range(y1, y2+1):
                    for x in range(x1, x2+1):
                        if y1 < y < y2 and x1 < x < x2:
                            continue
                        if r.x1 <= x <= r.x2 and r.y1 <= y <= r.y2:
                            ok = False
                if not ok:
                    break 
            else:
                # good room
                print("room created with:", x1,y1,x2,y2)
                self.number = Room.number
                Room.book[self.number] = self
                Room.number += 1
                self.x1, self.y1, self.x2, self.y2 = x1,y1,x2,y2
                self.z = z
                break
        else:
            print("unable to create (another) room...")
            




class Door(Monster):
    
    def overwrite_parameters(self):
        self.hitpoints = random.choice((100,100,100,100,110,120,125,140,150,150,175))
        self.attack = (0, 1)
        self.defense = (1, 6)
        self.attack_bonus = 0
        self.defense_bonus = 3
        self.damage = (0,1)
        self.damage_bonus = 0
        self.char = "d"
    
    def ai(self):
        return 0,0
        
class Hero(Monster):
    
    def overwrite_parameters(self):
        self.hitpoints = 100
        self.char = "@"
        self.keys = 0
        self.amulets = 0
        self.attack = (4, 5) # 4 dice, each die has five sides
        self.attack_bonus =  3
        self.defense = (2, 6)
        self.defense_bonus = 1
        self.damage = (2, 10)
        self.damage_bonus = 3
        self.finished = False
        
        
class Wolf(Monster):
    
    def overwrite_parameters(self):
        self.hitpoints = 30
        self.char = "W"
        self.attack = (2, 6) # 2 dice, each die has six sides
        self.attack_bonus = 2
        self.defense = (2, 6)
        self.defense_bonus = 2
        self.damage = (2, 4)
        self.damage_bonus = 1
        self.agility = 0.4
        
class Snake(Monster):
    def overwrite_parameters(self):
        self.hitpoints = 20
        self.char = "S"
        self.attack = (2, 4) # 2 dice, each die has four sides
        self.attack_bonus = 2
        self.defense = (3, 3)
        self.defense_bonus = 2
        self.damage = (3, 4)
        self.damage_bonus = 1
        self.agility = 0.25
        
class Dragon(Monster):
    def overwrite_parameters(self):
        self.hitpoints = 45
        self.char = "D"
        self.attack = (4, 3) # 4 dice, each die has three sides
        self.attack_bonus = 1
        self.defense = (3, 5)
        self.defense_bonus = 2
        self.damage = (3, 3)
        self.damage_bonus = 2
        self.agility = 0.3
        
class Golem(Monster):
    def overwrite_parameters(self):
        self.hitpoints = 50
        self.char = "G"
        self.attack = (2, 4)
        self.attack_bonus = 1
        self.defense = (2, 4)
        self.defense_bonus = 2
        self.damage = (2, 4)
        self.damage_bonus = 1
        self.agility = 0.1

def fight(attacker, defender):
    """strike and counterstrike"""
    print("--- strike ---")
    strike(attacker, defender)
    if defender.hitpoints > 0:
        if defender.attack[0] == 0:
            print("no counterstrike because 0 attack die ")
        else:
            print("--- counterstrike ---")
            strike(defender, attacker)
        
def strike(a, d):
    """a = attacker, d = defender"""
    namea= a.__class__.__name__
    named= d.__class__.__name__
    print("{} strikes at {}".format(namea, named))
    print("attack value:")
    attack_a = roll(a.attack, a.attack_bonus)
    print("defense value:")
    defend_d = roll(d.defense, d.defense_bonus)
    # --- hit? ---
    if attack_a <= defend_d:
        print("{} <= {}: miss.....".format(attack_a, defend_d))
        input("press enter to continue....")
        return
    print("{} > {}: hit!!!! ".format(attack_a, defend_d))
    input("press enter to continue....")
    # ---- damage ----
    print("calculating damage...")
    damage = roll(a.damage, a.damage_bonus)
    d.hitpoints -= damage
    print("{} looses {} hp and has only {} hp left".format(
          named, damage, d.hitpoints))
    input("press enter to continue....")
    
def roll(dice, bonus=0):
    rolls = dice[0]
    sides = dice[1]
    total = 0
    print("-----------------------")
    print("rolling {}d{} + bonus {}".format(rolls, sides, bonus))
    print("-----------------------")
    for d in range(rolls):
        value = random.randint(1, sides)
        print("rolling die #{}:....{} ".format(d, value))
        total += value
    print("==================")
    print("=result:    {}".format(total))
    print("+bonus:     {}".format(bonus))
    print("==================")
    print("=total:     {}".format(total+bonus))
    return total+bonus
        
    
        
    
    
    
def game():
    player = Hero(1,2,0)
    #dungeon = create()
    dungeon = [] 
    dungeon.append(create_textlevel()) #level 0
    dungeon.append(create_textlevel()) #level 1
    #dungeon.append(create_textlevel()) #level 2    
    #dungeon.append(create_textlevel()) #level 3
    #print("jetzt gehts los.....")
    make_monsters(dungeon)
    #print("Monster gemacht")
    # ------
    # place hero on empty field in level 0
    found = False
    for y, line in enumerate( dungeon[0]):
        for x, char in enumerate(line):
            if char == ".":
                player.x = x
                player.y = y
                found = True
                break
        if found:
            break
    else:
        print("error, no place for player found")
        
    
    message = ""
    while player.hitpoints > 0 and not player.finished :
        #-------------move the monsters------------
        for m in Monster.zoo.values():
            if m.number == player.number:
                continue
            if m.hitpoints < 1:
                continue
            if m.z != player.z:
                continue
            dx, dy = m.ai()
            target = dungeon[m.z][m.y+dy][m.x+dx]
            #-- wall check-----
            if target == "#" or target == "D" or target == "~":  
                continue
            #---- other monster---
            for m2 in Monster.zoo.values():
                if m2.number == m.number:
                    continue
                if m2.hitpoints <1:
                    continue
                if m2.z != m.z:
                    continue
                #is this other m2 monster in the way
                if m2.y == m.y +dy and m2.x == m.x+dx:
                    dx, dy = 0, 0
                    if m2.number == player.number:
                        fight(m, player)
                    break
                    
                    
            #-----monster can move-----
            m.x += dx
            m.y += dy
        #-------------graphic engine---------------
        for y, line in enumerate(dungeon[player.z]):
            for x, char in enumerate(line):
                # Monster ? 
                for m in Monster.zoo.values():
                    if m.hitpoints <= 0:
                        continue
                    if m.z == player.z and m.y==y and m.x == x:
                        print(m.char, end="")
                        break
                else:
                    # Item ?
                    for i in Item.store.values():
                        if i.carrier is not None:
                            continue
                        if i.z == player.z and i.y == y and i.x == x:
                            print(i.char, end="")
                            break
                    else:   # print dungeon tile 
                        if char == "~":   # display outer wall as wall
                            c = "#"
                        else:
                            c = char
                        print(c, end="")
            print() # end of line
        # --- status ---
        status = "hp: {} keys: {}  amulets: {}  {}".format(
                  player.hitpoints, player.keys, player.amulets,message)
        message = ""
        command = input(status + " >>>")
        dx, dy = 0, 0
        if command == "quit":
            break
        if command == "up" and player.z > 0:
            if dungeon[player.z][player.y][player.x] == "<":
                player.z -= 1
            else:
                #print("you need to find a stair up (<)")
                message += "you need to find a stair up (<) "
        if command == "down" and player.z < len(dungeon) - 1:
            if dungeon[player.z][player.y][player.x] == ">":
                player.z += 1
            else:
                print("you need to find a stair down (>)")
        if command == "w":
            dy = -1
        if command == "s":
            dy = 1
        if command == "a":
            dx = -1
        if command == "d":
            dx = 1
        # ---- collision test with wall ----
        target = dungeon[player.z][player.y + dy][player.x + dx] 
        if target == "#" or target == "~":
            message += "Ouch! "
            player.hitpoints -= 1
            dx, dy = 0, 0
        
        # ----- collision test with other monster -----
        for m in Monster.zoo.values():
            if m.hitpoints <= 0:
                continue
            if m.number == player.number:
                continue
            if m.z != player.z:
                continue
            if player.y + dy == m.y and player.x + dx == m.x:
                # crash
                if m.__class__.__name__ == "Door":
                    #opendoor(player, m)
                    fight(player, m) # fight the door!
                    dx, dy = 0, 0
                elif m.__class__.__name__ == "Treasure":
                    opentreasure(player, m)
                    dx, dy = 0, 0
                elif m.__class__.__name__ in ["Wolf", "Snake", "Dragon", "Golem"]:
                    fight(player, m)
                    dx, dy = 0, 0
                break
        # ---- movement ------
        player.x += dx
        player.y += dy
        # ----- found something? -----
        pos = dungeon[player.z][player.y][player.x]
        
        #  --- stairs -----
        if pos == "<":
            #print("i found a stair up. you can use the UP command")
            message += "i found a stair up. you can use the UP command "
        if pos == ">":
            #print("i found a stair down. you can use the DOWN command")
            message += "i found a stair down. you can use the DOWN command "
        # ---- pick up item(s) -----
        for i in Item.store.values():
            if i.carrier is not None:
                continue
            if i.z == player.z and i.y == player.y and i.x == player.x:
                message += "\nyou pick up an item!"
                i.carrier = player.number
        
    # ========= end of game loop ===========
    print("Game Over")        
    if player.hitpoints < 1:
        print("You failed your quest and you are not very healthy. Actually, you died.")
    elif player.finished:
        print("You got all five amulets. Your job here is done!")
    else:
        print("You failed your quest, but you're alive. Still you are a looser.")
    


if __name__ == "__main__":
    game()
        
                    
                
                        
    
    
    
        
    
    
