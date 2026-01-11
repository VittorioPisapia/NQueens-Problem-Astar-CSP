from dataclasses import dataclass
from typing import Callable, Dict, Generic, Iterable, Optional, Set, Tuple, TypeVar, Any, List
import heapq
import time

S = TypeVar("S")


@dataclass
class AStarResult(Generic[S]):
    found : bool
    solution_state : Optional[S]
    solution_actions : List[Any]
    g_cost : Optional[int]
    runtime_s : float
    expanded : int
    generated : int
    branching_min : int
    branching_max : int
    branching_avg : float
    peak_nodes_in_memory : int

def _reconstruct_actions(came_from: Dict[Any, Tuple[Any, Any]], goal_key : Any) -> List[Any]:   #Dict[state, Tuple[parent, action]]
    actions : List[Any] = []
    cur = goal_key
    while cur in came_from:  #se cur é figlio di qualcosa
        parent_key, action = came_from[cur]
        actions.append(action)
        cur = parent_key
    actions.reverse()
    return actions

def astar_search(
    initial_state : S,
    is_goal : Callable[[S], bool],
    successors : Callable[[S], Iterable[Tuple[Any, S, int]]],
    heuristic : Callable[[S], int],
    state_key : Callable[[S], Any],
) -> AStarResult[S]:
    
    t0 = time.perf_counter()
    frontier : List[Tuple[int, int, int, Any, S]] = [] #(f, tie, g, key, state)
    tie = 0

    start_key = state_key(initial_state)
    g_best : Dict[Any, int] = {start_key : 0}
    came_from : Dict[Any, Tuple[Any, Any]] = {}
    explored :Set[Any] = set()

    f0 = heuristic(initial_state)
    heapq.heappush(frontier, (f0, tie, 0, start_key, initial_state))

    expanded = 0
    generated = 0
    b_min = 10**9
    b_max = 0
    b_sum = 0
    peak_mem = 1

    while frontier:
        peak_mem = max(peak_mem, len(frontier) + len(explored))
        f, _, g, key, state = heapq.heappop(frontier)  #pop best node - lowest f

        if g != g_best.get(key, None):
            continue #if we got better g, ignore this iteration of loop

        if is_goal(state):

            runtime = time.perf_counter() - t0

            actions = _reconstruct_actions(came_from, key)
            avg_b = b_sum / expanded if expanded > 0 else 0.0
            return AStarResult(
                found=True,
                solution_state=state,
                solution_actions=actions,
                g_cost=g,
                runtime_s=runtime,
                expanded=expanded,
                generated=generated,
                branching_min=(0 if b_min == 10**9 else b_min),
                branching_max=b_max,
                branching_avg=avg_b,
                peak_nodes_in_memory=peak_mem,
            )
        
        explored.add(key)
        expanded += 1
        succs = list(successors(state))
        generated += len(succs)

        b = len(succs)
        b_min = min(b_min, b)
        b_max = max(b_max, b)
        b_sum += b

        for action, nxt, step_cost in succs:
            nxt_key = state_key(nxt)
            if nxt_key in explored:
                continue
            tentative_g = g + step_cost
            old_g = g_best.get(nxt_key)

            if old_g is None or tentative_g < old_g:
                g_best[nxt_key] = tentative_g
                came_from[nxt_key] = (key, action)
                tie += 1
                fn = tentative_g + heuristic(nxt)
                heapq.heappush(frontier, (fn, tie, tentative_g, nxt_key, nxt))


    runtime = time.perf_counter() - t0
    avg_b = (b_sum / expanded) if expanded > 0 else 0.0
    return AStarResult(
        found=False,
        solution_state=None,
        solution_actions=[],
        g_cost=None,
        runtime_s=runtime,
        expanded=expanded,
        generated=generated,
        branching_min=(0 if b_min == 10**9 else b_min),
        branching_max=b_max,
        branching_avg=avg_b,
        peak_nodes_in_memory=peak_mem,
    )
