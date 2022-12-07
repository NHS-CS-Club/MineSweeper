import random, string, re, os
import display as disp
from typing import List, Tuple, Dict, Union
import sys
import time
from copy import deepcopy


def print_slow(str, delay):
  for letter in str:
    sys.stdout.write(letter)
    sys.stdout.flush()
    time.sleep(delay)
  return


field = []  # Not-Displayed Field
visible = []  # Displayed Field
first_click = True
safe_zone = []  # Zone of zeros around user's first click
MINE_CHANCE = 4  # Number of possible outcomes where a mine is only 1 (eg. MINE_CHANCE=6 means a mine has a 1/6 chance)
mines = set([])  # List of mine locations
flags = set([]) # List of flag locations

'''
Symbols:
# - Mines
? - Flag
- - Empty
1-9 - Numbers
'''
SYMBOLS = {
  'mine': '#',
  'flag': '⚑',
  'empty': f' {disp.dim}▢{disp.normal} ',
  'zero': f'{disp.dim}■{disp.normal}'
}

DIFFICULTY = {'easy': 10, 'normal': 18, 'hard': 26}

INPUT_ERR = f'''
{disp.dim}You should enter a column-letter and a row-number for the cell you want to target (eg. f8, F8). 
If you want to flag it instead of open it, then type `flag` before the cell (eg. `flag f8`, `flag F8`). 
If you want to unflag it, type `unflag` before the cell (eg. `unflag p14`).{disp.normal}
'''.strip()

BOUNDS_ERR = f'''
{disp.dim}Enter a number and letter that are in the board's bounds{disp.normal}
'''.strip()

TOO_MANY_FLAGS = f'''
{disp.dim}Uh Oh! Looks like you have too many flags!{disp.normal}
'''


# Checks if cell can be uncovered
def uncoverable(cell: tuple) -> bool:
  value = (cell[0] >= 0 and cell[0] <= 26 and cell[1] >= 0 and cell[1] <= 26
           and field[cell[0]][cell[1]] == SYMBOLS['empty'])
  print(cell, value)
  return value


# Uncovers all adjacent cells
# Diagonals don't count
def uncover_cell(cell: tuple):
  global first_click

  # Checks if cell is bomb
  if field[cell[1]][cell[0]] == SYMBOLS['mine']:
    os.system("clear")
    print("You hit a bomb!")
    time.sleep(2)
    os.system("clear")
    print_slow(f"""\n\n\n\n       Game Over""", 0.05)
    time.sleep(2)
    os.system("clear")
    disp.begin()

  # Checks if cell is flag
  if field[cell[1]][cell[0]] == SYMBOLS['flag']:
    os.system("clear")
    print("Cannot uncover a flag!\n")
    # print_field(field)
    print("\n\n\n\n\n")
    print_field(visible)
    return -1
  os.system("clear")

  visible[cell[1]][cell[0]] = field[cell[1]][cell[0]]
  uncover_linked(cell)
  # print_field(field)
  print("\n\n\n\n\n")
  print_field(visible)
  return 0
  
# Flags a cell
def flag_cell(cell: tuple):
  targeted = visible[cell[1]][cell[0]]

  if targeted == SYMBOLS['empty']:
    visible[cell[1]][cell[0]] = SYMBOLS['flag']
    flags.add(cell)
    print(flags,mines)
    if mines == flags:
      for f in flags:
        # winner winner chicken dinner
          os.system("clear")
          print("You Win!")
          time.sleep(2)
          os.system("clear")
          print_slow(f"""\n\n\n\n       Winner Winner...""", 0.05)
          time.sleep(2)
          print_slow(f"""\n\n\n\n             Chicken Dinner!""", 0.05)
          time.sleep(2)
          os.system("clear")
          disp.begin()
    
    return 0
  else:
    print(f"{disp.dim}Cannot place flag here!{disp.normal}")
    return -1


# Unflags a cell
def unflag_cell(cell: tuple):
  targeted = visible[cell[1]][cell[0]]

  if targeted == SYMBOLS['flag']:
    visible[cell[1]][cell[0]] = SYMBOLS['empty']
    flags.remove(cell)
    return 0
  else:
    print(f"{disp.dim}Cannot unflag non-flagged cells or mines!{disp.normal}")
    return -1


