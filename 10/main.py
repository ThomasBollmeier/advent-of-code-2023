import os

class Pipe:
  NS = "|"
  EW = "-"
  SE = "F"
  SW = "7"
  NW = "J"
  NE = "L"
  GROUND = "."
  START = "S"


class Direction:
  NORTH = (-1, 0)
  SOUTH = (1, 0)
  EAST = (0, 1)
  WEST = (0, -1)


def opposite_dir(d):
  drow, dcol = d
  return (-drow, -dcol)


PIPE_DIRECTIONS = {
  Pipe.NS: [Direction.NORTH, Direction.SOUTH],
  Pipe.EW: [Direction.EAST, Direction.WEST],
  Pipe.SE: [Direction.SOUTH, Direction.EAST],
  Pipe.SW: [Direction.SOUTH, Direction.WEST],
  Pipe.NW: [Direction.NORTH, Direction.WEST],
  Pipe.NE: [Direction.NORTH, Direction.EAST],
}
  

def read_input(filename):
  filepath = os.path.dirname(__file__) + os.sep + filename
  with open(filepath) as f:
    ret = f.readlines()
  return ret  


def part1():
  maze = read_input("input.txt")
  start = find_start(maze)
  print(find_largest_distance(maze, start))


def find_start(maze):
  for row_idx, row in enumerate(maze):
    for col_idx, pipe in enumerate(row):
      if pipe == Pipe.START:
        return row_idx, col_idx
  return None


def find_largest_distance(maze, start):
  ret = 0
  pos1 = pos2 = start
  dir1, dir2 = find_start_directions(maze, start)
  
  while True:
    ret += 1
    pos1, dir1 = move(maze, pos1, dir1)
    pos2, dir2 = move(maze, pos2, dir2)
    if pos1 == pos2:
      break

  return ret


def move(maze, pos, dir):
  next_pos = (pos[0] + dir[0], pos[1] + dir[1])
  row, col = next_pos
  next_dirs = PIPE_DIRECTIONS[maze[row][col]][:]
  next_dirs.remove(opposite_dir(dir))
  return next_pos, next_dirs[0]


def find_start_directions(maze, start):
  ret = []
  srow, scol = start

  if srow > 0:
    neighbor = maze[srow - 1][scol]
    if neighbor in PIPE_DIRECTIONS and Direction.SOUTH in PIPE_DIRECTIONS[neighbor]:
      ret.append(Direction.NORTH)

  if srow < len(maze) - 1:
    neighbor = maze[srow + 1][scol]
    if neighbor in PIPE_DIRECTIONS and Direction.NORTH in PIPE_DIRECTIONS[neighbor]:
      ret.append(Direction.SOUTH)

  if scol > 0:
    neighbor = maze[srow][scol - 1]
    if neighbor in PIPE_DIRECTIONS and Direction.EAST in PIPE_DIRECTIONS[neighbor]:
      ret.append(Direction.WEST)

  if scol < len(maze[srow]) - 1:
    neighbor = maze[srow][scol + 1]
    if neighbor in PIPE_DIRECTIONS and Direction.WEST in PIPE_DIRECTIONS[neighbor]:
      ret.append(Direction.EAST)
  
  if len(ret) != 2:
    raise Exception("There must exactly be two connected pipes")

  return ret


def part2():
  maze = read_input("input.txt")
  start = find_start(maze)
  print(calc_enclosed_area(maze, start))


def calc_enclosed_area(maze, start):
  ret = 0
  loop = get_loop(maze, start)
  line = []
  prev_row = None
  for pos, pipe in loop:
    if prev_row is None or pos[0] != prev_row:
      if line:
        ret += calc_enclosed(line)
      line = []
    if pipe != Pipe.EW:
      line.append((pos[1], pipe))
    prev_row = pos[0]

  if line:
    ret += calc_enclosed(line)
  
  return ret


def calc_enclosed(line):
  ret = 0
  pairs = list(zip(line, line[1:]))
  state = (0, 1) # left outside, right inside
  for pair in pairs:
    left_pipe = pair[0][1]
    right_pipe = pair[1][1]
    next_state = switch(state) \
        if (left_pipe, right_pipe) not in {(Pipe.SE, Pipe.NW), (Pipe.NE, Pipe.SW)} \
        else state
    if state[1] and next_state[0]: # both inside
      if right_pipe not in {Pipe.NW, Pipe.SW}:
        num_enclosed = pair[1][0] - pair[0][0] - 1
        ret += num_enclosed
    state = next_state

  return ret


def switch(state):
  left, right = state
  return ((left + 1) % 2, (right + 1) % 2)


def get_loop(maze, start):
  pos1 = pos2 = start
  dir1, dir2 = find_start_directions(maze, start)
  start_pipe = None
  for pipe, dirs in PIPE_DIRECTIONS.items():
    if dir1 in dirs and dir2 in dirs:
      start_pipe = pipe
      break
  loop = {(start, start_pipe)}
  
  while True:
    pos1, dir1 = move(maze, pos1, dir1)
    pos2, dir2 = move(maze, pos2, dir2)
    loop.add((pos1, maze[pos1[0]][pos1[1]]))
    loop.add((pos2, maze[pos2[0]][pos2[1]]))
    if pos1 == pos2:
      break

  return sorted(list(loop))


if __name__ == "__main__":
  part2()
