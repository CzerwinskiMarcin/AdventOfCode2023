from solver.utils.file_utils import *
import os

hand_states = [[5], [4], [3, 2], [3], [2, 2], [2], [1]]
card_strengths_map = {
  'A': 14,
  'K': 13,
  'Q': 12,
  'J': 11,
  'T': 10,
  '9': 9,
  '8': 8,
  '7': 7,
  '6': 6,
  '5': 5,
  '4': 4,
  '3': 3,
  '2': 2,
}

card_strength_map_with_joker = {
  'A': 14,
  'K': 13,
  'Q': 12,
  'T': 10,
  '9': 9,
  '8': 8,
  '7': 7,
  '6': 6,
  '5': 5,
  '4': 4,
  '3': 3,
  '2': 2,
  'J': 1,
}

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
  calculated_state_hands = [calculate_hand_state(hand) for hand in formatted_data]
  update_hands_card_sequence_strength(calculated_state_hands, card_strengths_map)
  ordererd_state_hands = order_hands_by_state(calculated_state_hands)
  ordered_strength_hands = sort_hands_by_strength_cards_order(ordererd_state_hands)
  ordered_strength_hands.reverse()
  return calculate_total_winning(ordered_strength_hands)

def solve_second_part(data):
  formatted_data = format_data(data)
  calculated_state_hands = [calculate_hand_state_with_joker(hand) for hand in formatted_data]
  update_hands_card_sequence_strength(calculated_state_hands, card_strength_map_with_joker)
  ordererd_state_hands = order_hands_by_state(calculated_state_hands)
  ordered_strength_hands = sort_hands_by_strength_cards_order(ordererd_state_hands)
  ordered_strength_hands.reverse()
  return calculate_total_winning(ordered_strength_hands)

def format_data(data):
  hands = []
  for line in data:
    [hand, bid] = line.split(' ')
    hands.append({'hand': hand, 'bid': int(bid)})
  return hands

def calculate_hand_state(hand):
  hand_parts_count = count_hand_cards_and_sort(hand)
  update_hand_state(hand, hand_parts_count)
  return hand

def calculate_hand_state_with_joker(hand):
  update_hand_state_with_joker(hand)
  return hand


def count_hand_cards_and_sort(hand):
  hand_parts_count = {}
  hand_parts = [character for character in hand['hand']]
  for part in hand_parts:
    if part not in hand_parts_count:
      hand_parts_count[part] = 1
    else:
      hand_parts_count[part] += 1
  
  cards_raw_count = [hand_parts_count[key] for key in hand_parts_count]
  cards_raw_count.sort(reverse=True)
  return cards_raw_count

def update_hand_state(hand, hand_parts_count):
  for i in range(len(hand_states)):
    state = hand_states[i]
    is_matching = True
    for j in range(len(state)):
      if state[j] != hand_parts_count[j]:
        is_matching = False

    if is_matching:
      hand['state'] = i
      break

def update_hand_state_with_joker(hand): 
  state = 99
  for card in card_strength_map_with_joker:
    hand_copy = hand.copy()
    hand_copy['hand'] = hand_copy['hand'].replace('J', card)
    hand_parts_count = count_hand_cards_and_sort(hand_copy)
    update_hand_state(hand_copy, hand_parts_count)
    if state > hand_copy['state']:
      state = hand_copy['state']

  hand['state'] = state


def update_hands_card_sequence_strength(hands, card_strengths_map):
  for hand in hands:
    cards_strengths = []
    for card in hand['hand']:
      cards_strengths.append(card_strengths_map[card])
    hand['cards_strengths'] = cards_strengths

def compare_hands_by_state(hand):
  return hand['state']

def order_hands_by_state(hands):
  sorted_by_state = sorted(hands, key=compare_hands_by_state)
  return sorted_by_state

def sort_hands_by_strength_cards_order(hands):
  is_sorted = False

  while not is_sorted:
    is_sorted = True

    for i in range(len(hands) - 1):
      if hands[i]['state'] != hands[i+1]['state']:
        continue

      for j in range(len(hands[i]['cards_strengths'])):
        if hands[i]['cards_strengths'][j] > hands[i+1]['cards_strengths'][j]:
          break
        if hands[i]['cards_strengths'][j] < hands[i+1]['cards_strengths'][j]:
          hands[i], hands[i+1] = hands[i+1], hands[i]
          is_sorted = False
          break

  return hands

def calculate_total_winning(hands):
  total_winnings = 0
  for i in range(len(hands)):
    total_winnings += hands[i]['bid'] * (i+1)
  return total_winnings