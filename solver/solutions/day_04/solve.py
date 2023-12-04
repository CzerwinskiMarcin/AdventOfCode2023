from solver.utils.file_utils import *
import os
import re

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
  winning_numbers = get_winning_numbers(formatted_data)
  return calculate_points_from_wining_numbers(winning_numbers)

def solve_second_part(data):
  formatted_data = format_data(data)
  winning_numbers = get_winning_numbers(formatted_data)
  calculate_next_cards_from_wining_numbers(formatted_data, winning_numbers)
  return resolve_wining_cards_with_copies(formatted_data)

def format_data(data):
  formatted_data = []
  for d in data:
    [card, numbers] = re.split(r'\:', d)
    card_number = int(re.findall(r'[1234567890]+', card)[0])
    [raw_wining_numbers, raw_numbers] = re.split(r'\s\|\s', numbers)

    wining_numbers_it = re.finditer(r'[1234567890]+', raw_wining_numbers)
    wining_numbers = [int(number.group()) for number in wining_numbers_it]

    got_numbers_it = re.finditer(r'[1234567890]+', raw_numbers)
    got_numbers = [int(number.group()) for number in got_numbers_it]

    formatted_data.append({
      'index': card_number,
      'wining_numbers': wining_numbers,
      'numbers': got_numbers
    })
  return formatted_data

def get_winning_numbers(cards_data):
  cards_wining_numbers = []
  for card_data in cards_data:
    cards_wining_numbers.append([number for number in card_data['numbers'] if number in card_data['wining_numbers']])
  return cards_wining_numbers

def calculate_points_from_wining_numbers(cards_wining_numbers):
  sum_of_winning_cards = 0

  for winning_numbers in cards_wining_numbers:
    if len(winning_numbers) == 0:
      continue
    elif len(winning_numbers) == 1:
      sum_of_winning_cards += 1
    else:
      sum_of_winning_cards += pow(2, len(winning_numbers) - 1)
  return sum_of_winning_cards

def calculate_next_cards_from_wining_numbers(cards_data, winning_numbers):
  for index in range(len(cards_data)):
    card_data = cards_data[index]
    card_data['next_cards_indexes'] = []
    number_of_next_cards = len(winning_numbers[index])
    for next_index in range(number_of_next_cards):
      card_data['next_cards_indexes'].append(card_data['index'] + next_index)

def resolve_wining_cards_with_copies(cards_data):
  number_of_cards = []
  for card in cards_data:
    number_of_cards.append(1)

  for index, cards_number in enumerate(number_of_cards):
    next_cards_indexes = cards_data[index]['next_cards_indexes']
    for next_card_index in next_cards_indexes:
      number_of_cards[next_card_index] += cards_number
  return sum(number_of_cards)