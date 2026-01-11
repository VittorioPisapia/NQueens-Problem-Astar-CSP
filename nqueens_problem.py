from typing import Tuple, Iterable, Any

State = Tuple[int,...] #Tuple of arbitrary lenghts where all elements are int: A state is a tuple of column indices, one per row already filled. state = (1,3,5) means in row 0 there is a queen in column 1 etc. len(state) gives how many rows are already filled

def is_goal(state: State, n:int) -> bool:
    return len(state) == n

def is_safe(state: State, col:int) -> bool: #is it possible to place next queen in row r at column col?
    r = len(state)

    for rp, cp in enumerate(state):
        if cp == col:
            return False
        elif abs(cp-col) == abs(rp - r):
            return False
    return True

def successors(state: State, n:int) -> Iterable[Tuple[Any,State,int]]:
    for c in range(n):
        if is_safe(state, c):
            next_state = state + (c,)
            yield (c, next_state,1) #produce one by one

def state_key(state: State) -> State:
    return state  #already hashable

def pretty_board(state: State, n: int) -> str:
    lines = []
    for r in range(n):
        row = ["." for _ in range(n)]    
        if r < len(state):
            c = state[r]                
            row[c] = "Q"                 
        lines.append(" ".join(row))      
    return "\n".join(lines)

def count_legal_in_row(state: State, n: int, r: int) -> int:
    count = 0
    for c in range(n):
        ok = True
        for rp, cp in enumerate(state):
            if cp == c:
                ok = False
                break
            if abs(cp - c) == abs(rp - r):
                ok = False
                break
        if ok:
            count += 1
    return count

def h_mrv_next_row(state: State, n: int, scale: int = 1000, dead_penalty: int = 10**9) -> int:

    r = len(state)
    remaining = n - r
    if remaining == 0:
        return 0

    k = count_legal_in_row(state, n, r)  # next row is r
    if k == 0:
        return dead_penalty

    return remaining * scale + (scale // k)