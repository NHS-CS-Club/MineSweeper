import minesweeper as mine
import display as disp
import os
'''
TODO

* Generate Numbers in grid 
* Generate safe zone after first cell
* Print Game Over Screen 
* Display Uncovered Cells, Flagged Cells, Bombs
* More Stuff

'''


def main():
  # disp.print_slow('Initializing...\n\n', 0.1)
  # disp.time.sleep(2)
  # disp.print_slow('Please use full screen.', 0.1)
  # disp.time.sleep(1)
  # disp.os.system('clear')

  while True:

    size = disp.begin()
    status = 0  # DEFAULT: game not over
    player_won: bool = False  # If they won or lost
    game_over: bool = status == 1  # If game is over

    mine.init_grid(size)
    mine.print_field(mine.visible, vis=True)

    # 0. init vars                         - DONE
    # 1. display empty field               - DONE
    # 2. get user input                    - DONE
    # 3. use the user input as safe zone   - DONE
    # 4. generate field                    - DONE
    # 5. refresh field                     - DONE
    # 6. continue game                     - 
    # 7. process commands                  - 

    # Check input validity
    while True:
      user_input = input(f'\nSelect a Cell (or flag/unflag)\n{disp.bright}> {disp.reset}')
      print(disp.normal)
      if (cmd := mine.get_cmd(user_input,size)) != 'ERR':
        break

    mine.safe_zone = [cmd["cell"]]
    mine.build_grid(size)
    
    while not game_over:
      user_input = input(f'\nSelect a Cell (or flag/unflag)\n{disp.bright}> {disp.reset}')
    
      print(disp.normal, end='')

      # Check input validity
      if (cmd := mine.get_cmd(user_input,size)) == 'ERR':
        continue  # If input is valid

      # If input is correct
      print('CMD:', cmd)
      mine.exec_cmd(cmd)
      mine.refresh_field()
      print()

    # After they lost or won
    CHOICES = ['quit', 'play']

    while user_input not in CHOICES:
      print('Either type quit or play to exit or play again!', end=' ')
      user_input = input().lower()

    if user_input == 'quit':
      return 0

if __name__ == '__main__':
  os.system('python --version')

  main()
  disp.end_game()
  print('DONE!')