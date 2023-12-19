def main():
  lines = read_input("input.txt")
  dig_plan = parse_dig_plan(lines)
  corners_info = CornersInfo(get_corners(dig_plan))

  print(corners_info.calc_area())


class CornersInfo:

  def __init__(self, corners):
    self._corners = corners
    self._row_info = {}
    self._col_info = {}
    self._init_row_info()
    self._init_col_info()

  def calc_area(self):
    ret = 0
    rects = self.get_rectangles()
    nrows = len(rects)
    ncols = len(rects[0])

    for row, rect_row in enumerate(rects):
      for col, rect in enumerate(rect_row):
        
        (top, left), (bottom, right), is_inside = rect
      
        if not is_inside:
          continue
        
        width = right - left
        height = bottom - top
        right_rect = rects[row][col + 1] if col < ncols - 1 else None
        bottom_rect = rects[row + 1][col] if row < nrows - 1 else None

        has_right_neigbor = right_rect is not None and right_rect[2]
        if not has_right_neigbor:
          width += 1
          
        if bottom_rect is None or not bottom_rect[2]:
          height += 1

        area = width * height

        if col < ncols - 1 and row > 0:
          north_east_rect = rects[row - 1][col + 1]
          if north_east_rect[2] and not has_right_neigbor:
            area -= 1 # correction for overlapping corners           

        #print(f"({top} {left}), ({bottom} {right}): {area}")
        ret += area
      

    return ret
        
  def get_rectangles(self):
    ret = []
    rows = sorted({row for row, _ in self._corners})
    cols = sorted({col for _, col in self._corners})
    row_pairs = list(zip(rows, rows[1:], strict=False))
    col_pairs = list(zip(cols, cols[1:], strict=False))

    for row, (top, bottom) in enumerate(row_pairs):
      rect_row = []
      for col, (left, right) in enumerate(col_pairs):
        if row > 0:
          upper_rect = ret[row - 1][col]
          if self._has_upper_border((top, left)):
            is_inside = not upper_rect[2]
          else:
            is_inside = upper_rect[2]
        elif col > 0:
          left_rect = rect_row[col - 1]
          if self._has_left_border((top, left)):
            is_inside = not left_rect[2]
          else:
            is_inside = left_rect[2]
        else:
          is_inside = self._has_upper_border((top, left))

        rect_row.append(((top, left), (bottom, right), is_inside))

      ret.append(rect_row)

    return ret

  def _has_left_border(self, pos):
    top, bottom = self.get_vert_corners(pos)
    if top is not None and top in "7F":
      return True
    if bottom is not None and bottom in "JL":
      return True
    return False

  def _has_upper_border(self, pos):
    left, right = self.get_horiz_corners(pos)
    if left is not None and left in "FL":
      return True
    if right is not None and right in "7J":
      return True
    return False

  def get_horiz_corners(self, pos):
    row, column = pos
    columns = self._row_info[row]
    for i, (col, _) in enumerate(columns):
      if col > column:
        if i > 0:
          return columns[i - 1][1], columns[i][1]
        else:
          return None, columns[i][1]
    return columns[-1][1], None

  def get_vert_corners(self, pos):
    row, col = pos
    rows_data = self._col_info[col]
    for i, (r, _) in enumerate(rows_data):
      if r > row:
        if i > 0:
          return rows_data[i - 1][1], rows_data[i][1]
        else:
          return None, rows_data[i][1]
    return rows_data[-1][1], None

  def get_corner_type(self, pos):
    if pos in self._corners:
      return self._corners[pos]
    else:
      return None

  def _init_row_info(self):
    for (row, col), corner_type in sorted(self._corners.items()):
      if row not in self._row_info:
        self._row_info[row] = [(col, corner_type)]
      else:
        self._row_info[row].append((col, corner_type))

  def _init_col_info(self):
    corners = sorted([(col, row, corner_type)
                      for (row, col), corner_type in self._corners.items()])
    for col, row, corner_type in corners:
      if col not in self._col_info:
        self._col_info[col] = [(row, corner_type)]
      else:
        self._col_info[col].append((row, corner_type))


def get_corners(dig_plan):
  ret = {}
  pos_info = {}
  pos = (0, 0)
  for d, step in dig_plan:
    if pos not in pos_info:
      pos_info[pos] = (None, d)  # (enter_direction, exit_direction)
    else:
      enter, _ = pos_info[pos]
      pos_info[pos] = (enter, d)

    if d == "U":
      pos = (pos[0] - step, pos[1])
    elif d == "D":
      pos = (pos[0] + step, pos[1])
    elif d == "L":
      pos = (pos[0], pos[1] - step)
    elif d == "R":
      pos = (pos[0], pos[1] + step)

    if pos not in pos_info:
      pos_info[pos] = (d, None)  # (enter_direction, exit_direction)
    else:
      _, exit = pos_info[pos]
      pos_info[pos] = (d, exit)

  for pos, (enter, exit) in pos_info.items():
    corner_type_map = {
        "UR": "F",
        "UL": "7",
        "DR": "L",
        "DL": "J",
        "RU": "J",
        "RD": "7",
        "LU": "L",
        "LD": "F"
    }
    ret[pos] = corner_type_map[enter + exit]

  return ret


def parse_dig_plan(lines):
  ret = []
  for line in lines:
    d, step, _ = line.split(" ")
    ret.append((d, int(step)))
  return ret


def read_input(file_name):
  with open(file_name, 'r') as file:
    ret = file.readlines()
  return ret


if __name__ == "__main__":
  main()
