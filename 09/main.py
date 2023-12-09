import os


def read_input(filename):
  filepath = os.path.dirname(__file__) + os.sep + filename
  with open(filepath) as f:
    ret = f.readlines()
  return ret  


def parse_history(line):
  return [int(val) for val in line.split()]


def next_history(hist):
  ret = []
  for i in range(len(hist) - 1):
    ret.append(hist[i + 1] - hist[i])
  return ret


def all_zero(hist):
  for h in hist:
    if h != 0:
      return False
  return True


def find_next(hist):
  diffs = []
  while hist:
    if all_zero(hist):
      return sum(diffs)
    diffs.append(hist[-1])
    hist = next_history(hist)

  raise Exception("Cannot determine next element")


def find_prev(hist):
  first_elements = []
  while hist:
    if all_zero(hist):
      return calc_previous(first_elements)
    first_elements.append(hist[0])
    hist = next_history(hist)

  raise Exception("Cannot determine previous element")


def calc_previous(first_elements):
  ret = 0
  first_elements.reverse()
  for elem in first_elements:
    ret = elem - ret
  return ret


def part1():
  lines = read_input("input.txt")
  next_elements = [find_next(parse_history(line)) for line in lines]
  print(sum(next_elements))


def part2():
  lines = read_input("input.txt")
  prev_elements = [find_prev(parse_history(line)) for line in lines]
  print(sum(prev_elements))


if __name__ == "__main__":
  part2()
