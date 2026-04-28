"""
=============================================================================
Lab Assignment - 3
Course: Fundamentals of Operating System Lab (ENCA252)
Program: BCA (AI & DS) (Research)
Topic: Comprehensive Implementation of Page Replacement Algorithms
       - FIFO, LRU, Optimal, MRU, Second Chance (Clock Algorithm)
=============================================================================
"""

from collections import deque, OrderedDict


# ─────────────────────────────────────────────────────────────────────────────
# TASK 1 — Input and Page Reference String
# ─────────────────────────────────────────────────────────────────────────────

def get_input():
    """
    Task 1: Accept number of frames and page reference string from the user.
    Returns:
        frames (int): Number of memory frames available.
        pages  (list[int]): Page reference string.
    """
    print("\n" + "=" * 60)
    print("       PAGE REPLACEMENT ALGORITHM SIMULATOR")
    print("=" * 60)

    while True:
        try:
            frames = int(input("\nEnter number of frames: "))
            if frames <= 0:
                print("  [!] Frames must be a positive integer.")
                continue
            break
        except ValueError:
            print("  [!] Invalid input. Please enter an integer.")

    while True:
        try:
            raw = input("Enter page reference string (space-separated): ")
            pages = list(map(int, raw.strip().split()))
            if not pages:
                print("  [!] Page reference string cannot be empty.")
                continue
            break
        except ValueError:
            print("  [!] Invalid input. Please enter integers only.")

    print(f"\n  Frames          : {frames}")
    print(f"  Reference String: {pages}")
    return frames, pages


# ─────────────────────────────────────────────────────────────────────────────
# Utility — Pretty table printer
# ─────────────────────────────────────────────────────────────────────────────

def print_table(algo_name, pages, frame_states, fault_flags, fault_count):
    """
    Print a formatted step-by-step table showing frame contents at each step.
    """
    max_frames = max(len(fs) for fs in frame_states)

    print(f"\n{'─' * 60}")
    print(f"  {algo_name}")
    print(f"{'─' * 60}")

    # Header
    header = f"  {'Page':^6} | "
    for i in range(1, max_frames + 1):
        header += f"F{i:^4} "
    header += "| Fault"
    print(header)
    print("  " + "-" * (len(header) - 2))

    # Rows
    for i, page in enumerate(pages):
        frames_now = frame_states[i]
        fault = "✗ MISS" if fault_flags[i] else "  HIT "
        row = f"  {page:^6} | "
        for j in range(max_frames):
            val = frames_now[j] if j < len(frames_now) else " "
            row += f"{str(val):^5}"
        row += f"| {fault}"
        print(row)

    print("  " + "-" * (len(header) - 2))
    print(f"  Total Page Faults : {fault_count}")


# ─────────────────────────────────────────────────────────────────────────────
# TASK 2 — FIFO (First-In, First-Out)
# ─────────────────────────────────────────────────────────────────────────────

def fifo(pages, num_frames):
    """
    Task 2: FIFO Page Replacement.
    - Oldest page in memory is replaced first.
    - Implemented using a deque (queue) to track insertion order.
    """
    frame_set   = []          # Current pages in memory
    frame_queue = deque()     # Tracks insertion order
    fault_count = 0
    frame_states = []
    fault_flags  = []

    for page in pages:
        fault = False

        if page not in frame_set:
            fault = True
            fault_count += 1

            if len(frame_set) < num_frames:
                # Frames not full yet — just add
                frame_set.append(page)
                frame_queue.append(page)
            else:
                # Remove the oldest page
                oldest = frame_queue.popleft()
                frame_set.remove(oldest)
                frame_set.append(page)
                frame_queue.append(page)

        frame_states.append(frame_set.copy())
        fault_flags.append(fault)

    print_table("FIFO (First-In First-Out)", pages, frame_states,
                fault_flags, fault_count)
    return fault_count


# ─────────────────────────────────────────────────────────────────────────────
# TASK 3 — LRU (Least Recently Used)
# ─────────────────────────────────────────────────────────────────────────────

def lru(pages, num_frames):
    """
    Task 3: LRU Page Replacement.
    - Replaces the page that was least recently accessed.
    - Uses an OrderedDict to track access order efficiently.
    """
    memory      = OrderedDict()   # key = page, order = access recency
    fault_count = 0
    frame_states = []
    fault_flags  = []

    for page in pages:
        fault = False

        if page not in memory:
            fault = True
            fault_count += 1

            if len(memory) >= num_frames:
                # Evict the least recently used (first inserted in OrderedDict)
                memory.popitem(last=False)

            memory[page] = True
        else:
            # Move to end to mark as recently used
            memory.move_to_end(page)

        frame_states.append(list(memory.keys()))
        fault_flags.append(fault)

    print_table("LRU (Least Recently Used)", pages, frame_states,
                fault_flags, fault_count)
    return fault_count


# ─────────────────────────────────────────────────────────────────────────────
# TASK 4 — Optimal Page Replacement
# ─────────────────────────────────────────────────────────────────────────────

def optimal(pages, num_frames):
    """
    Task 4: Optimal Page Replacement.
    - Replaces the page whose next use is farthest in the future.
    - Serves as the theoretical benchmark (minimum possible page faults).
    """
    frame_set   = []
    fault_count = 0
    frame_states = []
    fault_flags  = []

    for idx, page in enumerate(pages):
        fault = False

        if page not in frame_set:
            fault = True
            fault_count += 1

            if len(frame_set) < num_frames:
                frame_set.append(page)
            else:
                # Find the page used farthest in the future
                future_use = {}
                for p in frame_set:
                    try:
                        future_use[p] = pages[idx + 1:].index(p)
                    except ValueError:
                        # Page never used again → best candidate for replacement
                        future_use[p] = float('inf')

                victim = max(future_use, key=future_use.get)
                frame_set[frame_set.index(victim)] = page

        frame_states.append(frame_set.copy())
        fault_flags.append(fault)

    print_table("Optimal Page Replacement", pages, frame_states,
                fault_flags, fault_count)
    return fault_count


