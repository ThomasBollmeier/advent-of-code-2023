import os
import heapq


def read_input(file_name):
    file_name = os.path.dirname(__file__) + os.sep + file_name
    with open(file_name, 'r') as f:
        ret = f.readlines()
    return ret


def main(input_file):
    lines = read_input(input_file)
    heat_losses = parse_lines(lines)
    print(find_min_heat_loss(heat_losses))


def find_min_heat_loss(heat_losses):
    total = 0
    height = len(heat_losses)
    width = len(heat_losses[0])
    visited = set()
    todo = []
    heapq.heappush(todo, (0, (0, 0, "")))
    while todo:
        heat_loss, state = heapq.heappop(todo)
        pos = (state[0], state[1])
        if pos == (height - 1, width - 1):
            total = heat_loss
            break
        visited.add(state)
        next_states = get_neighbors(state, height, width)
        for next_state in next_states:
            if next_state in visited:
                continue
            next_row, next_col, _ = next_state
            next_heat_loss = heat_loss + heat_losses[next_row][next_col]
            found = False
            for i, (hl, st) in enumerate(todo):
                if st == next_state:
                    if hl > next_heat_loss:
                        todo[i] = (next_heat_loss, st)
                    found = True
                    break
            if not found:
                heapq.heappush(todo, (next_heat_loss, next_state))

    return total


def get_neighbors(state, height, width):
    ret = []
    row, col, dirs = state
    if row > 0:
        if dirs != "^^^" and not (dirs and dirs[-1] == "v"):
            ret.append((row - 1, col, next_dir(dirs, "^")))
    if row < height - 1:
        if dirs != "vvv" and not (dirs and dirs[-1] == "^"):
            ret.append((row + 1, col, next_dir(dirs, "v")))
    if col > 0:
        if dirs != "<<<" and not (dirs and dirs[-1] == ">"):
            ret.append((row, col - 1, next_dir(dirs, "<")))
    if col < width - 1:
        if dirs != ">>>" and not (dirs and dirs[-1] == "<"):
            ret.append((row, col + 1, next_dir(dirs, ">")))
    return ret


def next_dir(dirs, d):
    if not dirs:
        return d
    else:
        return d if dirs[-1] != d else dirs + d
            

def parse_lines(lines):
    return [[int(ch) for ch in line.strip()] for line in lines]


if __name__ == '__main__':
    main('test.txt')
