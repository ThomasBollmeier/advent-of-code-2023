def read_input(filename):
  with open(filename) as f:
    ret = f.readlines()
  return ret


def parse_line(line):
  ret = 0
  _, numbers = line.split(":")
  win_str, nums_str = numbers.split("|")
  winning_numbers = {int(n) for n in win_str.split()}
  my_numbers = [int(n) for n in nums_str.split()]
  for n in my_numbers:
    if n in winning_numbers:
      ret = 1 if ret == 0 else 2 * ret
  return ret

def parse_num_wins(line):
  ret = 0
  _, numbers = line.split(":")
  win_str, nums_str = numbers.split("|")
  winning_numbers = {int(n) for n in win_str.split()}
  my_numbers = [int(n) for n in nums_str.split()]
  for n in my_numbers:
    if n in winning_numbers:
      ret += 1
  return ret
  

def part1():
  total = 0
  lines = read_input("input.txt")
  for line in lines:
    total += parse_line(line)
  print(total)


def part2():
  lines = read_input("input.txt")

  cards = []
  for line in lines:
    num_wins = parse_num_wins(line)
    cards.append((1, num_wins))

  num_orig_cards = len(cards)
 
  total = 0
  for i, card in enumerate(cards):
    cnt, num_wins = card
    total += cnt
    if num_wins > 0:
      n = min(i + 1 + num_wins, num_orig_cards)
      for j in range(i + 1, n):
        c = cards[j]
        cards[j] = (c[0] + cnt, c[1])
   
  print(total)


part2()
