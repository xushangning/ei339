import re

drawn_lines = None
# map each line to a unique number e.g (1, 2) -> 0
number_pair_to_line_number = {
    (1, 2): 0, (1, 3): 1, (2, 3): 2, (2, 4): 3, (2, 5): 4, (3, 5): 5, (3, 6): 6,
    (4, 5): 7, (5, 6): 8, (4, 7): 9, (4, 8): 10, (5, 8): 11,(5, 9): 12,
    (6, 9): 13, (6, 10): 14, (7, 8): 15, (8, 9): 16, (9, 10): 17
}
# For line i, line_triangles[i] contains a tuple of pairs of line numbers. e.g.
# line_triangles[0] contains (1, 2), which means that the line 0 can form a
# triangle with line 1 and line 2.
line_triangles = (
    ((1, 2),),
    ((0, 2),),
    ((0, 1), (4, 5)),
    ((4, 7),),
    ((3, 7), (2, 5)),
    ((2, 4), (6, 8)),
    ((5, 8),),
    ((3, 4), (10, 11)),
    ((5, 6), (12, 13)),
    ((10, 15),),
    ((9, 15), (7, 11)),
    ((7, 10), (12, 16)),
    ((11, 16), (8, 13)),
    ((8, 12), (14, 17)),
    ((13, 17),),
    ((9, 10),),
    ((11, 12),),
    ((13, 14),)
)


def score_by_line(line: int) -> int:
    """
    Return the number of points that will be earned if line is added to
    drawn_lines.
    """
    points = 0
    for a, b in line_triangles[line]:
        points += a in drawn_lines and b in drawn_lines
    return points


def value(lines_not_drawn: list, alpha: int, beta: int, is_max: bool) -> int:
    if len(lines_not_drawn) == 1:
        v = score_by_line(lines_not_drawn[0])
        return v if is_max else -v

    if is_max:
        v = -100
        for i in range(len(lines_not_drawn)):
            drawn_lines.add(lines_not_drawn[i])
            l_copy = lines_not_drawn.copy()
            del l_copy[i]
            # points scored by drawing the line
            points = score_by_line(lines_not_drawn[i])
            v = max(
                v,
                # A draws an extra line if they scores
                value(l_copy, alpha, beta, points > 0) + points
            )
            drawn_lines.remove(lines_not_drawn[i])
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    v = 100
    for i in range(len(lines_not_drawn)):
        drawn_lines.add(lines_not_drawn[i])
        l_copy = lines_not_drawn.copy()
        del l_copy[i]
        points = score_by_line(lines_not_drawn[i])
        v = min(
            v,
            # B draws an extra line if they scores
            value(l_copy, alpha, beta, points == 0) - score_by_line(lines_not_drawn[i])
        )
        drawn_lines.remove(lines_not_drawn[i])
        if v <= alpha:
            return v
        beta = min(beta, v)
    return v


if __name__ == '__main__':
    drawn_lines = set()
    A_turn = True
    score = 0
    # parse the list of drawn lines of the form (a, b)
    for p1, p2 in re.findall(r'\((\d+), (\d+)\)', input()):
        line = number_pair_to_line_number[(int(p1), int(p2))]
        points = score_by_line(line)
        drawn_lines.add(line)
        score += points if A_turn else - points
        if points == 0:
            A_turn = not A_turn

    lines_not_drawn = list(frozenset(range(18)) - drawn_lines)
    score += value(lines_not_drawn, -100, 100, A_turn)
    if score > 0:
        print('A')
    elif score == 0:
        print('DRAW')
    else:
        print('B')