# ─────────────────────────────────────────────────────────────────────────────
# TASK 5 — MRU (Most Recently Used)
# ─────────────────────────────────────────────────────────────────────────────

def mru(pages, num_frames):
    """
    Task 5: MRU Page Replacement.
    - Replaces the most recently used page.
    - Useful when recent access implies unlikely future reuse (e.g., sequential scan).
    """
    frame_set   = []
    recent_page = None        # Tracks the most recently used page
    fault_count = 0
    frame_states = []
    fault_flags  = []

    for page in pages:
        fault = False

        if page not in frame_set:
            fault = True
            fault_count += 1

            if len(frame_set) < num_frames:
                frame_set.append(page)
            else:
                # Replace the most recently used page
                if recent_page is not None and recent_page in frame_set:
                    frame_set[frame_set.index(recent_page)] = page
                else:
                    frame_set.pop()
                    frame_set.append(page)

        recent_page = page    # Update most recently used
        frame_states.append(frame_set.copy())
        fault_flags.append(fault)

    print_table("MRU (Most Recently Used)", pages, frame_states,
                fault_flags, fault_count)
    return fault_count


# ─────────────────────────────────────────────────────────────────────────────
# BONUS — Second Chance (Clock Algorithm)
# ─────────────────────────────────────────────────────────────────────────────

def second_chance(pages, num_frames):
    """
    Bonus: Second Chance (Clock) Page Replacement.
    - Extends FIFO by giving each page a 'second chance' via a reference bit.
    - If a page's reference bit is 1 when it's at the front, bit is cleared
      and the page is moved to the back (given a second chance).
    - If the bit is 0, the page is replaced immediately.
    """
    # Each entry: [page, reference_bit]
    frames      = []
    clock_hand  = 0           # Points to the oldest page
    fault_count = 0
    frame_states = []
    fault_flags  = []

    for page in pages:
        fault = False
        pages_in_mem = [f[0] for f in frames]

        if page not in pages_in_mem:
            fault = True
            fault_count += 1

            if len(frames) < num_frames:
                frames.append([page, 1])
            else:
                # Spin clock hand until a page with ref bit = 0 is found
                while True:
                    if frames[clock_hand][1] == 0:
                        frames[clock_hand] = [page, 1]
                        clock_hand = (clock_hand + 1) % num_frames
                        break
                    else:
                        frames[clock_hand][1] = 0   # Clear ref bit, give second chance
                        clock_hand = (clock_hand + 1) % num_frames
        else:
            # Page hit — set reference bit to 1
            for i, (p, _) in enumerate(frames):
                if p == page:
                    frames[i][1] = 1
                    break

        frame_states.append([f[0] for f in frames])
        fault_flags.append(fault)

    print_table("Second Chance (Clock Algorithm)", pages, frame_states,
                fault_flags, fault_count)
    return fault_count


# ─────────────────────────────────────────────────────────────────────────────
# TASK 6 & 7 — Performance Comparison and Result Analysis
# ─────────────────────────────────────────────────────────────────────────────

def compare_algorithms(results):
    """
    Task 6: Compare all algorithm results.
    Task 7: Identify best/worst and provide analysis.
    """
    print("\n" + "=" * 60)
    print("         PERFORMANCE COMPARISON SUMMARY")
    print("=" * 60)
    print(f"  {'Algorithm':<32} {'Page Faults':>12}")
    print("  " + "-" * 46)

    sorted_results = sorted(results.items(), key=lambda x: x[1])
    for algo, faults in sorted_results:
        bar   = "█" * faults
        print(f"  {algo:<32} {faults:>5}   {bar}")

    best_algo  = sorted_results[0]
    worst_algo = sorted_results[-1]

    print("\n" + "=" * 60)
    print("                 RESULT ANALYSIS")
    print("=" * 60)
    print(f"\n  ✔  Best  Algorithm : {best_algo[0]}  ({best_algo[1]} faults)")
    print(f"  ✘  Worst Algorithm : {worst_algo[0]}  ({worst_algo[1]} faults)")

    print("""
  Algorithm Insights:
  ─────────────────────────────────────────────────────────
  • FIFO       — Simple to implement; suffers from Belady's
                 Anomaly (more frames can cause more faults).
  • LRU        — Efficient in practice; exploits temporal
                 locality; higher implementation overhead.
  • Optimal    — Theoretical minimum faults; impractical
                 (requires knowledge of future references).
  • MRU        — Effective for cyclic/sequential access;
                 performs poorly under general workloads.
  • 2nd Chance — Approximates LRU with lower cost; provides
                 fairness via the reference bit mechanism.
  ─────────────────────────────────────────────────────────
  Conclusion:
    Optimal sets the lower bound. LRU and Second Chance
    achieve near-optimal results in real systems. FIFO is
    simple but unreliable. MRU suits niche access patterns.
  """)


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    num_frames, pages = get_input()

    results = {}
    results["FIFO"]          = fifo(pages, num_frames)
    results["LRU"]           = lru(pages, num_frames)
    results["Optimal"]       = optimal(pages, num_frames)
    results["MRU"]           = mru(pages, num_frames)
    results["Second Chance"] = second_chance(pages, num_frames)

    compare_algorithms(results)


if __name__ == "__main__":
    main()
