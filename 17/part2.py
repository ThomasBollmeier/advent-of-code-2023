import os
import heapq


class Todos:

    def __init__(self):
        self._todos = []
        self._states = {}

    def push(self, state, heat_loss):
        if state in self._states:
            prev_heat_losses = self._states[state]
            if prev_heat_losses[-1] <= heat_loss:
                return
            else:
                self._states[state].append(heat_loss)
        else:
            self._states[state] = [heat_loss]
        heapq.heappush(self._todos, (heat_loss, state))

    def pop(self):
        heat_loss, state = heapq.heappop(self._todos)
        try:
            heat_losses = self._states[state]
            heat_losses.pop()
            if not heat_losses:
                del self._states[state]
            else:
                self._states[state] = heat_losses
        except KeyError:
            pass
        return heat_loss, state

    def is_empty(self):
        return len(self._states) == 0


def read_input(file_name):
    file_name = os.path.dirname(__file__) + os.sep + file_name
    with open(file_name, 'r') as f:
        ret = f.readlines()
    return ret


def main(input_file):
    lines = read_input(input_file)
    heat_losses = parse_lines(lines)
    print(f"Heat loss: {find_min_heat_loss(heat_losses)}")


def find_min_heat_loss(heat_losses):
    total = 0
    height = len(heat_losses)
    width = len(heat_losses[0])
    visited = set()
    todos = Todos()
    todos.push((0, 0, ""), 0)
    while not todos.is_empty():
        heat_loss, state = todos.pop()
        row, col = state[0], state[1]
        if (row, col) == (height - 1, width - 1):
            total = heat_loss
            break
        visited.add(state)
        next_states = get_neighbors(state, height, width)
        for next_state in next_states:
            if next_state in visited:
                continue
            next_row, next_col, _ = next_state
            next_heat_loss = heat_loss + accumulate_heat_loss(row, col, next_row, next_col, heat_losses)
            todos.push(next_state, next_heat_loss)
    return total


def accumulate_heat_loss(row, col, next_row, next_col, heat_losses):
    if row == next_row:
        if col < next_col:
            return sum([heat_losses[row][c] for c in range(col + 1, next_col + 1)])
        else:
            return sum([heat_losses[row][c] for c in range(next_col, col)])
    else:
        if row < next_row:
            return sum([heat_losses[r][col] for r in range(row + 1, next_row + 1)])
        else:
            return sum([heat_losses[r][col] for r in range(next_row, row)])


def get_neighbors(state, height, width):
    ret = []
    row, col, dirs = state
    min_steps = 4
    max_steps = 10

    moves = []
    for d in "^v><":
        moves += get_next_moves(dirs, d, min_steps, max_steps)
    valid_moves = [move for move in moves if is_valid_move(row, col, move[0], width, height)]

    for mv, d, steps in valid_moves:
        next_row = row + mv[1]
        next_col = col + mv[0]
        if dirs and dirs[-1] == d:
            next_dirs = dirs + steps * d
        else:
            next_dirs = steps * d
        ret.append((next_row, next_col, next_dirs))
    return ret


def get_next_moves(dirs, d, min_steps, max_steps):
    same_dir = dirs and dirs[-1] == d
    if is_opposite_dir(dirs, d):
        return []
    start = 1 if same_dir else min_steps
    end_incl = max_steps - len(dirs) if same_dir else max_steps
    return [(get_move(d, steps), d, steps) for steps in range(start, end_incl + 1)]


def is_opposite_dir(dirs, d):
    if not dirs:
        return False
    return {
        "^": "v",
        "v": "^",
        ">": "<",
        "<": ">"
    }[dirs[-1]] == d


def is_valid_move(row, col, move, width, height):
    new_row = row + move[1]
    new_col = col + move[0]
    return 0 <= new_row < height and 0 <= new_col < width


def get_move(d, steps):
    return {
        "^": (0, -steps),
        "v": (0, steps),
        ">": (steps, 0),
        "<": (-steps, 0)
    }[d]
            

def parse_lines(lines):
    return [[int(ch) for ch in line.strip()] for line in lines]


if __name__ == '__main__':
    main('input.txt')
