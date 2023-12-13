def read_input(file_name):
  with open(file_name, 'r') as f:
    ret = f.readlines()
  return ret


def main(input_file):
  pattern = []
  total = 0
  for line in read_input(input_file):
    line = line.strip()
    if not line:
      if pattern:
        total += score(pattern, max_diff_count=1)
        pattern = []
    else:
      pattern.append(line)
  if pattern:
    total += score(pattern, max_diff_count=1)

  print(total)


def score(pattern, max_diff_count=0):
  horiz_idx = search_reflection_idx(pattern, max_diff_count)
  if horiz_idx != -1:
    return 100 * (horiz_idx + 1)
  num_columns = pattern[0]
  vertical_pattern = [
      get_column(pattern, col) for col in range(len(num_columns))
  ]
  vert_idx = search_reflection_idx(vertical_pattern, max_diff_count)
  if vert_idx != -1:
    return vert_idx + 1
  return 0


def get_column(pattern, col_idx):
  return "".join([row[col_idx] for row in pattern])


def search_reflection_idx(pattern, max_diff_count):
  n = len(pattern)
  for i in range(n - 1):
    is_match, _ = differs_at_most(pattern[i], pattern[i + 1], max_diff_count)
    if is_match and is_reflection(pattern, i, max_diff_count):
      return i
  return -1


def is_reflection(pattern, idx, max_diff_count):
  i1, i2 = idx, idx + 1
  cnt_not_exact = 0
  while i1 >= 0 and i2 < len(pattern):
    is_match, is_exact_match = differs_at_most(pattern[i1], pattern[i2],
                                               max_diff_count)
    if not is_match:
      return False
    elif not is_exact_match:
      cnt_not_exact += 1
      if cnt_not_exact > 1:
        return False
    i1 -= 1
    i2 += 1
  return cnt_not_exact == 1


def differs_at_most(line1, line2, max_diff_count):
  cnt_diffs = 0
  for i, cell in enumerate(line1):
    if cell != line2[i]:
      cnt_diffs += 1
      if cnt_diffs > max_diff_count:
        return False, False
  return True, cnt_diffs == 0


if __name__ == '__main__':
  main('input.txt')
