import re

LINE_REGEX = re.compile(r'\.*(\d+|[^\d.\n])')


class Number:

    def __init__(self, value, row, col_start, col_end):
        self.value = value
        self.row = row
        self.col_start = col_start
        self.col_end = col_end

    def get_neighbors(self):
        nbs = [(self.row - 1, col) for col in range(self.col_start - 1, self.col_end + 2)]
        nbs += [(self.row, self.col_start - 1), (self.row, self.col_end + 1)]
        nbs += [(self.row + 1, col) for col in range(self.col_start - 1, self.col_end + 2)]
        return set(nbs)

    def has_any_symbol_as_neighbor(self, symbols):
        nbs = self.get_neighbors()
        for sym in symbols:
            if (sym.row, sym.col) in nbs:
                return True
        return False

    def __str__(self):
        return f"{self.value}@[{self.row}, {self.col_start}..{self.col_end}]"


class Symbol:

    def __init__(self, symbol_char, row, col):
        self.symbol_char = symbol_char
        self.row = row
        self.col = col

    def filter_number_neighbors(self, numbers):
        return [n for n in numbers if n.has_any_symbol_as_neighbor([self])]

    def __str__(self):
        return f"{self.symbol_char}@[{self.row}, {self.col}]"


def read_input(filename):
    with open(filename) as f:
        ret = f.readlines()
    return ret


def parse_line(line, row=0):
    numbers = []
    symbols = []
    offset = 0
    while True:
        match = LINE_REGEX.match(line)
        if match is None:
            break
        start = offset + match.start(1)
        end = offset + match.end(1) - 1  # inclusive
        match_str = match.group(1)
        if match_str.isdigit():
            num = Number(int(match_str),
                         row,
                         start,
                         end)
            numbers.append(num)
        else:
            sym = Symbol(match_str,
                         row,
                         start)
            symbols.append(sym)
        offset += match.end()
        line = line[match.end():]
    return numbers, symbols


def part1():
    lines = read_input("input.txt")
    prev_numbers, prev_symbols = [], []
    total_sum = 0
    for row, line in enumerate(lines):
        curr_numbers, curr_symbols = parse_line(line, row)
        for num in prev_numbers:
            if num.has_any_symbol_as_neighbor(curr_symbols):
                total_sum += num.value
        prev_numbers = []
        for num in curr_numbers:
            if num.has_any_symbol_as_neighbor(curr_symbols + prev_symbols):
                total_sum += num.value
            else:
                prev_numbers.append(num)
        prev_symbols = curr_symbols
    print(total_sum)


def part2():

    total_sum = 0
    lines = read_input("input.txt")

    numbers, gears = [], []
    for row, line in enumerate(lines):
        nums, syms = parse_line(line, row)
        numbers.append(nums)
        gears.append([s for s in syms if s.symbol_char == "*"])

    num_rows = len(gears)
    for row in range(num_rows):
        nums = numbers[row][:]
        if row > 0:
            nums += numbers[row - 1][:]
        if row < num_rows - 1:
            nums += numbers[row + 1][:]
        gs = gears[row]
        for g in gs:
            neighboring_nums = g.filter_number_neighbors(nums)
            if len(neighboring_nums) == 2:
                a, b = neighboring_nums
                total_sum += a.value * b.value

    print(total_sum)


if __name__ == "__main__":
    part2()
