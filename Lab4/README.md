# Assignment 4 — Disk Scheduling Algorithms
**Course:** Fundamentals of Operating System Lab (ENCA252)  
**Program:** BCA (AI & DS) (Research)  
**Topic:** Implementation and Analysis of Disk Scheduling Algorithms

---

## Problem Statement
Disk scheduling is an essential function of operating systems that determines the order in which disk I/O requests are serviced. Efficient disk scheduling improves system performance by reducing seek time and increasing throughput. This assignment implements and analyzes FCFS, SSTF, SCAN, and C-SCAN algorithms by simulating head movements and calculating total seek time.

---

## Algorithms Implemented

| Task | Algorithm | Strategy |
|------|-----------|----------|
| 2 | **FCFS** (First Come First Serve) | Services requests in the order they arrive |
| 3 | **SSTF** (Shortest Seek Time First) | Services the request closest to the current head |
| 4 | **SCAN** (Elevator Algorithm) | Head sweeps in one direction, then reverses |
| 5 | **C-SCAN** (Circular SCAN) | Head sweeps in one direction only, jumps back to 0 |

---

## File Structure

```
Assignment4/
└── disk_scheduling.py    # All 4 algorithms in a single file
```

---

## Requirements

- Python 3.x
- No external libraries required

---

## How to Run

```bash
python3 disk_scheduling.py
```

You will be prompted to enter:
1. Disk request queue (space-separated cylinder numbers)
2. Initial head position
3. Total disk size (number of cylinders)

---

## Sample Run

```
============================================================
        DISK SCHEDULING ALGORITHM SIMULATOR
============================================================

Enter disk request queue (space-separated): 98 183 37 122 14 124 65 67
Enter initial head position: 53
Enter disk size (total cylinders, e.g. 200): 200

  Request Queue   : [98, 183, 37, 122, 14, 124, 65, 67]
  Initial Head    : 53
  Disk Size       : 200 cylinders (0 to 199)

────────────────────────────────────────────────────────────
  FCFS (First Come First Serve)
────────────────────────────────────────────────────────────
  Seek Sequence : 53 → 98 → 183 → 37 → 122 → 14 → 124 → 65 → 67
  Total Seek Time (Head Movements) : 640 cylinders

────────────────────────────────────────────────────────────
  SSTF (Shortest Seek Time First)
────────────────────────────────────────────────────────────
  Seek Sequence : 53 → 65 → 67 → 37 → 14 → 98 → 122 → 124 → 183
  Total Seek Time (Head Movements) : 236 cylinders

────────────────────────────────────────────────────────────
  SCAN (Elevator Algorithm)
────────────────────────────────────────────────────────────
  Seek Sequence : 53 → 65 → 67 → 98 → 122 → 124 → 183 → 199 → 37 → 14
  Total Seek Time (Head Movements) : 331 cylinders

────────────────────────────────────────────────────────────
  C-SCAN (Circular SCAN)
────────────────────────────────────────────────────────────
  Seek Sequence : 53 → 65 → 67 → 98 → 122 → 124 → 183 → 199 → 0 → 14 → 37
  Total Seek Time (Head Movements) : 382 cylinders

============================================================
         PERFORMANCE COMPARISON SUMMARY
============================================================
  Algorithm                         Seek Time (cylinders)
  -------------------------------------------------------
  SSTF                                236   ███████
  SCAN                                331   ██████████
  C-SCAN                              382   ███████████
  FCFS                                640   ████████████████████

  ✔  Best  Algorithm : SSTF  (236 cylinders)
  ✘  Worst Algorithm : FCFS  (640 cylinders)
```

---

## Algorithm Details

### FCFS (First Come First Serve)
- Requests are serviced in the **exact order** they arrive in the queue.
- Simplest algorithm with no optimization.
- Can result in high total seek time when requests are scattered across the disk.
- **No starvation** — every request is eventually serviced.

### SSTF (Shortest Seek Time First)
- At each step, services the request **nearest to the current head position**.
- Greedy approach — significantly reduces average seek time compared to FCFS.
- **Risk of starvation** — requests far from the head may wait indefinitely if closer requests keep arriving.

### SCAN (Elevator Algorithm)
- The disk head moves in **one direction** (toward higher cylinders), servicing all requests along the way.
- When it reaches the **end of the disk**, it reverses direction and services requests on the way back.
- Behaves like an elevator — balanced performance with no starvation.
- Slightly unfair to requests just behind the head when it reverses.

### C-SCAN (Circular SCAN)
- The disk head moves in **one direction only** (toward higher cylinders).
- After reaching the end of the disk, it **jumps back to cylinder 0** without servicing requests on the return.
- Provides **more uniform wait times** than SCAN.
- Slightly higher total seek time than SCAN due to the wrap-around cost.

---

## Key Concepts

| Term | Definition |
|------|-----------|
| **Seek Time** | Time taken for the disk head to move to the required cylinder |
| **Cylinder** | A set of tracks at the same position on all disk platters |
| **Head Position** | Current location of the read/write head on the disk |
| **Throughput** | Number of I/O requests completed per unit time |
| **Starvation** | A request that is indefinitely delayed because other requests keep getting priority |

---

## Result Analysis

- **SSTF** achieves the lowest seek time but risks starvation of distant requests.
- **SCAN** offers a balanced trade-off — good performance with fairness.
- **C-SCAN** provides the most uniform response times, ideal for heavily loaded systems.
- **FCFS** is used only when simplicity and fairness (no starvation) are the only concerns.

### When to Use Which Algorithm

| Scenario | Recommended Algorithm |
|----------|----------------------|
| Low load, simple system | FCFS |
| Minimize seek time, low load | SSTF |
| Balanced performance & fairness | SCAN |
| High load, uniform response needed | C-SCAN |

---

*Submitted as part of ENCA252 Lab | School of Engineering and Technology*
