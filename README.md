# n-Queens: A* vs CSP

This project solves the **n-Queens problem** using two Artificial Intelligence approaches:

- A* state-space search with different heuristics
- Constraint Satisfaction Problem (CSP) formulation solved with OR-Tools CP-SAT

The goal is to compare the scalability and performance of search-based and constraint-based methods.

## Requirements

- Python >= 3.9 (tested with Python 3.11)

### Python dependencies
Install the required libraries with:
```bash
pip install ortools matplotlib
```

### How to Run
Single experiment
```bash
python main.py
```

Run benchmarks
```bash
python benchmark.py
```


This generates a results.csv file containing all performance metrics.

Generate plots
```bash
python plot_result.py
```
