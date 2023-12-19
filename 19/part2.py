def read_input(file_name):
  with open(file_name, 'r') as f:
    ret = f.readlines()
  return ret


class PartsRange:

  def __init__(self,
               xrange=(1, 4000),
               mrange=(1, 4000),
               arange=(1, 4000),
               srange=(1, 4000)):

    self.xrange = xrange
    self.mrange = mrange
    self.arange = arange
    self.srange = srange

  def size(self):
    ret = 1
    for lo, hi in [self.xrange, self.mrange, self.arange, self.srange]:
      ret *= hi - lo + 1
    return ret

  def copy(self):
    return PartsRange(self.xrange, self.mrange, self.arange, self.srange)

  def __str__(self) -> str:
    return f"x: {self.xrange}\tm: {self.mrange}\ta: {self.arange}\ts: {self.srange}"


class Workflow:

  def __init__(self, name, rules):
    self.name = name
    self.rules = rules

  def apply_to(self, parts_range):
    ret = []
    rng = parts_range
    for rule in self.rules:
      result, success_rng, failed_rng = rule.apply_to(rng)
      if success_rng is not None:
        ret.append((result, success_rng))
      rng = failed_rng
      if rng is None:
        break
    return ret

  def __str__(self):
    ret = "Workflow: " + self.name + "\n"
    for rule in self.rules:
      ret += "\t" + str(rule) + "\n"
    return ret


class Rule:

  def __init__(self, result, condition=None):
    self.result = result
    self.condition = condition

  def apply_to(self, parts_range):
    success_rng, failed_rng = self.condition.apply_to(
        parts_range) if self.condition else (parts_range, None)
    return self.result, success_rng, failed_rng

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

  def apply_to(self, parts_range):
    max_value = 10_000
    prng = parts_range.copy()
    attr = self.category + "range"
    lo1, hi1 = getattr(prng, attr)
    if self.op == "<":
      lo2, hi2 = 1, self.value - 1
    else:
      lo2, hi2 = self.value + 1, max_value
    lo = max(lo1, lo2)
    hi = min(hi1, hi2)
    if lo >= hi:
      return None, prng

    if lo1 < lo:
      success_rng = prng
      setattr(success_rng, attr, (lo, hi))
      failed_rng = prng.copy()
      setattr(failed_rng, attr, (lo1, lo - 1))
    else:
      success_rng = prng
      setattr(success_rng, attr, (lo, hi))
      failed_rng = prng.copy()
      setattr(failed_rng, attr, (hi + 1, hi1))

    return success_rng, failed_rng

  def __str__(self):
    return self.category + " " + self.op + " " + str(self.value)


def part2(input_file):
  lines = read_input(input_file)
  workflows = parse_lines(lines)

  total = 0
  todos = [(workflows["in"], PartsRange())]
  while todos:
    new_todos = []
    for wf, parts_range in todos:
      #print(wf.name, parts_range)
      results = wf.apply_to(parts_range)
      for result, new_parts_range in results:
        if result == "A":
          total += new_parts_range.size()
        elif result != "R":
          new_todos.append((workflows[result], new_parts_range))
    todos = new_todos

  print(total)


def parse_lines(lines):
  ret = {}

  for line in lines:
    line = line.strip()
    if not line:
      break
    workflow = parse_workflow(line)
    ret[workflow.name] = workflow

  return ret


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


if __name__ == '__main__':

  part2('input.txt')
