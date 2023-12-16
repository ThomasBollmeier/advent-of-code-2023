def read_input(file_name):
    with open(file_name, 'r') as f:
        ret = f.readlines()
    return ret


def empty(d):
    return [d]


def mirror_slash(d):
    new_directions = {
        (-1, 0): (0, 1),
        (1, 0): (0, -1),
        (0, -1): (1, 0),
        (0, 1): (-1, 0)
    }
    return [new_directions[d]]


def mirror_backslash(d):
    new_directions = {
        (-1, 0): (0, -1),
        (1, 0): (0, 1),
        (0, -1): (-1, 0),
        (0, 1): (1, 0)
    }
    return [new_directions[d]]


def split_vert(d):
    dx, dy = d
    if dx == 0:
        return [d]
    return [(0, -dx), (0, dx)]


def split_horiz(d):
    dx, dy = d
    if dy == 0:
        return [d]
    return [(-dy, 0), (dy, 0)]


def part1(input_file):
    lines = read_input(input_file)
    beam_transformers = parse_lines(lines)
    print(count_energized_tiles(((0, 0), (1, 0)), beam_transformers))


def part2(input_file):
    lines = read_input(input_file)
    beam_transformers = parse_lines(lines)
    width = len(beam_transformers[0])
    height = len(beam_transformers)
    start_beams = create_start_beams(width, height)
    counts = [count_energized_tiles(b, beam_transformers) for b in start_beams]
    print(max(*counts))


def create_start_beams(w, h):
    ret = []
    ret += [((0, y), (1, 0)) for y in range(h)]
    ret += [((w - 1, y), (-1, 0)) for y in range(h)]
    ret += [((x, 0), (0, 1)) for x in range(w)]
    ret += [((x, h - 1), (0, -1)) for x in range(w)]
    return ret


def count_energized_tiles(start_beam, beam_transformers):
    width = len(beam_transformers)
    height = len(beam_transformers[0])

    energized = set()
    visited = set()
    beams = [start_beam]
    while beams:
        next_beams = []
        for beam in beams:
            pos, d = beam
            energized.add(pos)
            visited.add(beam)
            transformer = beam_transformers[pos[1]][pos[0]]
            for next_dir in transformer(d):
                next_x, next_y = pos[0] + next_dir[0], pos[1] + next_dir[1]
                if 0 <= next_x < width and 0 <= next_y < height:
                    next_beam = ((next_x, next_y), next_dir)
                    if next_beam not in visited:
                        next_beams.append(next_beam)
        beams = next_beams

    return len(energized)


def parse_lines(lines):
    return [parse_line(line.strip()) for line in lines]


transformer_map = {
    ".": empty,
    "/": mirror_slash,
    "\\": mirror_backslash,
    "|": split_vert,
    "-": split_horiz
}


def parse_line(line):
    return [transformer_map[ch] for ch in line]


if __name__ == '__main__':
    part2('input.txt')
