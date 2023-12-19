def read_input(file_name):
  with open(file_name, 'r') as f:
    ret = f.readlines()
  return ret


class Part:

  def __init__(self, x=0, m=0, a=0, s=0):
    self.x = x
    self.m = m
    self.a = a
    self.s = s

  def rating(self):
    return self.x + self.m + self.a + self.s

  def __str__(self) -> str:
    return f"Part(x={self.x}, m={self.m}, a={self.a}, s={self.s})"


class Workflow:

  def __init__(self, name, rules):
    self.name = name
    self.rules = rules

  def process(self, part):
    for rule in self.rules:
      result = rule.apply(part)
      if result is not None:
        return result
    return None

  def __str__(self):
    ret = "Workflow: " + self.name + "\n"
    for rule in self.rules:
      ret += "\t" + str(rule) + "\n"
    return ret


class Rule:

  def __init__(self, result, condition=None):
    self.result = result
    self.condition = condition

  def apply(self, part):
    if self.condition is None or self.condition.applies_to(part):
      return self.result
    return None

  def __str__(self):
    ret = "Rule: " + self.result
    if self.condition:
      ret += " if " + str(self.condition)
    return ret


class Condition:

  def __init__(self, category, op, value):
    self.category = category
    self.op = op
    self.value = value

  def applies_to(self, part):
    part_value = getattr(part, self.category)
    if self.op == '>':
      return part_value > self.value
    if self.op == '<':
      return part_value < self.value
    return False

  def __str__(self):
    return self.category + " " + self.op + " " + str(self.value)


def part1(input_file):
  lines = read_input(input_file)
  workflows, parts = parse_lines(lines)

  total = 0
  for part in parts:
    result = process(part, workflows)
    if result == "A":
      total += part.rating()
  print(total)

def process(part, workflows):
  current_workflow = workflows["in"]
  while True:
    result = current_workflow.process(part)
    if result in "AR":
      return result
    current_workflow = workflows[result]


def parse_lines(lines):
  workflows = {}
  parts = []
  parse_workflows = True

  for line in lines:
    line = line.strip()
    if not line:
      parse_workflows = False
      continue
    if parse_workflows:
      workflow = parse_workflow(line)
      workflows[workflow.name] = workflow
    else:
      parts.append(parse_part(line))

  return workflows, parts


def parse_workflow(line) -> Workflow:
  name, rules_str = line.split("{")
  rules_str = rules_str[:-1]
  rules = []
  for rule_str in rules_str.split(","):
    rule = parse_rule(rule_str)
    rules.append(rule)

  ret = Workflow(name, rules)
  return ret


def parse_rule(rule_str) -> Rule:
  if ":" in rule_str:
    condition_str, result = rule_str.split(":")
    category = condition_str[0]
    op = condition_str[1]
    value = int(condition_str[2:])
    condition = Condition(category, op, value)
  else:
    condition = None
    result = rule_str
  return Rule(result, condition)


def parse_part(line):
  ret = Part()
  items = line[1:-1].split(",")
  for item in items:
    category = item[0]
    value = int(item[2:])
    setattr(ret, category, value)
  return ret


if __name__ == '__main__':

  part1('input.txt')
