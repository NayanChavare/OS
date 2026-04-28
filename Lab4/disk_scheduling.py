"""
=============================================================================
Lab Assignment - 4
Course: Fundamentals of Operating System Lab (ENCA252)
Program: BCA (AI & DS) (Research)
Topic: Implementation and Analysis of Disk Scheduling Algorithms
       - FCFS, SSTF, SCAN, C-SCAN
=============================================================================
"""


# ─────────────────────────────────────────────────────────────────────────────
# TASK 1 — Input and Disk Request Representation
# ─────────────────────────────────────────────────────────────────────────────

def get_input():
    """
    Task 1: Accept disk request queue, initial head position, and disk size.
    Returns:
        requests  (list[int]): Disk I/O request queue.
        head      (int)      : Initial head position.
        disk_size (int)      : Total number of cylinders on the disk.
    """
    print("\n" + "=" * 60)
    print("        DISK SCHEDULING ALGORITHM SIMULATOR")
    print("=" * 60)

    while True:
        try:
            raw = input("\nEnter disk request queue (space-separated): ")
            requests = list(map(int, raw.strip().split()))
            if not requests:
                print("  [!] Request queue cannot be empty.")
                continue
            break
        except ValueError:
            print("  [!] Invalid input. Please enter integers only.")

    while True:
        try:
            head = int(input("Enter initial head position: "))
            if head < 0:
                print("  [!] Head position must be non-negative.")
                continue
            break
        except ValueError:
            print("  [!] Invalid input. Please enter an integer.")

    while True:
        try:
            disk_size = int(input("Enter disk size (total cylinders, e.g. 200): "))
            if disk_size <= 0:
                print("  [!] Disk size must be positive.")
                continue
            break
        except ValueError:
            print("  [!] Invalid input. Please enter an integer.")

    print(f"\n  Request Queue   : {requests}")
    print(f"  Initial Head    : {head}")
    print(f"  Disk Size       : {disk_size} cylinders (0 to {disk_size - 1})")
    return requests, head, disk_size


# ─────────────────────────────────────────────────────────────────────────────
# Utility — Pretty print seek sequence
# ─────────────────────────────────────────────────────────────────────────────

def print_result(algo_name, seek_sequence, seek_time):
    """
    Display the seek order and total seek time in a formatted table.
    """
    print(f"\n{'─' * 60}")
    print(f"  {algo_name}")
    print(f"{'─' * 60}")
    print(f"  Seek Sequence : {' → '.join(map(str, seek_sequence))}")
    print(f"  Total Seek Time (Head Movements) : {seek_time} cylinders")


# ─────────────────────────────────────────────────────────────────────────────
# TASK 2 — FCFS (First Come First Serve)
# ─────────────────────────────────────────────────────────────────────────────

def fcfs(requests, head):
    """
    Task 2: FCFS Disk Scheduling.
    - Services requests in the exact order they arrive.
    - Simple but can result in high total seek time.
    """
    seek_time    = 0
    current_head = head
    seek_sequence = [head]

    for req in requests:
        seek_time   += abs(current_head - req)
        current_head = req
        seek_sequence.append(req)

    print_result("FCFS (First Come First Serve)", seek_sequence, seek_time)
    return seek_time


# ─────────────────────────────────────────────────────────────────────────────
# TASK 3 — SSTF (Shortest Seek Time First)
# ─────────────────────────────────────────────────────────────────────────────

def sstf(requests, head):
    """
    Task 3: SSTF Disk Scheduling.
    - Always services the request closest to the current head position.
    - Reduces average seek time but may cause starvation of distant requests.
    """
    seek_time     = 0
    current_head  = head
    remaining     = requests.copy()
    seek_sequence = [head]

    while remaining:
        # Find the nearest request to the current head
        nearest = min(remaining, key=lambda x: abs(x - current_head))
        seek_time   += abs(current_head - nearest)
        current_head = nearest
        seek_sequence.append(nearest)
        remaining.remove(nearest)

    print_result("SSTF (Shortest Seek Time First)", seek_sequence, seek_time)
    return seek_time


# ─────────────────────────────────────────────────────────────────────────────
# TASK 4 — SCAN (Elevator Algorithm)
# ─────────────────────────────────────────────────────────────────────────────

