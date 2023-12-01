import solver.utils

def solve(type, part):
  if type == 'test':
    solve_test(part)
  else:
    solve_puzzle(part)

def solve_test(part):
  if part == 'first':
    solve_test_first_part()
  else:
    solve_test_second_part()

def solve_test_first_part():
  pass

def solve_test_second_part():
  pass

def solve_puzzle(part):
  if part == 'first':
    solve_puzzle_first_part()
  else:
    solve_puzzle_second_part()

def solve_puzzle_first_part():
  pass

def solve_puzzle_second_part():
  pass