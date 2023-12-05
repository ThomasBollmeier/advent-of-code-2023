import os

class Ranges:

  def __init__(self, ranges):
    self._ranges = sorted(ranges, key=lambda rng: rng[1])

  def get_destination(self, source_val):
    dest_value = source_val
    for dest, src, length in self._ranges:
      if source_val < src:
        return dest_value
      if source_val >= src and source_val < src + length:
        return dest + (source_val - src)
    return dest_value
  
  def get_destination_ranges(self, source_range):
    ret = []
    unmappeds = [source_range]
    for r in self._ranges:
      new_unmappeds = []
      for unmapped in unmappeds:
        parts = Ranges._calc_overlap(unmapped, (r[1], r[2]))
        for rng, overlaps in parts:
          if overlaps:
            ret.append((rng[0] + r[0] - r[1], rng[1]))
          else:
            new_unmappeds.append(rng)
      unmappeds = new_unmappeds
    ret += unmappeds
    return ret
  
  def get_all_destination_ranges(self, source_ranges):
    ret = []
    for source_range in source_ranges:
      ret += self.get_destination_ranges(source_range)
    return set(ret)

  @staticmethod
  def _calc_overlap(rng, other):
    min1, len1 = rng
    min2, len2 = other
    overlap_min = max(min1, min2)
    overlap_max = min(min1 + len1, min2 + len2)
    if overlap_min < overlap_max:
      ret = []
      if min1 < overlap_min:
        ret.append(((min1, overlap_min - min1), False))
      overlap = (overlap_min, overlap_max - overlap_min)
      ret.append((overlap, True))
      if min1 + len1 > overlap_max:
        ret.append(((overlap_max, min1 + len1 -  overlap_max), False))
      return ret
    else:
      return [(rng, False)]
    

def read_input(filename):
  with open(filename) as f:
    ret = f.readlines()
  return ret  


def parse_seeds(lines, line_num):
  line = lines[line_num]
  seeds = line.split(":")[1].split()
  return [int(seed) for seed in seeds], line_num + 1


def skip_empty_lines(lines, line_num):
  n = len(lines)
  while line_num < n:
    line = lines[line_num]
    if not line.strip():
      line_num += 1
    else:
      break
  return line_num


def parse_ranges(lines, line_num):
  n = len(lines)
  line_num += 1
  ranges = []
  while line_num < n:
    line = lines[line_num]
    if not line.strip():
      break
    line_num += 1
    ranges.append([int(i) for i in line.split()])
  return Ranges(ranges), line_num


def get_final_dest_value(source_value, ranges_list):
  ret = source_value
  for ranges in ranges_list:
    ret = ranges.get_destination(ret)
  return ret


def get_final_dest_ranges(source_ranges, ranges_list):
  ret = source_ranges
  for ranges in ranges_list:
    ret = ranges.get_all_destination_ranges(ret)  
  return ret


def part1():
  lines = read_input(os.path.dirname(__file__) + os.sep + "input.txt")
  line_num = 0

  seeds, line_num = parse_seeds(lines, line_num)
  
  line_num = skip_empty_lines(lines, line_num)
  seed_soil, line_num = parse_ranges(lines, line_num)
  
  line_num = skip_empty_lines(lines, line_num)
  soil_fert, line_num = parse_ranges(lines, line_num)

  line_num = skip_empty_lines(lines, line_num)
  fert_water, line_num = parse_ranges(lines, line_num)
  
  line_num = skip_empty_lines(lines, line_num)
  water_light, line_num = parse_ranges(lines, line_num)

  line_num = skip_empty_lines(lines, line_num)
  light_temp, line_num = parse_ranges(lines, line_num)

  line_num = skip_empty_lines(lines, line_num)
  temp_humid, line_num = parse_ranges(lines, line_num)

  line_num = skip_empty_lines(lines, line_num)
  humid_location, line_num = parse_ranges(lines, line_num)

  ranges_list = [
    seed_soil,
    soil_fert,
    fert_water,
    water_light,
    light_temp,
    temp_humid,
    humid_location
  ]

  lowest_location = None
  for seed in seeds:
    location = get_final_dest_value(seed, ranges_list)
    if lowest_location is None or location < lowest_location:
      lowest_location = location
  
  print(lowest_location)


def part2():
  lines = read_input(os.path.dirname(__file__) + os.sep + "input.txt")
  line_num = 0
  
  ranges, line_num = parse_seeds(lines, line_num)
  seed_ranges = []
  n = len(ranges) // 2
  for i in range(n):
    start = ranges[2 * i]
    length = ranges[2 * i + 1]
    seed_ranges.append((start, length))

  line_num = skip_empty_lines(lines, line_num)
  seed_soil, line_num = parse_ranges(lines, line_num)
  
  line_num = skip_empty_lines(lines, line_num)
  soil_fert, line_num = parse_ranges(lines, line_num)

  line_num = skip_empty_lines(lines, line_num)
  fert_water, line_num = parse_ranges(lines, line_num)
  
  line_num = skip_empty_lines(lines, line_num)
  water_light, line_num = parse_ranges(lines, line_num)

  line_num = skip_empty_lines(lines, line_num)
  light_temp, line_num = parse_ranges(lines, line_num)

  line_num = skip_empty_lines(lines, line_num)
  temp_humid, line_num = parse_ranges(lines, line_num)

  line_num = skip_empty_lines(lines, line_num)
  humid_location, line_num = parse_ranges(lines, line_num)

  ranges_list = [
    seed_soil,
    soil_fert,
    fert_water,
    water_light,
    light_temp,
    temp_humid,
    humid_location
  ]

  location_ranges = get_final_dest_ranges(seed_ranges, ranges_list)

  lowest_location = None
  for loc_range in location_ranges:
    location = loc_range[0]
    if lowest_location is None or location < lowest_location:
      lowest_location = location
  
  print(lowest_location)


if __name__ == "__main__":
  part2()
