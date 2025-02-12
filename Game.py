import random as rd


#run the code to initate a game, genarate map
def gameInit():
    global playerCurrent
    global map

    spawnTile = [rd.randrange(1, mapScale[0] -1), rd.randrange(1, mapScale[1] -1)]
    playerCurrent = spawnTile
    for i in range(mapScale[0]):
        map.append([])
        for j in range(mapScale[1]):
            map[i].append({
                'north':'wall' if i == 0 else '',
                'east':'wall' if j == mapScale[1] - 1 else '',
                'south':'wall' if i == mapScale[0] - 1 else '',
                'west':'wall' if j == 0 else ''
            })

    routeOrigins = [spawnTile]
    for cR in range(cRQuantity):
        originCell = rd.choice(routeOrigins)
        prevCD = ''
        extendRoute = True
        for i in range(rd.randrange(cRTargetLength-cRLengthVariance,cRTargetLength+cRLengthVariance)):
            dirops = [['north',-1,0,'south'],['east',0,1,'west'],['south',1,0,'north'],['west',0,-1,'east']]
            while True:
                dir = rd.choice(dirops) if len(dirops) > 0 else 'break'
                if dir != 'break':
                    if dir[0] == prevCD or map[originCell[0]][originCell[1]][dir[0]] != '':
                        dirops.remove(dir)
                    else: break
                else:
                    extendRoute = False
                    break
            if extendRoute:
                map[originCell[0]][originCell[1]][dir[0]] = 'passageWay'
                prevCD = dir[3]
                routeOrigins.append([originCell[0] + dir[1], originCell[1] + dir[2]])
                originCell[0] += dir[1]
                originCell[1] += dir[2]

#code used to interprate player commands
def readCommands(userInput, expectedCommands, displyError = False):
    commands = expectedCommands
    result = []
    p = 0
    if len(userInput.split()) != 0:
        while True:
            for i in range(len(userInput.split()[p])):
                invalids = []
                for testCommand in commands:
                    if userInput.split()[p].lower()[:i+1] != (testCommand[:i+1] if type(testCommand) == str else testCommand[0][:i+1]): invalids.append(testCommand)
                for inv in invalids: commands.remove(inv)
            if len(commands) == 1:
                if type(commands[0]) == str:
                    result.append(commands[0])
                    return result
                    break
                else:
                    result.append(commands[0][0])
                    commands = commands[0][1]
                    p += 1
                    if len(userInput.split()) < p+1:
                        if displyError: print('!!!additional argument expexted!!!')
                        return 'notFound'
                        break
            else:
                if displyError: print('!!!argument not collapsed!!!')
                return 'notFound'
                break
    else:
        if displyError: print('!!!no value given!!!')
        return 'notFound'

#weighted random
def weightedChoice(choices, weights):
    if len(weights) == len(choices):
        temp = []
        for w in range(len(weights)):
            for v in range(weights[w]):
                temp.append(choices[w])
        return rd.choice(temp)
    else: print('!!!given weights do not match choices!!!')

#displays the map for the player
def disMap():
    output = ''
    for y in range(mapScale[0]):
        for l in range(4):
            for x in range(mapScale[1]):
                explored = True if map[y][x]['north'] != '' and map[y][x]['east'] != '' and map[y][x]['south'] != '' and map[y][x]['west'] != '' else False
                if l == 0:
                    output += '\u250F' if explored else ' '
                    if explored:
                        if map[y][x]['north'] == 'passageWay': output += '\u251B  \u2517'
                        elif map[y][x]['north'] == 'wall': output += '\u2501'*4
                        elif map[y][x]['north'] == 'unopenedTreasure': output += '\u2501\u2588\u2588\u2501'
                        else: output += '    '
                    else: output += '    '
                    output += '\u2513' if explored else ' '
                elif l == 1:
                    if explored:
                        if map[y][x]['west'] == 'passageWay': output += '\u251B'
                        elif map[y][x]['west'] == 'wall': output += '\u2503'
                        elif map[y][x]['west'] == 'unopenedTreasure': output += '\u2588'
                        else: output += ' '
                    else: output += ' '
                    output += ' \u256D\u256E ' if [y,x] == playerCurrent else '    '
                    if explored:
                        if map[y][x]['east'] == 'passageWay': output += '\u2517'
                        elif map[y][x]['east'] == 'wall': output += '\u2503'
                        elif map[y][x]['east'] == 'unopenedTreasure': output += '\u2588'
                        else: output += ' '
                    else: output += ' '
                elif l == 2:
                    if explored:
                        if map[y][x]['west'] == 'passageWay': output += '\u2513'
                        elif map[y][x]['west'] == 'wall': output += '\u2503'
                        elif map[y][x]['west'] == 'unopenedTreasure': output += '\u2588'
                        else: output += ' '
                    else: output += ' '
                    output += ' \u2570\u256F ' if [y,x] == playerCurrent else '    '
                    if explored:
                        if map[y][x]['east'] == 'passageWay': output += '\u250F'
                        elif map[y][x]['east'] == 'wall': output += '\u2503'
                        elif map[y][x]['east'] == 'unopenedTreasure': output += '\u2588'
                        else: output += ' '
                    else: output += ' '
                else:
                    output += '\u2517' if explored else ' '
                    if explored:
                        if map[y][x]['south'] == 'passageWay': output += '\u2513  \u250F'
                        elif map[y][x]['south'] == 'wall': output += '\u2501'*4
                        elif map[y][x]['south'] == 'unopenedTreasure': output += '\u2501\u2588\u2588\u2501'
                        else: output += '    '
                    else: output += '    '
                    output += '\u251B' if explored else ' '
            output += '\n'
    print(output)

