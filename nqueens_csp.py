from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Tuple
import time

from ortools.sat.python import cp_model


@dataclass
class CSPResult:
    found: bool
    placement: Optional[Tuple[int, ...]]
    runtime_s: float
    status_name: str
    conflicts: int
    branches: int
    wall_time_s: float


def solve_nqueens_csp(n: int, time_limit_s: Optional[float] = None) -> CSPResult:
    t0 = time.perf_counter()

    model = cp_model.CpModel()

    Q = [model.NewIntVar(0, n - 1, f"Q_{r}") for r in range(n)]

    model.AddAllDifferent(Q)

    diag1 = [model.NewIntVar(-(n - 1), n - 1, f"d1_{r}") for r in range(n)]
    diag2 = [model.NewIntVar(0, 2 * n - 2, f"d2_{r}") for r in range(n)]

    for r in range(n):
        model.Add(diag1[r] == Q[r] - r)
        model.Add(diag2[r] == Q[r] + r)

    model.AddAllDifferent(diag1)
    model.AddAllDifferent(diag2)

    solver = cp_model.CpSolver()
    if time_limit_s is not None:
        solver.parameters.max_time_in_seconds = float(time_limit_s)

    status = solver.Solve(model)
    runtime = time.perf_counter() - t0

    status_name = solver.StatusName(status)

    placement: Optional[Tuple[int, ...]] = None
    found = status in (cp_model.OPTIMAL, cp_model.FEASIBLE)
    if found:
        placement = tuple(int(solver.Value(Q[r])) for r in range(n))

    return CSPResult(
        found=found,
        placement=placement,
        runtime_s=runtime,
        status_name=status_name,
        conflicts=int(solver.NumConflicts()),
        branches=int(solver.NumBranches()),
        wall_time_s=float(solver.WallTime()),
    )
