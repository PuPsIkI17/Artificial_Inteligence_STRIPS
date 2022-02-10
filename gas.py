from typing import List, Tuple
from levels import *
from util import delta, iswin, p
import copy, math
"""
#######################################
################ TODOs ################
#######################################
"""

#function
def update_position(new_state, state, dir, state_changer, j):
    new_pos = delta(state[j][X], state[j][Y], dir)
    pos_tuple = (new_pos[0], new_pos[1])
    if pos_tuple in state_changer.keys():
        new_state[j][DIR] = state_changer[pos_tuple]
    new_state[j][X] = new_pos[0]
    new_state[j][Y] = new_pos[1]


#operator 1
def moveNorh(color, state, state_changer, dir):
    new_state = copy.deepcopy(state)
    for i in range(len(state)):
        if state[i][COLOR] == color:
            for j in range(len(state)):
                if state[j][COLOR] != state[i][COLOR] and state[j][X] == state[i][X]:
                    count = 0
                    for k in range(len(state)):
                        if state[k][X] == state[i][X] and state[k][COLOR] != state[j][COLOR] and state[k][COLOR] != state[i][COLOR] \
                                and state[k][Y] > state[i][Y] and state[k][Y] < state[j][Y]:
                            count += 1
                    if count + 1 == state[j][Y] - state[i][Y]:
                        update_position(new_state, state, dir, state_changer, j)
            update_position(new_state, state, dir, state_changer, i)
    return new_state

#operator 2
def moveSouth(color, state, state_changer, dir):
    new_state = copy.deepcopy(state)
    for i in range(len(state)):
        if state[i][COLOR] == color:
            for j in range(len(state)):
                if state[j][COLOR] != state[i][COLOR] and state[j][X] == state[i][X]:
                    count = 0
                    for k in range(len(state)):
                        if state[k][X] == state[i][X] and state[k][COLOR] != state[j][COLOR] and state[k][COLOR] != state[i][COLOR] \
                                and state[k][Y] < state[i][Y] and state[k][Y] > state[j][Y]:
                            count += 1
                    if count + 1 == state[i][Y] - state[j][Y]:
                        update_position(new_state, state, dir, state_changer, j)
            update_position(new_state, state, dir, state_changer, i)
    return new_state

#operator 3
def moveEast(color, state, state_changer, dir):
    new_state = copy.deepcopy(state)
    for i in range(len(state)):
        if state[i][COLOR] == color:
            for j in range(len(state)):
                if state[j][COLOR] != state[i][COLOR] and state[j][Y] == state[i][Y]:
                    count = 0
                    for k in range(len(state)):
                        if state[k][Y] == state[i][Y] and state[k][COLOR] != state[j][COLOR] and state[k][COLOR] != state[i][COLOR] \
                                and state[k][X] < state[i][X] and state[k][X] > state[j][X]:
                            count += 1
                    if count + 1 == state[i][X] - state[j][X]:
                        update_position(new_state, state, dir, state_changer, j)
            update_position(new_state, state, dir, state_changer, i)
    return new_state

#operator 4
def moveWest(color, state, state_changer, dir):
    new_state = copy.deepcopy(state)
    for i in range(len(state)):
        if state[i][COLOR] == color:
            for j in range(len(state)):
                if state[j][COLOR] != state[i][COLOR] and state[j][Y] == state[i][Y]:
                    count = 0
                    for k in range(len(state)):
                        if state[k][Y] == state[i][Y] and state[k][COLOR] != state[j][COLOR] and state[k][COLOR] != state[i][COLOR] \
                                and state[k][X] > state[i][X] and state[k][X] < state[j][X]:
                            count += 1
                    if count + 1 == state[j][X] - state[i][X]:
                        update_position(new_state, state, dir, state_changer, j)
            update_position(new_state, state, dir, state_changer, i)
    return new_state

def press(color: str, state: List[List[str or int]]) -> List[List[str or int]]:
    state_changer = {(e[X], e[Y]): e[DIR] for e in state if e[TYPE] == CHANGER}
    state_sq = [e for e in state if e[TYPE] == SQUARE]
    goal_state = [e for e in state if e[TYPE] == GOAL]
    changer_state = [e for e in state if e[TYPE] == CHANGER]
    dir_squares = {e[COLOR]: e[DIR] for e in state if e[TYPE] == SQUARE}
    dir = dir_squares[color]
    new_state = []
    if dir == '^':
        new_state = moveNorh(color, state_sq, state_changer, dir)
    elif dir == 'v':
        new_state = moveSouth(color, state_sq, state_changer, dir)
    elif dir == '<':
        new_state = moveEast(color, state_sq, state_changer, dir)
    elif dir == '>':
        new_state = moveWest(color, state_sq, state_changer, dir)
    final_state = goal_state + new_state + changer_state
    return final_state

UprimIda = 0
costT = 0
def h_function(state, goal_state):
    state_sq = [e for e in state if e[TYPE] == SQUARE]
    cost = 0
    for i in state_sq:
        x1 = i[X]
        y1 = i[Y]
        if i[COLOR] not in goal_state.keys():
            return cost
        x2 = goal_state[i[COLOR]][X]
        y2 = goal_state[i[COLOR]][Y]
        diff1 = x2 - x1
        diff2 = y2 - y1
        if diff1 < 0:
            diff1 = -diff1
        if diff2 < 0:
            diff2 = -diff2
        #cost += diff1 + diff2
        cost += int(math.sqrt((diff1 ** 2 + diff2 ** 2) * 25))
    return cost

def ida(s, g, U, visited, pcost, goal_state):
  global UprimIda, costT
  if iswin(s):
    print("Cost: " + str(g))
    costT = len(visited)
    return ([s],[])

  hashable = []
  for i in s:
      hashable += tuple(i)
  hashable = tuple(hashable)

  if hashable in visited.keys() and hashable in pcost.keys() and g >= pcost[hashable]:
    return ({},{})
  visited[hashable] = 1
  pcost[hashable] = g
  for i in s:
      if i[TYPE] == SQUARE:
        v = press(i[COLOR], s)
        h = h_function(v, goal_state)
        cost = 1
        if g + cost + h <= U:
            (p, colors) = ida(v, g + cost, U, visited, pcost, goal_state)
            if p != {}:
                p.append(s)
                colors.append(i[COLOR])
                return (p,colors)
        else:
            if g + cost + h <= UprimIda:
                UprimIda = g + cost + h
  return ({},{})

def buclaIDA(s, goal_state):
  inf = 150000000000
  global UprimIda
  bestPath = {}
  bestColors = {}
  while bestPath == {} and UprimIda != inf:
    visited = {}
    cost = {}
    U = UprimIda
    UprimIda = inf
    (bestPath, bestColors) = ida(s, 0, U, visited, cost, goal_state)
  return (bestPath, bestColors)


def solve(initial_state: List[List[str or int]]) -> Tuple[List[str], List[List[List[str or int]]], int]:
    #return ([],[initial_state], 0)
    global UprimIda, costT
    UprimIda = 0
    costT = 0
    goal_state = {e[COLOR]:e[XY] for e in initial_state if e[TYPE] == GOAL}
    (way,colors) = buclaIDA(initial_state, goal_state)
    all_states = way[::-1]
    colors = colors[::-1]
    return (colors, all_states, costT)

def play(initstate: List[List[str or int]], plan: List[str], small: bool=False):
    state = initstate
    print(p(state, small))
    for action in plan:
        state = press(action, state)
        print(p(state, small))


# play(levels['level10'], [RED, RED, RED, DARK, DARK, BLUE, BLUE, BLUE])