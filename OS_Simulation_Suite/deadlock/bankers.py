import numpy as np
import time

def bankers_algorithm(available, max_matrix, allocation):
    """
    Simulates the Banker's Algorithm to find if the system is in a safe state.
    Returns: (is_safe, safe_sequence)
    """
    n = len(allocation) # num processes
    
    # Calculate Need matrix
    need = np.array(max_matrix) - np.array(allocation)
    work = np.array(available).copy()
    finish = [False] * n
    safe_sequence = []

    while True:
        found = False
        for i in range(n):
            if not finish[i] and all(need[i] <= work):
                # Process can finish
                work += np.array(allocation[i])
                finish[i] = True
                safe_sequence.append(f"P{i}")
                found = True
        if not found:
            break

    if all(finish):
        return True, safe_sequence
    else:
        return False, safe_sequence

def bankers_with_steps(available, max_matrix, allocation, callback):
    n = len(allocation) # num processes
    
    # Calculate Need matrix
    need = np.array(max_matrix) - np.array(allocation)
    work = np.array(available).copy()
    finish = [False] * n
    safe_sequence = []

    callback({"type": "init", "work": list(work), "need": need.tolist(), "alloc": allocation, "finish": finish})
    time.sleep(1)

    while True:
        found = False
        for i in range(n):
            if not finish[i] and all(need[i] <= work):
                callback({"type": "checking", "proc": i, "work": list(work), "finish": finish})
                time.sleep(1)
                
                work += np.array(allocation[i])
                finish[i] = True
                safe_sequence.append(f"P{i}")
                
                callback({"type": "finished_step", "proc": i, "work": list(work), "finish": finish})
                time.sleep(1)
                found = True

        if not found:
            break

    if all(finish):
        callback({"type": "success", "sequence": safe_sequence, "finish": finish})
    else:
        callback({"type": "deadlock", "finish": finish})
