import random
import time
import os

size = int(input("マップの一辺:"))

map = {}#{(x,y):stat} stat...0,1,-1 -1は何もない

for x in range(size):
    for y in range(size):
        map[(x,y)] = -1 #初期状態はなし

for i,x in enumerate([0,size-1]):
    for y in range(size):
        map[x,y] = i #両方に数字を

def move(map, target, enm, danger_zone=None):
    directions = [(1,0), (-1,0), (0,1), (0,-1)]
    enm_locs = [k for k,v in map.items() if v == enm] if enm is not None else None

    for direction in directions:
        pretarget = tuple(x + y for x, y in zip(target, direction))
        if danger_zone and pretarget in danger_zone:
            continue
        if enm_locs and pretarget in enm_locs:
            return pretarget

    for direction in random.sample(directions, 4):
        pretarget = tuple(x + y for x, y in zip(target, direction))
        if danger_zone and pretarget in danger_zone:
            continue
        if pretarget not in map:
            continue
        if map[pretarget] in [enm, -1]:
            return pretarget

    return None

    
#-動かす処理-
count = 0
while True:
    count += 1
    for n in range(2):

        enm = 0 if n == 1 else 1 #enm = 敵の数字
        targets = [k for k,v in map.items() if v == n] #チームメンバーの座標全取得

        print(f"{"青"if n == 0 else "赤"}:{len(targets)}")

        if not targets: #全滅
            input(f"{"青"if enm == 0 else "赤"}チームの勝利。:")

        
        for target in random.sample(targets, (len(targets) // 1) if len(targets) != 1 else 1): #総数の半分を動かす
            new_pos = move(map, target, enm)
            pretarget = new_pos if new_pos is not None else target

            map[target] = -1 #移動元の場所は殻に
            map[pretarget] = n
        
    time.sleep(0.1)
    os.system("cls" if os.name == "nt" else "clear")

        #-出力-
    output = ""
    for y in range(size):
        line = ""
        for x in range(size):
            if (x,y) not in map:
                line += "　"
                continue

            value = map[(x, y)]
            if value == 0:
                line += "\033[34m■\033[0m"  # 青
            elif value == 1:
                line += "\033[31m■\033[0m"  # 赤
            else:
                line += "■"  # 色なし
        line += "\n"
        output += line

    print(output)

    if count % 20 == 0:
        ind = int((count / 20) - 1)
        blue = [k for k,v in map.items() if v == 0]
        red =  [k for k,v in map.items() if v == 1]

        danger_zone = set()
        for x in range(size):
            for y in range(size):
                if x == ind or y == ind or x == size-ind-1 or y == size-ind-1:
                    danger_zone.add((x, y))

        premap = map.copy()

        for team, color in [(blue, 0), (red, 1)]:
            enm = 1 - color
            for target in team:
                if target in danger_zone:
                    if target in map:
                        del map[target]
                        new_pos = move(premap, target, enm, danger_zone)
                        map[new_pos if new_pos is not None else target] = color

        for pos in danger_zone:
            map.pop(pos, None)
                            