def scan(requests, head, disk_size):
    """
    Task 4: SCAN (Elevator) Disk Scheduling.
    - Head moves in one direction (toward higher cylinders), services all
      requests along the way, reaches the end, then reverses direction.
    - Provides more uniform wait times than SSTF.

    Direction: head moves toward higher cylinder numbers first.
    """
    seek_time     = 0
    current_head  = head
    seek_sequence = [head]

    # Split requests into those to the right (≥ head) and left (< head)
    left  = sorted([r for r in requests if r < head], reverse=True)
    right = sorted([r for r in requests if r >= head])

    # Move RIGHT first — service all requests going up
    for r in right:
        seek_time   += abs(current_head - r)
        current_head = r
        seek_sequence.append(r)

    # Go to end of disk (if not already there)
    if current_head != disk_size - 1:
        seek_time   += abs(current_head - (disk_size - 1))
        current_head = disk_size - 1
        seek_sequence.append(current_head)

    # Reverse direction — service LEFT requests going down
    for r in left:
        seek_time   += abs(current_head - r)
        current_head = r
        seek_sequence.append(r)

    print_result("SCAN (Elevator Algorithm)", seek_sequence, seek_time)
    return seek_time


# ─────────────────────────────────────────────────────────────────────────────
# TASK 5 — C-SCAN (Circular SCAN)
# ─────────────────────────────────────────────────────────────────────────────

def cscan(requests, head, disk_size):
    """
    Task 5: C-SCAN (Circular SCAN) Disk Scheduling.
    - Head moves in ONE direction only (toward higher cylinders).
    - After reaching the end of the disk, it jumps back to cylinder 0
      without servicing requests on the return trip.
    - Provides more uniform wait time than regular SCAN.

    Direction: always moves toward higher cylinder numbers.
    """
    seek_time     = 0
    current_head  = head
    seek_sequence = [head]

    left  = sorted([r for r in requests if r < head])
    right = sorted([r for r in requests if r >= head])

    # Move RIGHT — service all requests going up
    for r in right:
        seek_time   += abs(current_head - r)
        current_head = r
        seek_sequence.append(r)

    # Jump to end of disk
    if current_head != disk_size - 1:
        seek_time   += abs(current_head - (disk_size - 1))
        current_head = disk_size - 1
        seek_sequence.append(current_head)

    # Jump back to cylinder 0 (no service on the return)
    seek_time   += current_head   # cost of jumping from end to 0
    current_head = 0
    seek_sequence.append(0)

    # Service LEFT requests from cylinder 0 upward
    for r in left:
        seek_time   += abs(current_head - r)
        current_head = r
        seek_sequence.append(r)

    print_result("C-SCAN (Circular SCAN)", seek_sequence, seek_time)
    return seek_time


# ─────────────────────────────────────────────────────────────────────────────
# TASK 6 & 7 — Performance Comparison and Result Analysis
# ─────────────────────────────────────────────────────────────────────────────

def compare_algorithms(results):
    """
    Task 6: Compare all disk scheduling algorithms.
    Task 7: Identify best/worst and provide analysis.
    """
    print("\n" + "=" * 60)
    print("         PERFORMANCE COMPARISON SUMMARY")
    print("=" * 60)
    print(f"  {'Algorithm':<32} {'Seek Time (cylinders)':>22}")
    print("  " + "-" * 55)

    sorted_results = sorted(results.items(), key=lambda x: x[1])
    max_time = sorted_results[-1][1] if sorted_results[-1][1] > 0 else 1
    for algo, time in sorted_results:
        bar = "█" * int((time / max_time) * 20)
        print(f"  {algo:<32} {time:>6}   {bar}")

    best_algo  = sorted_results[0]
    worst_algo = sorted_results[-1]

    print("\n" + "=" * 60)
    print("                 RESULT ANALYSIS")
    print("=" * 60)
    print(f"\n  ✔  Best  Algorithm : {best_algo[0]}  ({best_algo[1]} cylinders)")
    print(f"  ✘  Worst Algorithm : {worst_algo[0]}  ({worst_algo[1]} cylinders)")

    print("""
  Algorithm Insights:
  ─────────────────────────────────────────────────────────
  • FCFS   — Simplest; fair (no starvation) but highest
             seek time; no optimization at all.
  • SSTF   — Greedy; lowest average seek time in practice;
             risk of starvation for faraway requests.
  • SCAN   — Balanced; no starvation; slightly unfair to
             requests near the end that were just passed.
  • C-SCAN — Most uniform wait times; constant service
             direction; slightly higher seek than SCAN.
  ─────────────────────────────────────────────────────────
  Conclusion:
    SSTF minimizes seek time but risks starvation.
    SCAN and C-SCAN offer a practical trade-off between
    performance and fairness. FCFS is used only when
    simplicity is the primary concern.
  """)


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    requests, head, disk_size = get_input()

    results = {}
    results["FCFS"]   = fcfs(requests, head)
    results["SSTF"]   = sstf(requests, head)
    results["SCAN"]   = scan(requests, head, disk_size)
    results["C-SCAN"] = cscan(requests, head, disk_size)

    compare_algorithms(results)


if __name__ == "__main__":
    main()
