from argparse import ArgumentParser
import os
import sys
import importlib

def __main__():
  parser = ArgumentParser(prog="AoC 2023", description='Solves AoC 2023 puzzles')
  parser.add_argument('-d', '--day', choices=range(1, 26), type=int, required=True)
  parser.add_argument('-t', '--type', choices=['test', 'puzzle'], default='puzzle')
  parser.add_argument('-p', '--part', choices=['first', 'second'], default='first')
  args = parser.parse_args()

  day = '0{}'.format(args.day) if args.day <= 9 else '{}'.format(args.day)
  print(day)

  sys.path.append(os.path.join(os.getcwd(), 'solver', 'utils'))

  module = importlib.import_module('solver.solutions.day_{}.solve'.format(day))
  module.solve(type=args.type, part=args.part)

__main__()