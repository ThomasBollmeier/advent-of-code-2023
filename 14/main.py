def read_input(file_name):
  with open(file_name, 'r') as f:
    ret = f.readlines()
  return ret


def part1(input_file):
  platform = create_platform(read_input(input_file))
  positions = get_positions(platform)
  limits = get_limits(platform)
  tilted = tilt_positions(positions, limits, Direction.NORTH)
  print(calc_total_load(len(platform), tilted))


def part2(input_file):

  N = 1000000000
  MAX_ITER = 1000

  platform = create_platform(read_input(input_file))
  positions = get_positions(platform)
  limits = get_limits(platform)
  height = len(platform)

  result = find_period_with_start(height, positions, limits, MAX_ITER)
  if result:
    start, period = result
    print(period[(N - 1 - start) % len(period)])
  else:
    print('No solution found')


def create_platform(lines):
  ret = []
  for line in lines:
    ret.append(line.strip())
  return ret


def get_left_limits(cells):
  ret = []
  curr_limit = 0
  for idx, cell in enumerate(cells):
    ret.append(curr_limit)
    if cell == '#':
      curr_limit = idx + 1
  return ret


def get_right_limits(cells):
  ret = []
  i = 0
  n = len(cells)
  curr_limit = n - 1
  for i in range(n - 1, -1, -1):
    ret.append(curr_limit)
    if cells[i] == '#':
      curr_limit = i - 1
  ret = list(reversed(ret))
  return ret


class Direction:
  NORTH = 1
  SOUTH = 2
  WEST = 3
  EAST = 4


def get_positions(platform):
  positions = set()
  for row_idx, row in enumerate(platform):
    for col_idx, cell in enumerate(row):
      if cell == 'O':
        positions.add((row_idx, col_idx))
  return positions


def get_limits(platform):
  limits = {}

  for row_idx, row in enumerate(platform):
    left_limits = get_left_limits(row)
    for col_idx, left_limit in enumerate(left_limits):
      limits[(row_idx, col_idx)] = {Direction.WEST: (row_idx, left_limit)}
    right_limits = get_right_limits(row)
    for col_idx, right_limit in enumerate(right_limits):
      limits[(row_idx, col_idx)][Direction.EAST] = (row_idx, right_limit)

  width = len(platform[0])
  for col_idx in range(width):
    column = [row[col_idx] for row in platform]
    left_limits = get_left_limits(column)
    for row_idx, left_limit in enumerate(left_limits):
      limits[(row_idx, col_idx)][Direction.NORTH] = (left_limit, col_idx)
    right_limits = get_right_limits(column)
    for row_idx, right_limit in enumerate(right_limits):
      limits[(row_idx, col_idx)][Direction.SOUTH] = (right_limit, col_idx)

  return limits


def tilt_positions(positions, limits, direction):
  ret = set()
  stats = {}
  for pos in positions:
    limit_pos = limits[pos][direction]
    stats[limit_pos] = stats.get(limit_pos, 0) + 1
  for pos, count in stats.items():
    for new_pos in expand(pos, count, direction):
      ret.add(new_pos)
  return ret


def expand(pos, count, direction):
  row, col = pos
  if direction == Direction.NORTH:
    return [(row + i, col) for i in range(count)]
  elif direction == Direction.SOUTH:
    return [(row - i, col) for i in range(count)]
  elif direction == Direction.WEST:
    return [(row, col + i) for i in range(count)]
  else:
    return [(row, col - i) for i in range(count)]


def cycle(positions, limits):
  ret = tilt_positions(positions, limits, Direction.NORTH)
  ret = tilt_positions(ret, limits, Direction.WEST)
  ret = tilt_positions(ret, limits, Direction.SOUTH)
  ret = tilt_positions(ret, limits, Direction.EAST)
  return ret


def calc_total_load(height, positions):
  return sum([height - row for row, _ in positions])


def find_period(values):
  n = len(values)
  max_period = n // 2
  for period in range(1, max_period + 1):
    n_periods = n // period
    period_values = values[:period]
    period_found = True
    for i in range(1, n_periods):
      offset = i * period
      if values[offset:offset + period] != period_values:
        period_found = False
        break
    if period_found:
      return period_values
  return None


def find_period_with_start(height, start_position, limits, max_iter):
  HISTORY_SIZE = 100
  load_history = []

  positions = start_position

  for i in range(max_iter):
    positions = cycle(positions, limits)
    load = calc_total_load(height, positions)
    if len(load_history) >= HISTORY_SIZE:
      load_history.pop()
    load_history.insert(0, load)

    if len(load_history) == HISTORY_SIZE:
      period = find_period(load_history)
      if period is not None:
        forward_period = list(reversed(period[1:]))
        forward_period.insert(0, period[0])
        return i, forward_period

  return None


if __name__ == '__main__':

  part1('input.txt')
  part2('input.txt')
