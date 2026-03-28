# Task 1: System Input and Data Representation [cite: 159]
def get_matrix_input(rows, cols, name):
    """Helper function to cleanly input a 2D matrix."""
    print(f"Enter {name} Matrix row by row (space-separated integers):")
    matrix = []
    for i in range(rows):
        while True:
            try:
                row = list(map(int, input(f"P{i}: ").split()))
                if len(row) != cols:
                    print(f"Please enter exactly {cols} values.")
                    continue
                matrix.append(row)
                break
            except ValueError:
                print("Invalid input. Please enter integers.")
    return matrix

def print_matrix(matrix, title):
    """Utility to print 2D matrices."""
    print(f"\n--- {title} ---")
    for i, row in enumerate(matrix):
        print(f"P{i}: {row}")

# Task 2: Need Matrix Calculation 
def calculate_need(allocation, maximum, num_p, num_r):
    """Computes the remaining resource requirements: Need = Maximum - Allocation[cite: 177]."""
    need = []
    for i in range(num_p):
        need_row = []
        for j in range(num_r):
            need_row.append(maximum[i][j] - allocation[i][j])
        need.append(need_row)
    return need

# Task 3 & 4: Banker's Safety Algorithm & Safe Sequence [cite: 184, 198]
def is_safe_state(processes, available, maximum, allocation, need, num_p, num_r):
    """Determines whether the system is in a safe state and generates a safe sequence[cite: 186, 202]."""
    
    # Initialize Work = Available [cite: 190]
    work = available.copy()
    
    # Initialize Finish array for all processes to False [cite: 191]
    finish = [False] * num_p
    
    safe_sequence = []
    
    # Repeat until all processes are completed or no allocation is possible [cite: 194]
    count = 0
    while count < num_p:
        found_process = False
        for i in range(num_p):
            if not finish[i]:
                # Find a process whose Need <= Work [cite: 192]
                # We check if ALL resources needed by P[i] are available in 'work'
                can_allocate = True
                for j in range(num_r):
                    if need[i][j] > work[j]:
                        can_allocate = False
                        break
                
                if can_allocate:
                    # Allocate resources and update Work: Work = Work + Allocation 
                    for j in range(num_r):
                        work[j] += allocation[i][j]
                        
                    safe_sequence.append(i)  # Store process in safe sequence [cite: 204]
                    finish[i] = True
                    found_process = True
                    count += 1
                    
        # If we loop through all processes and cannot find one to fulfill, it's unsafe
        if not found_process:
            print("\nSYSTEM IS IN AN UNSAFE STATE! Deadlock may occur.")
            return False
            
    # Task 5: Result Analysis (Safe Execution) [cite: 209]
    print("\nSYSTEM IS IN A SAFE STATE!")
    # Display the safe sequence [cite: 205]
    print("Safe Sequence: ", end="")
    print(" -> ".join([f"P{p}" for p in safe_sequence]))
    return True

if __name__ == "__main__":
    print("--- Banker's Algorithm Simulation ---")
    try:
        # 1. Define number of processes and resources [cite: 165]
        num_p = int(input("Enter total number of processes: "))
        num_r = int(input("Enter total number of resource types: "))
        
        # 2. Input Allocation Matrix [cite: 166]
        allocation = get_matrix_input(num_p, num_r, "Allocation")
        
        # 3. Input Maximum Matrix [cite: 167]
        maximum = get_matrix_input(num_p, num_r, "Maximum")
        
        # 4. Input Available Resources [cite: 168]
        while True:
            available = list(map(int, input(f"\nEnter Available Resources (space-separated, {num_r} values): ").split()))
            if len(available) == num_r:
                break
            print(f"Please enter exactly {num_r} values.")
            
        print_matrix(allocation, "Allocation Matrix")
        print_matrix(maximum, "Maximum Matrix")
        print(f"\nAvailable Resources: {available}")
        
        # Calculate and Display Need Matrix [cite: 179, 180]
        need_matrix = calculate_need(allocation, maximum, num_p, num_r)
        print_matrix(need_matrix, "Need Matrix")
        
        # Run Safety Algorithm
        is_safe_state(range(num_p), available, maximum, allocation, need_matrix, num_p, num_r)

    except ValueError:
         print("Invalid input. Please ensure you are entering numeric data.")