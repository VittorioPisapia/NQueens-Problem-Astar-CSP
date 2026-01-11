from astar import astar_search
from nqueens_problem import is_goal, successors, state_key, pretty_board, State, h_mrv_next_row
from nqueens_csp import solve_nqueens_csp

def main():
    select = 0  #0 = Astar, 1 = Csp
    print_board = True
    n = 10
    
    if select == 0 :
        initial_state: State = ()

        def goal_fn(s):
            return is_goal(s, n)

        def succ_fn(s):
            return successors(s, n)

        def h1(s):
            return n - len(s)

        def h2(s):
            return h_mrv_next_row(s, n)

        for name, h in [("baseline_remaining", h1), ("mrv_next_row", h2)]:
            sol = astar_search(
                initial_state=initial_state,
                is_goal=goal_fn,
                successors=succ_fn,
                heuristic=h,
                state_key=state_key,
            )

            print("\n====", name, "====")
            print("found:", sol.found)
            print("g_cost:", sol.g_cost)
            print("runtime_s:", sol.runtime_s)
            print("expanded:", sol.expanded)
            print("generated:", sol.generated)
            print("peak_mem:", sol.peak_nodes_in_memory)
            print(
                "branching min/avg/max:",
                sol.branching_min,
                f"{sol.branching_avg:.2f}",
                sol.branching_max,
            )

            if sol.found:
                sol = sol.solution_state
                print("\nSolution placement:", sol)
                if print_board:
                    print(pretty_board(sol, n))

    elif select == 1:
        sol_csp = solve_nqueens_csp(n, time_limit_s=None)
        print("\n==== csp_ortools ====")
        print("found:", sol_csp.found)
        print("status:", sol_csp.status_name)
        print("runtime_s:", sol_csp.runtime_s)
        print("conflicts:", sol_csp.conflicts)
        print("branches:", sol_csp.branches)

        if sol_csp.found:
            sol = sol_csp.placement
            if print_board:
                    print(pretty_board(sol, n))

    

if __name__ == "__main__":
    main()