CMDS = {'open': uncover_cell, 'flag': flag_cell, 'unflag': unflag_cell}


# Uncovers all 0 tiles that touch a 0 tile
def uncover_linked(cell: Tuple):
  # If 0 cell
  if field[cell[1]][cell[0]] == "0":
    # Uncover cell if its not a bomb
    if field[cell[1]][cell[0]] != SYMBOLS['mine']:
      visible[cell[1]][cell[0]] = field[cell[1]][cell[0]]

    #visible[cell[1]][cell[0]] = field[cell[1]][cell[0]]
    # check all surrounding tiles for 0
    for i in range(-1, 2):
      for j in range(-1, 2):
        # for every 0
        search_row = cell[1] + i
        search_col = cell[0] + j
        if search_row < size and search_col < size and search_row >= 0 and search_col >= 0:
          if field[cell[1] +i][cell[0] +j] == "0" and visible[cell[1] + i][cell[0] + j] != "0":

            # call the function with the coords of that cell
            uncover_linked((cell[0] + j, cell[1] + i))
          else:
            if field[cell[1] + i][cell[0] + j] != SYMBOLS['mine']:
              visible[cell[1] + i][cell[0] + j] = field[cell[1]+i][cell[0]+j]
        else:
          continue
  else:
    return


# Gets big zone from zone (of zeroes), to prevent bombs from generating there (in the future)
def get_big_zone() -> List[Tuple[int, int]]:
  big_zone = []
  all_big_zone_cells = []
  for cell in safe_zone:
    for i in range(-2, 1):
      for j in range(-2, 1):
        if cell[0] + j >= 0 and cell[1] + i >= 0 and cell[0] + j < size and cell[1] + i < size:
          new_cell = (cell[0] + j, cell[1] + i)
          if new_cell not in all_big_zone_cells:
            big_zone += [new_cell]
            visible[new_cell[0] + j][new_cell[1] + i] = visible[new_cell[0]+j][new_cell[1]+i]
        else:
          continue
  # print('BIG_ZONE:', big_zone, end='\n\n')
  return big_zone


# Fills grid with empty spaces
def init_grid(size: int) -> None:
  global field, visible

  # field = [
  #   [SYMBOLS['empty']] * size
  # ] * size
  for i in range(size):
    row = []
    for j in range(size):
      row += [SYMBOLS['empty']]
    field += [row]
  visible = deepcopy(field)


# Builds a grid for the minesweeper field after first click
def build_grid(size_l: int) -> None:
  global size, safe_zone, field

  size = size_l

  new_safe_zone = []
  source = safe_zone[0]
  for i in range(-2, 2):
    for j in range(-2, 2):
      if source[0] + i >= 0 and source[1] + j >= 0 and source[0] + abs(i) < size and source[1] + abs(j) < size:
        new_safe_zone += [(source[0] + abs(i), source[1] + abs(j)) ]
  safe_zone = new_safe_zone

  big_zone = get_big_zone()

  for cell in safe_zone:
    print('CELL IN BUILD:', cell)
    field[cell[1]][cell[0]] = '0'

  # Generate mines
  for r in range(size):
    for c in range(size):
      rand = random.randrange(MINE_CHANCE)
      if rand == 0 and (c, r) not in big_zone:
        field[r][c] = SYMBOLS["mine"]
        mines.add((c,r))

  for r in range(size):
    for c in range(size):
      cell = field[r][c]
      num_bombs = 0

      # Checks cells adjacent to `cell` and counts mines. Puts count as the value of the cell
      for i in range(-1, 2):
        for j in range(-1, 2):
          search_row = r + i
          search_col = c + j

          # Increment counter if mine found
          if search_row < size and search_col < size and search_row >= 0 and search_col >= 0:
            if field[r + i][c + j] == SYMBOLS['mine']:
              num_bombs += 1
                # 
      if cell != SYMBOLS['mine']:
        bomb_count = str(num_bombs)
        field[r][c]=bomb_count
        # field[r][c] = SYMBOLS['zero'] if num_bombs == 0 else str(num_bombs)
        # num_bombs == "0" ? field[r][c] = SYMBOLS["zero"] : field[r][c] = str(num_bombs)
    # visible[cell[1]][cell[0]] = SYMBOLS["zero"]

  uncover_linked(source)

  # for cell in get_big_zone():
  #   visible[cell[1]][cell[0]] = SYMBOLS["zero"]

  os.system("clear")
  print()

  print_field(visible, vis=True)

