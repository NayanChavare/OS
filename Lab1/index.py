# Task 1: Process Creation & Input Handling
class Process:
    def __init__(self, pid, at, bt):
        self.pid = pid      # Process ID [cite: 40]
        self.at = at        # Arrival Time [cite: 42]
        self.bt = bt        # Burst Time [cite: 44]
        self.ct = 0         # Completion Time
        self.tat = 0        # Turnaround Time
        self.wt = 0         # Waiting Time
        self.is_completed = False 

def display_table(processes, title="Process Table"):
    """Displays process details in a tabular format[cite: 47]."""
    print(f"\n--- {title} ---")
    print(f"{'PID':<5} | {'AT':<5} | {'BT':<5} | {'CT':<5} | {'TAT':<5} | {'WT':<5}")
    print("-" * 45)
    for p in processes:
        print(f"{p.pid:<5} | {p.at:<5} | {p.bt:<5} | {p.ct:<5} | {p.tat:<5} | {p.wt:<5}")

def print_gantt_chart(execution_order, title="Gantt Chart"):
    """Visualizes the process execution sequence[cite: 90]."""
    print(f"\n--- {title} ---")
    chart = "|"
    timeline = "0"
    
    for pid, start, end in execution_order:
        # Handle CPU idle time
        if int(timeline.split()[-1]) < start:
            chart += f" IDLE |"
            timeline += f"      {start}"
            
        chart += f"  P{pid}  |"
        # Formatting to keep the timeline aligned
        timeline += f"{str(end):>7}" 
        
    print(chart)
    print(timeline)

def calculate_averages(processes):
    """Calculates Average Waiting Time and Average Turnaround Time."""
    total_tat = sum(p.tat for p in processes)
    total_wt = sum(p.wt for p in processes)
    n = len(processes)
    return total_wt / n, total_tat / n

# Task 2: FCFS Scheduling Implementation
def fcfs_scheduling(processes):
    """Implements First Come First Serve scheduling."""
    # Sort processes by Arrival Time [cite: 57]
    fcfs_processes = sorted(processes, key=lambda x: x.at)
    current_time = 0
    execution_order = []

    for p in fcfs_processes:
        # Handle CPU idle condition if no process has arrived [cite: 64]
        if current_time < p.at:
            current_time = p.at
            
        start_time = current_time
        p.ct = current_time + p.bt            # Completion Time (CT) [cite: 61]
        p.tat = p.ct - p.at                   # Turnaround Time (TAT) = CT - AT [cite: 62]
        p.wt = p.tat - p.bt                   # Waiting Time (WT) = TAT - BT [cite: 63]
        
        current_time = p.ct
        execution_order.append((p.pid, start_time, p.ct))

    display_table(fcfs_processes, "FCFS Scheduling Results")
    print_gantt_chart(execution_order, "FCFS Gantt Chart")
    avg_wt, avg_tat = calculate_averages(fcfs_processes)
    print(f"FCFS Average Waiting Time: {avg_wt:.2f}")
    print(f"FCFS Average Turnaround Time: {avg_tat:.2f}\n")

# Task 3: SJF Scheduling (Non-Preemptive)
def sjf_scheduling(processes):
    """Implements Non-Preemptive Shortest Job First scheduling."""
    # Create a fresh copy to avoid modifying FCFS results
    sjf_processes = [Process(p.pid, p.at, p.bt) for p in processes]
    completed = 0
    n = len(sjf_processes)
    current_time = 0
    execution_order = []

    while completed != n:
        # Ensure only arrived processes are considered [cite: 77]
        available_processes = [p for p in sjf_processes if p.at <= current_time and not p.is_completed]

        if not available_processes:
            # CPU is idle; move time forward
            current_time += 1
            continue

        # Pick the process with the shortest burst time [cite: 76]
        # In case of a tie, standard SJF falls back to AT
        shortest_process = min(available_processes, key=lambda x: (x.bt, x.at))
        
        start_time = current_time
        shortest_process.ct = current_time + shortest_process.bt
        shortest_process.tat = shortest_process.ct - shortest_process.at
        shortest_process.wt = shortest_process.tat - shortest_process.bt
        shortest_process.is_completed = True
        
        current_time = shortest_process.ct
        execution_order.append((shortest_process.pid, start_time, shortest_process.ct))
        completed += 1

    # Sort back by PID for standard table display
    sjf_processes.sort(key=lambda x: x.pid)
    display_table(sjf_processes, "SJF (Non-Preemptive) Scheduling Results")
    print_gantt_chart(execution_order, "SJF Gantt Chart")
    avg_wt, avg_tat = calculate_averages(sjf_processes)
    print(f"SJF Average Waiting Time: {avg_wt:.2f}")
    print(f"SJF Average Turnaround Time: {avg_tat:.2f}\n")

if __name__ == "__main__":
    print("--- CPU Scheduling Simulation ---")
    try:
        n = int(input("Enter the number of processes (4-5 recommended): "))
        processes = []
        for i in range(n):
            print(f"\nEnter details for Process P{i+1}:")
            at = int(input("Arrival Time (AT): "))
            bt = int(input("Burst Time (BT): "))
            processes.append(Process(i+1, at, bt))
            
        print("\n=== EXECUTING FCFS ===")
        fcfs_scheduling(processes)
        
        print("=== EXECUTING SJF ===")
        sjf_scheduling(processes)
        
    except ValueError:
        print("Invalid input. Please enter integer values.")