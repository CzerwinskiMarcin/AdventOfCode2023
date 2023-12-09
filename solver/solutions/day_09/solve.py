from solver.utils.file_utils import *
import os

def solve(type, part):
  target_data_file = 'test.txt' if type == 'test' else 'data.txt'
  solve_directory_path = os.path.dirname(__file__)
  filepath = os.path.join(solve_directory_path, 'data', target_data_file)
  data = read_lines(filepath)
  return do_solve(part, data)

def do_solve(part, data):
  if part == 'first':
    return solve_first_part(data)
  else:
    return solve_second_part(data)

def solve_first_part(data):
  formatted_data = format_data(data)
  [update_differences(numbers) for numbers in formatted_data]
  [extrapolate_forward(numbers) for numbers in formatted_data]

  return sum_extrapolates_forward(formatted_data)

def solve_second_part(data):
  formatted_data = format_data(data)
  [update_differences(numbers) for numbers in formatted_data]
  [extrapolate_backward(numbers) for numbers in formatted_data]

  return sum_extrapolates_backward(formatted_data)

def format_data(data):
  sensors_data = []
  for line in data:
    numbers = [int(x) for x in line.split(' ')]
    sensors_data.append([numbers])
  return sensors_data

def update_differences(numbers):
  are_all_differences_equal_zero = False

  while not are_all_differences_equal_zero:
    differences = []

    for i in range(len(numbers[-1]) - 1):
      differences.append(numbers[-1][i+1] - numbers[-1][i])
    
    are_all_differences_equal_zero = all([number == 0 for number in differences])
    numbers.append(differences)
  
def extrapolate_forward(numbers):
  numbers.reverse()

  last_predict = 0
  for i in range(len(numbers) - 1):
    last_number = numbers[i+1][-1]
    last_predict = last_number + last_predict
    numbers[i+1].append(last_predict)
  
  numbers.reverse()

def extrapolate_backward(numbers):
  numbers.reverse()

  last_predict = 0
  for i in range(len(numbers) - 1):
    last_number = numbers[i+1][0]
    last_predict = last_number - last_predict
    numbers[i+1].insert(0, last_predict)
  
  numbers.reverse()

def sum_extrapolates_forward(data):
  sum = 0
  for numbers in data:
    sum += numbers[0][-1]
  return sum

def sum_extrapolates_backward(data):
  sum = 0
  for numbers in data:
    sum += numbers[0][0]
  return sum