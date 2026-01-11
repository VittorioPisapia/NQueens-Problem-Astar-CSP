import csv
from collections import defaultdict
import matplotlib.pyplot as plt # type: ignore


def read_results(path="results.csv"):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            r["n"] = int(r["n"])
            r["found"] = (r["found"] == "True")
            r["valid"] = (r["valid"] == "True")
            r["runtime_s"] = float(r["runtime_s"]) if r["runtime_s"] != "" else None
            r["expanded"] = int(r["expanded"]) if r["expanded"] != "" else None
            rows.append(r)
    return rows


def plot_runtime(rows, out_path="runtime_vs_n.png"):
    series = defaultdict(list)
    for r in rows:
        key = (r["method"], r["heuristic"])
        if r["runtime_s"] is not None:
            series[key].append((r["n"], r["runtime_s"]))

    plt.figure()
    for (method, heur), pts in sorted(series.items()):
        pts.sort()
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        label = f"{method}" + (f" ({heur})" if heur else "")
        plt.plot(xs, ys, marker="o", label=label)

    plt.yscale("log") 
    plt.xlabel("n")
    plt.ylabel("runtime (s, log scale)")
    plt.title("n-Queens: runtime vs n")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    print(f"Saved {out_path}")


def plot_expanded(rows, out_path="expanded_vs_n.png"):
    series = defaultdict(list)
    for r in rows:
        if r["method"] != "astar":
            continue
        key = r["heuristic"]
        if r["expanded"] is not None:
            series[key].append((r["n"], r["expanded"]))

    plt.figure()
    for heur, pts in sorted(series.items()):
        pts.sort()
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        plt.plot(xs, ys, marker="o", label=heur)

    plt.yscale("log")
    plt.xlabel("n")
    plt.ylabel("expanded nodes (log scale)")
    plt.title("A*: expanded nodes vs n")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    print(f"Saved {out_path}")


def main():
    rows = read_results("results.csv")
    plot_runtime(rows, "runtime_vs_n.png")
    plot_expanded(rows, "expanded_vs_n.png")


if __name__ == "__main__":
    main()