# Formats numbers to be displayed
def format_num(st):
  if st == '0':
    return ' '
  else:
    return disp.SYM_COLOR.get(st, disp.white) + st + disp.reset
  
# Prints the field
def print_field(field: list, *, vis=False):
  print("   ", *(string.ascii_uppercase[0:len(field)]), sep=" ")

  for i, r in enumerate(field):
    if i + 1 < 10: print(" ", end="")
    
    print(f'{i + 1}. ', end="")
    
    if vis: 
      print(*[format_num(c.strip()) for c in r], sep=" ")
    else:
      print(*[c.strip() for c in r], sep=" ")


# Reprints edited field to the user
def refresh_field() -> None:
  os.system("clear")
  print_field(visible, vis=True)


# Target a certain cell based off of the string representation
def target_cell(st: str) -> tuple:
  col = st[0]
  row = st[1:]

  # Checks if column is not a letter
  if not col.isalpha():
    raise TypeError('Column must be letter')
  # Checks if row is not a number
  elif not row.isnumeric():
    raise TypeError('Row must be number')

  col = string.ascii_lowercase.index(col.lower())
  row = int(row)
  return (col, row)


# Check validity of cell string (not of entire cmd)
def valid_input(st: str) -> bool:
  valid = re.search("^[a-zA-Z][0-9]+", st)
  if valid is not None:
    return True
  return False


# Do the appropriate action for the given cmd
def exec_cmd(cmd: Dict[str, Union[str, Tuple[int, int]]]) -> None:
  cell = cmd['cell']

  if cmd['cmd'] not in CMDS:
    raise ValueError(f'Invalid cell type: must be one of {CMDS.keys()}')

  if cell[0] > size or cell[1] > size:
    raise ValueError('Invalid cell value: too large')

  if cell[0] < 0 or cell[1] < 0:
    raise ValueError('Invalid cell value: too small')

  # cmd is already lowercase, no need for `.lower()`
  CMDS[cmd['cmd']](cell)


'''
SYNTAX for cmds:
  Just cell when opening a cell:
    c4
    b8
    I11
  `flag` before cell to flag it:
    flag c4
    flag B8
    flag i11
  `unflag` before cell to unflag already flagged cells:
    unflag C4
    unflag b8
    unflag I11
get_cmd will return the cmd, or an error value.
'''


def get_cmd(st: str, size: int) -> Dict[str, Union[str, Tuple[int, int]]]:
  cmd = [s.lower() for s in st.strip().split(' ')]

  if len(cmd) == 1:
    cmd *= 2
    cmd[0] = 'open'

  print('CMD', cmd)

  if not cmd[-1][0].isalpha():
    print('ERR', 1, '\n' + INPUT_ERR)
    return 'ERR'

  if not cmd[-1][1:].isnumeric():
    print('ERR', 2, '\n' + INPUT_ERR)
    return 'ERR'

  if cmd[0] not in CMDS:
    print('ERR', 3, '\n' + INPUT_ERR)
    return 'ERR'

  if not valid_input(cmd[-1]):
    print('ERR', 4, '\n' + INPUT_ERR)
    return 'ERR'

  char_idx = string.ascii_lowercase.index(cmd[-1][0])
  row = int(cmd[-1][1:])

  if char_idx >= size:
    print('ERR', 5, '\n' + BOUNDS_ERR)
    return 'ERR'

  if row > size or row <= 0 or not isinstance(row, int):
    print(6, '\n' + BOUNDS_ERR)
    return 'ERR'

  return {'cmd': cmd[0], 'cell': (char_idx, int(cmd[-1][1:]) - 1)}
