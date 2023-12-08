from collections import namedtuple, Counter
from typing import Dict, Iterable, List, Tuple

Hand = namedtuple('hand', 'cards bid')
CARDS = {
    card: i
    for i, card in enumerate('23456789TJQKA')
}
CARDS_JOKER = {
    card: i
    for i, card in enumerate('J23456789TQKA')
}


def parse_input(input_lines: List[str]) -> Iterable[Hand]:
    for line in input_lines:
        cards, bid = line.split()
        yield Hand(cards, int(bid))


def get_combination(hand: Hand,
                    cards_set: Dict[str, int] = CARDS,
                    cards_counter: Counter = None) -> Tuple[int, Iterable[int]]:
    if not cards_counter:
        cards_counter = Counter(hand.cards)

    _, most_common = cards_counter.most_common(1)[0]
    match most_common:
        case 5:
            combination = 8  # Five of a kind
        case 4:
            combination = 7  # Four of a kind
        case 3:
            if len(cards_counter) == 2:
                combination = 6  # Full house
            else:
                combination = 5  # Three of a kind
        case 2:
            if len(cards_counter) == 3:
                combination = 4  # Two pairs
            else:
                combination = 3  # One pair
        case 1:
            combination = 2  # High card
        case _:
            raise ValueError('Invalid hand')
    return combination, tuple(cards_set[card] for card in hand.cards)


def get_combination_joker(hand: Hand) -> Tuple[int, Iterable[int]]:
    cards = None
    if 'J' in hand.cards:
        cards = Counter(hand.cards)
        if cards['J'] == 5:
            return get_combination(hand, cards_set=CARDS_JOKER)
        jokers = cards['J']
        del cards['J']
        cards[cards.most_common(1)[0][0]] += jokers

    return get_combination(hand, cards_set=CARDS_JOKER, cards_counter=cards)


def part1(input_lines: List[str]) -> int:
    return sum(
        bid * i
        for i, (_, bid) in enumerate(sorted(
            ((get_combination(hand), hand.bid) for hand in parse_input(input_lines)),
            key=lambda x: x[0],
        ), 1)
    )


def part2(input_lines: List[str]) -> int:
    return sum(
        bid * i
        for i, (_, bid) in enumerate(sorted(
            ((get_combination_joker(hand), hand.bid)
             for hand in parse_input(input_lines)),
            key=lambda x: x[0],
        ), 1)
    )
