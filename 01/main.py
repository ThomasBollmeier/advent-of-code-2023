import regex

NUM_REGEX = regex.compile(r'(\d|one|two|three|four|five|six|seven|eight|nine)')

STR_TO_NUM = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
}


def read_input(filename):
  with open(filename) as f:
    ret = f.readlines()
  return ret


def to_num(s):
  if s.isdigit():
    return int(s)
  else:
    return STR_TO_NUM[s]


def get_number(line):
  numbers = NUM_REGEX.findall(line, overlapped=True)
  num = 10 * to_num(numbers[0]) + to_num(numbers[-1])
  #print(numbers, num)
  return num


total = 0
lines = read_input("input2.txt")
for line in lines:
  n = get_number(line)
  total += n

print(total)
