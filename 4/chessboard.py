from functools import lru_cache

n = 0


def valid_position(r: int, c: int) -> bool:
    return 0 <= r < n and 0 <= c < n


def next_white_positions(r: int, c: int):
    """
    The generator for the white piece's next positions, given its position
    (r, c).
    """
    c += 1
    if valid_position(r, c):
        yield r, c
    c -= 2
    if valid_position(r, c):
        yield r, c
    c += 1
    r += 1
    if valid_position(r, c):
        yield r, c
    r -= 2
    if valid_position(r, c):
        yield r, c


def next_black_positions(r: int, c: int):
    """
    The generator for the black piece's next positions, given its position
    (r, c). The black piece has at most 8 possible next positions.
    """
    for pos in next_white_positions(r, c):
        yield pos

    c += 2
    if valid_position(r, c):
        yield r, c
    c -= 4
    if valid_position(r, c):
        yield r, c
    c += 2
    r += 2
    if valid_position(r, c):
        yield r, c
    r -= 4
    if valid_position(r, c):
        yield r, c


@lru_cache(None)
def value(r1: int, c1: int, r2: int, c2, depth: int, is_max: bool) -> int:
    """
    reward = 100 if B wins and reward = -100 if A wins. Every round incurs a
    reward of -1.

    B is assigned to be the maximizer so that they will try to win with fewest
    rounds possible, and A as the minimizer tries to maximize the number of
    rounds.
    """
    if r1 == r2 and c1 == c2:
        # If is_max is true, then last move is A's move, so A wins.
        return (-100 if is_max else 100) - depth
    elif depth > 4 * n:
        return - 4 * n - 1

    if is_max:
        max_value = -100
        for r, c in next_black_positions(r2, c2):
            temp = value(r1, c1, r, c, depth + 1, False)
            if max_value < temp:
                max_value = temp
        return max_value

    min_value = 100
    for r, c in next_white_positions(r1, c1):
        temp = value(r, c, r2, c2, depth + 1, True)
        if min_value > temp:
            min_value = temp
    return min_value


if __name__ == '__main__':
    params = [x - 1 for x in map(int, input().split(' '))]
    n = params[0] + 1
    if (params[1] == params[3] and abs(params[2] - params[4]) == 1
            or params[2] == params[4] and abs(params[1] - params[3]) == 1):
        print("WHITE 1")
    else:
        print("BLACK", 100 - value(params[1], params[2], params[3], params[4], 0, False))
