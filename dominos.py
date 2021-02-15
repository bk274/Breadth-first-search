from __future__ import print_function
import os
import logging
import argparse

from iterative_deepening import IterativeDeepening, ERR_MESSAGE, State, Searchable


class Domino(object):
  def __init__(self, index, content):
    self.index = index
    self.content = content

  def __repr__(self):
    return "{{{}: {}}}".format(self.index, self.content)


class PostCorrespondenceState(State):
  def __init__(self, state=("", ""), history=None):
    super(PostCorrespondenceState, self).__init__(state, history)

  def IsValid(self):
    return True if self.history else False

  def __str__(self):
    return "-".join(["D%d"%d for d in self.history])

  def __repr__(self):
    return "{{{}, {}}}".format(self.state, self.history)


class DominoSpace(Searchable):
  '''
  The class DominoSpace contains
    fields:
      start_point: a PostCorrespondenceState to start with.
        Initialized to state=("", ""), history=[].
      dominos: a list of Domino.
    methods:
      Neighbors(state): generate a list of neighboring states of the
        given state by trying concatenating dominos.
      Assert(state): determine if the STATE meets the goal.
 '''
  def __init__(self, dominos,
               start_point=PostCorrespondenceState(("", ""), [])):
    super(DominoSpace, self).__init__(start_point)
    # self.start_point = start_point
    self.dominos = sorted(dominos, key=lambda d: d.index)

  @staticmethod
  def _CatDomino(state, domino):
    '''
    Concatenate a domino to a state and determine if it is valid.
    Args:
      state: a PostCorrespondenceState Object.
        A valid state should have at least one empty string ("").
      domino: (int, (str_top, str_bottom)) to concatenate to the state.
    Returns:
      If a valid state is produced, return the state.
      Otherwise return an invalid state.
    '''
    state_top, state_bottom = state.state
    domino_top, domino_bottom = domino.content
    new_top, new_bottom = state_top + domino_top, state_bottom + domino_bottom
    max_len_prefix = min(len(new_top), len(new_bottom))
    if new_top[:max_len_prefix] == new_bottom[:max_len_prefix]:
      return PostCorrespondenceState(
          (new_top[max_len_prefix:], new_bottom[max_len_prefix:]),
          state.history+[domino.index]
          )
    else:
      return PostCorrespondenceState()

  def Neighbors(self, state):
    '''
    Generates a sequence of valid neighbors of a given state.

    Args:
      state: A valid state should having at least one empty string ("") in state.
    Returns:
      A list of the valid neighbor states.
    '''
    neighbors = [self._CatDomino(state, d) for d in self.dominos]
    return [n for n in neighbors if n.IsValid()]

  def Assert(self, state):
    '''
    Assert if the given state meets the goal.
    '''
    if state.IsValid():
      return state.state[0] == state.state[1]
    else:
      return False

  def Replay(self, state):
    '''
    Return the sequence of states towards the finding of the given state
    in chronological order.

    Args:
      state: The state object to whose history is to be replayed.
    Return:
      A list of states towards the finding of the given state
    organized in chronological order.
    '''
    final = state.history
    start = self.start_point.history
    final = final[len(start):]

    index_to_domino = {d.index: d for d in self.dominos}
    states = [self.start_point]
    for state in final:
      states.append(self._CatDomino(states[-1], index_to_domino[state]))
    return states


def LoadFile(fname=None):
  '''
  Args:
    fname: The file name.
  Returns:
    max_queue_size: The maximum queue size for BFS.
    max_states_num: The maximum number of states to explore.
    dominos: A list of Domino object.
  '''
  max_queue_size = None
  max_states_num = None
  flag = None
  domino_num = None
  dominos = None
  dominosMap = {}
  index = 1
  if not os.path.isfile(fname):
    print('Cannot open file: {}.'.format(fname))
    exit()
  else:
    try:
      with open(fname) as fin:
        print(fin)
        max_queue_size = int(fin.readline())
        max_states_num = int(fin.readline())
        flag = int(fin.readline())
        domino_num = int(fin.readline())
        dominos = []
        for line in fin:
          data = line.strip('\n').split(' ')
          dominos.append(Domino(int(data[0]), (data[1], data[2])))
          dominosMap["D" + data[0]] = data[1]
          if len(dominos) == domino_num: 
            break
            
    except:
      print(r'''Incompatible format!''')
      exit()

  return max_queue_size, max_states_num, flag, dominos, dominosMap


def main():
  parser = argparse.ArgumentParser(
      description=("Using BFS with Iterative Deepening to solve "
                   "the post correspondence problem of dominos."))
  parser.add_argument("FILE", type=str, help="input file name.")
  args = parser.parse_args()
  fname = args.FILE

  max_queue_size, max_states_num, flag, dominos, dominosMap = LoadFile(fname)

  domino_space = DominoSpace(dominos=dominos)
  solver = IterativeDeepening(
      domino_space,
      max_queue_size=max_queue_size,
      max_states_num=max_states_num)
  sol, err = solver.Search()

  if flag:
    all_states = solver.seen_bfs_states.keys()
    print("----- Filling Frontier -----")
    for s in all_states:
      states = format(s).split(',')
      if len(states[0]) > 3 : print("Adding State to Frontier: +" + states[0][2:-1])
      elif len(states[1]) > 4 : print("Adding State to Frontier: -" + states[1][2:-2])
    
    print("----- Frontier Complete -----")

  if sol:
    results = ("%s"%sol).split('-')
    value = ""
    for key in results: value += dominosMap[key]
    
    print("Solution Size (# of dominoes): %d (Found at iterative deepening with depth: 1)"%(len(results)))
    print("The solution sequence is: %s"%sol)
    print("The top and bottom of the sequence looks like: " + value + "/" + value)
  else:
    print("No solution exists")


if __name__ == '__main__':
  main()
