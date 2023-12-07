import os

CARD_MAP = dict(zip("AKQJT98765432", "abcdefghijklm"))
CARD_MAP_2 = dict(zip("AKQT98765432J", "abcdefghijklm"))
JOKER = "J"


def read_input(filename):
  with open(filename) as f:
    ret = f.readlines()
  return ret


def parse_hand_bid(line):
  hand, bid_str = line.split()
  return hand, int(bid_str)


def determine_value(hand):
  ret = determine_type(hand)
  ret += "".join([CARD_MAP[ch] for ch in hand])
  return ret


def determine_type(hand):
  counters = calc_counters(hand)
  if counters == (5, ):
    return 'a'  # five of a kind
  if counters == (4, 1):
    return 'b'  # four of a kind
  if counters == (3, 2):
    return 'c'  # full house
  if counters == (3, 1, 1):
    return 'd'  # three of a kind
  if counters == (2, 2, 1):
    return 'e'  # two pair
  if counters == (2, 1, 1, 1):
    return 'f'  # one pair
  if counters == (1, 1, 1, 1, 1):
    return 'g'  # high card
  return 'h'


def calc_counters(hand):
  stats = {}
  for ch in hand:
    stats[ch] = stats.get(ch, 0) + 1
  return tuple(sorted(stats.values(), reverse=True))


def determine_value_2(hand):
  ret = determine_type_2(hand)
  ret += "".join([CARD_MAP_2[ch] for ch in hand])
  return ret


def determine_type_2(hand):

  counters = calc_counters_2(hand)
  sum_jokers = 5 - sum(counters)
  if counters:
    counters[0] += sum_jokers
  else:
    counters = [sum_jokers]
  counters = tuple(counters)

  if counters == (5, ):
    return 'a'  # five of a kind
  if counters == (4, 1):
    return 'b'  # four of a kind
  if counters == (3, 2):
    return 'c'  # full house
  if counters == (3, 1, 1):
    return 'd'  # three of a kind
  if counters == (2, 2, 1):
    return 'e'  # two pair
  if counters == (2, 1, 1, 1):
    return 'f'  # one pair
  if counters == (1, 1, 1, 1, 1):
    return 'g'  # high card
  return 'h'


def calc_counters_2(hand):
  stats = {}
  for ch in hand:
    if ch == JOKER:
      continue
    stats[ch] = stats.get(ch, 0) + 1
  return sorted(stats.values(), reverse=True)


def part1():
  run(os.path.dirname(__file__) + os.sep + "input.txt", determine_value)


def part2():
  run(os.path.dirname(__file__) + os.sep + "input.txt", determine_value_2)


def run(filename, value_fn):
  lines = read_input(filename)
  hands_bids = [parse_hand_bid(line) for line in lines]
  values_bids = sorted([(value_fn(hand), bid) for hand, bid in hands_bids],
                       key=lambda t: t[0],
                       reverse=True)
  total = 0
  for i, value_bid in enumerate(values_bids):
    total += (i + 1) * value_bid[1]
  print(total)


if __name__ == "__main__":
  part1()
  part2()