#fills in missing infrmation of a given tile
def genTile(pos):
    for cD in (
        ['north',-1,0,'south'],
        ['east',0,1,'west'],
        ['south',1,0,'north'],
        ['west',0,-1,'east']):
        if map[pos[0]][pos[1]][cD[0]] == '':
            if map[pos[0]+cD[1]][pos[1]+cD[2]][cD[3]] == 'passageWay':
                wallOp = 'passageWay'
            else: 
                while True:
                    wallOp = weightedChoice(wallGen, weights)
                    if map[pos[0]+cD[1]][pos[1]+cD[2]][cD[3]] == '' or wallOp != 'pasageWay': break
            map[pos[0]][pos[1]].update({
                cD[0] : wallOp
                })
            if wallOp == 'passageWay':
                map[pos[0]+cD[1]][pos[1]+cD[2]][cD[3]] = 'passageWay'

#gives a summary of the contents of the tile
def roomRead(pos):
    loc = map[pos[0]][pos[1]]
    for i in loc:
        print(f'To your {i} is a  {loc[i]} ')

#allows the player to gen stats
def pointBuyStats(basePoints, pointsPool, min=0, max=None):
    global playerStats
    pool = pointsPool
    cont = True
    for s in playerStats:
        playerStats[s] = basePoints
    while cont:
        it = 1
        for i in playerStats:
            print(f'| {i} | > {playerStats[i]}')
            it += 1
        print(f'\n[{pool}] point remaining\n')
        while True:
            if pool == 0:
                endPB = readCommands(input('Are you finished? [yes/no] >> '), ['yes', 'no'])
                if endPB[0] == 'yes':
                    cont = False
                    break
            while True:
                acceptedResponces = [['add', []], ['remove', []]]
                for s in playerStats:
                    acceptedResponces[0][1].append(s)
                    acceptedResponces[1][1].append(s)
                pInput = readCommands(input(' [add/remove] >> '), acceptedResponces)
                if pInput != 'notFound': break
            if pInput[0] == 'add' and pool > 0:
                if max != None:
                    if playerStats[1] < max:
                        playerStats[pInput[1]] += 1
                        pool -= 1
                    else: print(f'Points can not be above {max}')
                else:
                    playerStats[pInput[1]] += 1
                    pool -= 1
            elif pInput[0] == 'add' and pool == 0:
                print('You do not have any points remaining')
            elif pInput[0] == 'remove' and playerStats[pInput[1]] > min:
                playerStats[pInput[1]] -= 1
                pool += 1
            else: print(f'Points can not be below {min}')
            break

      
map = []

playerStats = {
    'strength' : 0,
    'dexterity' : 0,
    'intelligence' : 0,
    'magic' : 0
}

playerCurrent = []

mapScale = 10, 10

#core Routes (cRs)
    #number of cRs
cRQuantity = 2
    #mean length of cRs
cRTargetLength = 15
    #+- given to the length of each cR
cRLengthVariance = 4
    #available options for a wall
wallGen = [
    'unopenedTreasure',
    'wall',
    'passageWay'
]
weights = [1,10,3]

gameInit()

pointBuyStats(8, 1, min=4)

terminate = False

while True:
    if terminate: break

    genTile(playerCurrent)

    disMap()

    roomRead(playerCurrent)

    #get player input
    while True:
        pInput = readCommands(input(' [explore N/E/S/W] >>'), [['explore', ['north','east','south','west']], 'terminate'])
        if pInput[0] == 'explore':
            print('You chose to explore!!!')
            if map[playerCurrent[0]][playerCurrent[1]][pInput[1]] == 'passageWay':
                print(f'player adventures to the {pInput[1].upper()} room.')
                cDVal = {
                    'north' : [-1, 0],
                    'east' : [0, 1],
                    'south' : [1, 0],
                    'west' : [0, -1]
                }
                playerCurrent[0] += cDVal[pInput[1]][0]
                playerCurrent[1] += cDVal[pInput[1]][1]
                break
            else:
                print(f'That is a {map[playerCurrent[0]][playerCurrent[1]][pInput[1]]}')
        elif pInput[0] == 'terminate':
            print('!!!YOU HAVE CHOSEN TO END THE GAME!!!')
            terminate = True
            break