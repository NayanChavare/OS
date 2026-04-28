# Assignment 3 — Page Replacement Algorithms
**Course:** Fundamentals of Operating System Lab (ENCA252)  
**Program:** BCA (AI & DS) (Research)  
**Topic:** Comprehensive Implementation of Page Replacement Algorithms

---

## Problem Statement
In modern operating systems, virtual memory allows efficient utilization of physical memory. When memory frames are full, page replacement algorithms decide which page should be replaced. This assignment implements and analyzes all major page replacement algorithms and evaluates performance based on page faults.

---

## Algorithms Implemented

| Task | Algorithm | Strategy |
|------|-----------|----------|
| 2 | **FIFO** (First-In First-Out) | Replaces the oldest page in memory |
| 3 | **LRU** (Least Recently Used) | Replaces the page not used for the longest time |
| 4 | **Optimal** | Replaces the page whose next use is farthest in the future |
| 5 | **MRU** (Most Recently Used) | Replaces the most recently used page |
| Bonus | **Second Chance** (Clock Algorithm) | FIFO + reference bit for a second chance |

---

## File Structure

```
Assignment3/
└── page_replacement.py    # All 5 algorithms in a single file
```

---

## Requirements

- Python 3.x
- No external libraries (uses only built-in `collections` module)

---

## How to Run

```bash
python3 page_replacement.py
```

You will be prompted to enter:
1. Number of memory frames
2. Page reference string (space-separated integers)

---

## Sample Run

```
============================================================
       PAGE REPLACEMENT ALGORITHM SIMULATOR
============================================================

Enter number of frames: 3
Enter page reference string (space-separated): 7 0 1 2 0 3 0 4 2 3 0 3 2

  Frames          : 3
  Reference String: [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2]

────────────────────────────────────────────────────────────
  FIFO (First-In First-Out)
────────────────────────────────────────────────────────────
   Page  | F1    F2    F3   | Fault
  ------------------------------------------
    7    |  7              | ✗ MISS
    0    |  7    0         | ✗ MISS
    1    |  7    0    1    | ✗ MISS
    2    |  0    1    2    | ✗ MISS
    0    |  0    1    2    |   HIT
    3    |  1    2    3    | ✗ MISS
    ...
  Total Page Faults : 10

  [similarly for LRU, Optimal, MRU, Second Chance...]

============================================================
         PERFORMANCE COMPARISON SUMMARY
============================================================
  Algorithm                         Page Faults
  ----------------------------------------------
  Optimal                              7   ███████
  LRU                                  9   █████████
  Second Chance                        9   █████████
  FIFO                                10   ██████████
  MRU                                 11   ███████████

  ✔  Best  Algorithm : Optimal  (7 faults)
  ✘  Worst Algorithm : MRU      (11 faults)
```

---

## Algorithm Details

### FIFO (First-In First-Out)
- Maintains a queue of pages in memory.
- When a page fault occurs and frames are full, the **oldest** page (front of queue) is evicted.
- Simple to implement but suffers from **Belady's Anomaly** — increasing frames can sometimes increase page faults.

### LRU (Least Recently Used)
- Tracks the usage history of each page.
- Evicts the page that was **least recently accessed**.
- Exploits **temporal locality** — recently used pages are likely to be used again.
- Implemented using Python's `OrderedDict` for efficient ordering.

### Optimal Page Replacement
- Looks ahead in the reference string to find which page will **not be used for the longest time**.
- Produces the **minimum possible page faults** — serves as a theoretical benchmark.
- Not implementable in real systems (requires future knowledge).

### MRU (Most Recently Used)
- Evicts the **most recently used** page.
- Useful for sequential scan workloads where a recently accessed page is unlikely to be needed again soon.
- Generally performs worse than LRU on standard workloads.

### Second Chance (Clock Algorithm)
- An improvement over FIFO using a **reference bit**.
- When a page is about to be evicted, if its reference bit is `1`, it is given a second chance (bit cleared, moved to back of queue).
- If the reference bit is `0`, the page is evicted immediately.
- Approximates LRU with lower overhead.

---

## Key Concepts

| Term | Definition |
|------|-----------|
| **Page Fault** | Occurs when a requested page is not in memory and must be loaded |
| **Frame** | A fixed-size block of physical memory |
| **Page Reference String** | Sequence of page numbers accessed by a process |
| **Temporal Locality** | Tendency to reuse recently accessed pages |

---

## Result Analysis

- **Optimal** always yields the fewest page faults but is only a benchmark.
- **LRU** and **Second Chance** perform closest to Optimal in real-world scenarios.
- **FIFO** is simple but unreliable due to Belady's Anomaly.
- **MRU** is a niche algorithm suited to specific access patterns (e.g., cyclic scans).

---

*Submitted as part of ENCA252 Lab | School of Engineering and Technology*
