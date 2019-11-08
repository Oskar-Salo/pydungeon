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
        ">":"stair down",
        "<":"stair up",
        "A":"a good locking amulett"
            }
        


d1 = """
###################################################
#...>..........W................#......S#.........#
#.................................#####......###..#
#...#................S.....S......#.A.D...........#
###################################################
"""

d2 = """
###################################################
#...<......>..............S.......W.........W.....#
#....................#...........######..S........#
#..k#.#....S.....................#.A..D.......S...#
###################################################
"""

d3 = """
###################################################
#...>......<......W..........S.........S##.W#..k..#
#..............................########......#....#
#.....#.#.#.....W..............#A.d...D....W..W####
###################################################
"""

d4 = """
###################################################
#...<......>.......#............#.............W...#
#................S.##############....S....A.......#
#....W..................WS..................S.....#
###################################################
"""

d5 = """
###################################################
#.......S..<.......#.........S..W.......###########
#..######......#.....S..................DW.......A#
#.k#....#.S...............W.....####....####k######
###################################################
"""

# create levels
def create():        
    dungeon = []
    for z, d in enumerate((d1, d2, d3, d4, d5)):
        level = []
        for y, line in enumerate(d.splitlines()):
            row = []
            for x, char in enumerate(list(line)):
                if char == "W":
                    row.append(".")
                    Wolf(x,y,z)
                elif char == "S":
                    row.append(".")
                    Snake(x,y,z)
                elif char == "d":
                    row.append(".")
                    Dragon(x,y,z)
                elif char == "D":
                    row.append(".")
                    Door(x,y,z)
                else:
                    row.append(char)
            level.append(row)
        dungeon.append(level)
    return dungeon
        
def opendoor(player, door):
    if player.keys > 0:
        player.keys -= 1
        print("you use one of your keys to open the door")
        door.hitpoints = 0
        return
    print("You must find a key (k) to open the door")
        

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
        self.char = "M"
        self.hitpoints = 100
        self.overwrite_parameters()
        
    def ai(self):
        dx, dy = 0,0
        if random.random() < 1: #0.45
            dx, dy = random.choice(((1,1), (1,0), (1,-1),
                                    (0,1), (0,0), (0,-1),
                                    (-1,1), (-1,0), (-1,-1)))
        return dx, dy
        
    def overwrite_parameters(self):
        pass

class Door(Monster):
    
    def overwrite_parameters(self):
        self.hitpoints = 15
        self.char = "D"
    
    def ai(self):
        return 0,0
        
class Hero(Monster):
    
    def overwrite_parameters(self):
        self.hitpoints = 1
        self.char = "@"
        self.keys = 4
        self.amulets = 0
        self.attack = (4, 5) # 4 dice, each die has five sides
        self.attack_bonus =  100 #3
        self.defense = (2, 6)
        self.defense_bonus = 1
        self.damage = (2, 10)
        self.damage_bonus = 100 #3
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
        
class Dragon(Monster):
    def overwrite_parameters(self):
        self.hitpoints = 45
        self.char = "d"
        self.attack = (4, 3) # 4 dice, each die has three sides
        self.attack_bonus = 1
        self.defense = (3, 5)
        self.defense_bonus = 2
        self.damage = (3, 3)
        self.damage_bonus = 2

def fight(attacker, defender):
    """strike and counterstrike"""
    print("--- strike ---")
    strike(attacker, defender)
    if defender.hitpoints > 0:
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
    dungeon = create()
    
    # ------
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
            if target == "#" or target == "D":
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
                        fight(m2, player)
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
                    print(char, end="")
            print() # end of line
        # --- status ---
        status = "hitpoints: {} keys: {}  amulets: {} (x:{} y:{} z:{})".format(
                  player.hitpoints, player.keys, player.amulets,
                  player.x, player.y, player.z)
        command = input(status + " >>>")
        dx, dy = 0, 0
        if command == "quit":
            break
        if command == "up" and player.z > 0:
            if dungeon[player.z][player.y][player.x] == "<":
                player.z -= 1
            else:
                print("you need to find a stair up (<)")
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
        if target == "#":
            print("Oouch!")
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
                    opendoor(player, m)
                    dx, dy = 0, 0
                elif m.__class__.__name__ == "Treasure":
                    opentreasure(player, m)
                    dx, dy = 0, 0
                elif m.__class__.__name__ in ["Wolf", "Snake", "Dragon"]:
                    fight(player, m)
                    dx, dy = 0, 0
                break
        # ---- movement ------
        player.x += dx
        player.y += dy
        # ----- found something? -----
        pos = dungeon[player.z][player.y][player.x]
        if pos == "k":
            print("i found a key!")
            dungeon[player.z][player.y][player.x] = "."
            player.keys += 1
        if pos == "A":
            print("i found an amulett")
            dungeon[player.z][player.y][player.x] = "."
            player.amulets += 1
            if player.amulets == 5:
                player.finished = True
                #return
        if pos == "<":
            print("i found a stair up. you can use the UP command")
        if pos == ">":
            print("i found a stair down. you can use the DOWN command")
    
    # ========= end of game loop ===========
    print("Game Over")        
    if player.hitpoints < 1:
        print("You failed your quest and you are not very healthy. Actually, you died.")
    elif player.finished:
        print("You got all five amulets. Your job here is done!")
    else:
        print("You failed your quest, but you're alive. Still you are a looser.")
    
        
game()
        
                    
                
                        
    
    
    
        
    
    
