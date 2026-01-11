import csv
import time
from typing import Optional, Tuple

from astar import astar_search
from nqueens_problem import is_goal, successors, state_key, State, h_mrv_next_row
from nqueens_csp import solve_nqueens_csp


def check_solution(placement: Tuple[int, ...], n: int) -> bool:
    if placement is None or len(placement) != n:
        return False
    for r1 in range(n):
        c1 = placement[r1]
        for r2 in range(r1 + 1, n):
            c2 = placement[r2]
            if c1 == c2:
                return False
            if abs(c1 - c2) == abs(r1 - r2):
                return False
    return True


def run_astar(n: int, heuristic_name: str):
    initial: State = ()
    goal_fn = lambda s: is_goal(s, n)
    succ_fn = lambda s: successors(s, n)

    if heuristic_name == "baseline_remaining":
        h = lambda s: n - len(s)
    elif heuristic_name == "mrv_next_row":
        h = lambda s: h_mrv_next_row(s, n)
    else:
        raise ValueError(f"Unknown heuristic: {heuristic_name}")

    res = astar_search(
        initial_state=initial,
        is_goal=goal_fn,
        successors=succ_fn,
        heuristic=h,
        state_key=state_key,
    )

    placement = res.solution_state if res.found else None
    valid = check_solution(placement, n) if res.found else False

    return {
        "method": "astar",
        "heuristic": heuristic_name,
        "n": n,
        "found": res.found,
        "valid": valid,
        "runtime_s": res.runtime_s,
        "expanded": res.expanded,
        "generated": res.generated,
        "peak_mem": res.peak_nodes_in_memory,
        "branching_min": res.branching_min,
        "branching_avg": res.branching_avg,
        "branching_max": res.branching_max,
        # CSP-only fields:
        "status": "",
        "conflicts": "",
        "branches": "",
        "wall_time_s": "",
    }


def run_csp(n: int, time_limit_s: Optional[float] = None):
    res = solve_nqueens_csp(n, time_limit_s=time_limit_s)

    valid = check_solution(res.placement, n) if res.found else False

    return {
        "method": "csp",
        "heuristic": "",
        "n": n,
        "found": res.found,
        "valid": valid,
        "runtime_s": res.runtime_s,
        # A*-only fields:
        "expanded": "",
        "generated": "",
        "peak_mem": "",
        "branching_min": "",
        "branching_avg": "",
        "branching_max": "",
        # CSP fields:
        "status": res.status_name,
        "conflicts": res.conflicts,
        "branches": res.branches,
        "wall_time_s": res.wall_time_s,
    }


def main():
    astar_ns = [4, 6, 8, 10, 12, 13]
    csp_ns = [4,6, 8, 20, 50, 100,150,200]

    out_csv = "results.csv"
    fieldnames = [
        "method", "heuristic", "n", "found", "valid", "runtime_s",
        "expanded", "generated", "peak_mem",
        "branching_min", "branching_avg", "branching_max",
        "status", "conflicts", "branches", "wall_time_s",
    ]

    rows = []

    for n in astar_ns:
        for hname in ["baseline_remaining", "mrv_next_row"]:
            print(f"[A*] n={n} heuristic={hname}")
            row = run_astar(n, hname)
            rows.append(row)

    for n in csp_ns:
        print(f"[CSP] n={n}")
        row = run_csp(n, time_limit_s=None)
        rows.append(row)

    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nWrote {len(rows)} rows to {out_csv}")


if __name__ == "__main__":
    main()
