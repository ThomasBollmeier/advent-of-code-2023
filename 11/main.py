import os


def read_input(filename):
  filepath = os.path.dirname(__file__) + os.sep + filename
  with open(filepath) as f:
    ret = f.readlines()
  return ret  


def part1(filename):
  lines = read_input(filename)
  galaxies = parse_galaxy_positions(lines)
  galaxies = expand_galaxies(galaxies)
  print(sum_of_distances(galaxies))


def part2(filename, expansion_factor):
  lines = read_input(filename)
  galaxies = parse_galaxy_positions(lines)
  galaxies = expand_galaxies(galaxies, expansion_factor)
  print(sum_of_distances(galaxies))


def sum_of_distances(galaxies):
  ret = 0
  n = len(galaxies)
  for i, g1 in enumerate(galaxies):
    for j in range(i + 1, n):
      g2 = galaxies[j]
      delta_row = g2[0] - g1[0] if g2[0] >= g1[0] else g1[0] - g2[0]
      delta_col = g2[1] - g1[1] if g2[1] >= g1[1] else g1[1] - g2[1]
      ret += delta_row + delta_col
  return ret
  

def expand_galaxies(galaxies, expansion_factor=2):
  rows = sorted(list({row for row, _col in galaxies}))
  row_map = expand_indices(rows, expansion_factor)
  cols = sorted(list({col for _row, col in galaxies}))
  col_map = expand_indices(cols, expansion_factor)
  return [(row_map[row], col_map[col]) for row, col in galaxies]


def expand_indices(idxs, expansion_factor):
  idxs = sorted(idxs)
  idxs.insert(0, -1)
  gaps = [a - b - 1 for a, b in zip(idxs[1:], idxs)]
  accum_gaps = []
  accum_gap = 0
  for gap in gaps:
    accum_gap += gap * (expansion_factor - 1)
    accum_gaps.append(accum_gap)
  return dict([(idx, idx + accum_gap) for idx, accum_gap in zip(idxs[1:], accum_gaps)])


def parse_galaxy_positions(lines):
  ret = []
  for row, line in enumerate(lines):
    columns = find_galaxy_cols(line)
    ret += [(row, col) for col in columns]
  return ret


def find_galaxy_cols(line):
  ret = []
  start = 0
  while True:
    col = line.find("#", start)
    if col == -1:
      break
    ret.append(col)
    start = col + 1
  return ret



if __name__ == "__main__":
  part2("input.txt", expansion_factor=1_000_000)
