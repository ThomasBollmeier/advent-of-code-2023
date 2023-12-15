def read_input(file_name):
  with open(file_name, 'r') as f:
    ret = f.read().strip()
    ret = ret.replace('\n', '')
  return ret


def part1(input_file):
  line = read_input(input_file)
  steps = line.split(',')
  result = sum([hash(step) for step in steps])
  print(result)


def part2(input_file):
  line = read_input(input_file)
  steps = line.split(',')
  boxes = {}
  apply_steps(steps, boxes)
  total = 0
  for key, lenses in boxes.items():
    for i, (_, focal_length) in enumerate(lenses):
      total += focusing_power(key, i, focal_length)
  print(total)


def focusing_power(box_key, lense_idx, focal_length):
  return (box_key + 1) * (lense_idx + 1) * focal_length


def apply_steps(steps, boxes):
  for step in steps:
    if step[-1] == "-":
      label = step[:-1]
      remove_lense(boxes, label)
    elif "=" in step:
      label, focal_length = step.split("=")
      insert_lense(boxes, label, int(focal_length))


def insert_lense(boxes, label, focal_length):
  key = hash(label)
  if key not in boxes:
    boxes[key] = [(label, focal_length)]
    return
  found = False
  lenses = boxes[key]
  for i, (lbl, _) in enumerate(lenses):
    if lbl == label:
      lenses[i] = (label, focal_length)
      found = True
      break
  if not found:
    lenses.append((label, focal_length))
  boxes[key] = lenses


def remove_lense(boxes, label):
  key = hash(label)
  if key not in boxes:
    return
  lenses = boxes[key]
  new_lenses = []
  changed = False
  for content in lenses:
    if content[0] != label:
      new_lenses.append(content)
    else:
      changed = True
  if changed:
    boxes[key] = new_lenses


def hash(s):
  ret = 0
  for c in s:
    ret += ord(c)
    ret *= 17
    ret %= 256
  return ret


if __name__ == '__main__':

  part2('input.txt')
