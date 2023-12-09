from collections import namedtuple
from functools import cache
from itertools import chain, groupby, islice, pairwise
from typing import Iterable, List, Tuple

SeedMap = namedtuple('seed_map', 'dest source length')


def parse_input(input_lines: List[str]) -> Tuple[Iterable[int],
                                                 Iterable[Iterable[SeedMap]]]:
    return (
        int(seed) for seed in input_lines[0].split(': ')[1].split()
    ), tuple(
        tuple(SeedMap(*map(int, line.split())) for line in islice(group, 1, None))
        for k, group in groupby(input_lines[1:], lambda line: line == '')
        if not k
    )


def apply_map(seed: int, seed_map: Iterable[SeedMap]) -> int:
    for seed_map in seed_map:
        if seed in range(seed_map.source, seed_map.source + seed_map.length):
            return seed_map.dest + seed - seed_map.source
    return seed

@cache
def apply_map_line(seed: int, seed_map: SeedMap) -> int:
    if seed in range(seed_map.source, seed_map.source + seed_map.length):
        return seed_map.dest + seed - seed_map.source
    return seed


def part1(input_lines: List[str]) -> int:
    seeds, maps = parse_input(input_lines)
    for seed_map in maps:
        seeds = tuple(apply_map(seed, seed_map) for seed in seeds)
    return min(seeds)


def part2(input_lines: List[str]) -> int:
    # Parse input and generate seed pairs
    seed_ranges, maps = parse_input(input_lines)
    seed_pairs = list(chain((
        (seed_start, seed_start + seed_len)
        for seed_start, seed_len in islice(pairwise(seed_ranges), None, None, 2)
    )))

    for map_i, seed_map in enumerate(maps):
        # Sort seed pairs by start point
        seed_map = tuple(sorted(seed_map, key=lambda m: m.source))
        new_seed_pairs = []

        for seed_start, seed_end in seed_pairs:
            # Find maps that intersect with the current seed pair
            maps_to_apply = tuple(filter(
                lambda m: (
                    m.source <= seed_end and
                    m.source + m.length - 1 >= seed_start
                ),
                seed_map
            ))

            # If there are no maps to apply, save the seed pair and continue
            if not maps_to_apply:
                new_seed_pairs.append((seed_start, seed_end))
                continue

            # If first maps start further than the seed pair strat point,
            # save the range between start point and first map
            if maps_to_apply[0].source > seed_start:
                new_seed_pairs.append((seed_start, maps_to_apply[0].source - 1))
                seed_start = maps_to_apply[0].source

            # Save all ranges that are not covered by maps
            for map1, map2 in pairwise(maps_to_apply):
                if map1.source + map1.length < map2.source:
                    new_seed_pairs.append(
                        (map1.source + map1.length + 1, map2.source - 1)
                    )

            # If last maps end before the seed pair end point,
            # save the range between last map and end point
            if maps_to_apply[-1].source + maps_to_apply[-1].length - 1 < seed_end:
                new_seed_pairs.append(
                    (maps_to_apply[-1].source + maps_to_apply[-1].length, seed_end)
                )
                seed_end = maps_to_apply[-1].source + maps_to_apply[-1].length - 1

            for map_line, next_map_line in pairwise(maps_to_apply):
                new_seed_pairs.append((
                    apply_map_line(seed_start, map_line),
                    apply_map_line(map_line.source + map_line.length - 1, map_line)
                ))
                seed_start = next_map_line.source

            new_seed_pairs.append((
                apply_map_line(seed_start, maps_to_apply[-1]),
                apply_map_line(seed_end, maps_to_apply[-1])
            ))

        seed_pairs = new_seed_pairs

    return min(pair[0] for pair in seed_pairs)
