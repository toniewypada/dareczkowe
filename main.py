class Process:
    def __init__(self, pid, arrival_time, burst_time, current_time=0):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.completion_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0
        self.status = "new"
        self.remaining_time = burst_time
        self.time_in_states = {
            "new": 0,
            "pending": 0,
            "ready": 0,
            "processing": 0,
            "done": 0
        }
        self.last_state_change = current_time
        self.creation_time = current_time

    def update_state_time(self, current_time):
        # Update time spent in current state
        time_spent = current_time - self.last_state_change
        self.time_in_states[self.status] += time_spent
        self.last_state_change = current_time

    def change_status(self, new_status, current_time):
        self.update_state_time(current_time)
        self.status = new_status

def sjf_scheduling(processes, core_capacity=2):
    processes.sort(key=lambda x: x.arrival_time)
    
    n = len(processes)
    current_time = 0
    completed = 0
    ready_queue = []
    result = []
    
    # Track new and pending processes separately
    new_processes = processes.copy()
    pending_processes = []
    
    while completed != n:
        # Move processes from new to pending based on core capacity
        for process in new_processes[:]:
            if len(pending_processes) < core_capacity:
                process.change_status("pending", current_time)
                pending_processes.append(process)
                new_processes.remove(process)
        
        # Update pending time for processes not yet in ready queue
        for process in pending_processes[:]:
            if process.arrival_time <= current_time:
                process.time_in_states["pending"] = current_time - process.last_state_change
                process.change_status("ready", current_time)
                ready_queue.append(process)
                pending_processes.remove(process)
            else:
                process.update_state_time(current_time)
        
        # Update time for processes still in new state
        for process in new_processes:
            process.update_state_time(current_time)
        
        # Update waiting time for processes in ready queue
        for process in ready_queue:
            process.update_state_time(current_time)
        
        ready_queue.sort(key=lambda x: x.burst_time)
        
        if len(ready_queue) == 0:
            current_time += 1
            continue
            
        # Process the job with shortest burst time
        current_process = ready_queue.pop(0)
        current_process.change_status("processing", current_time)
        
        # Calculate times
        current_time += current_process.burst_time
        current_process.completion_time = current_time
        current_process.turnaround_time = current_process.completion_time - current_process.arrival_time
        current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
        
        # Update final state
        current_process.change_status("done", current_time)
        
        result.append(current_process)
        completed += 1
        
        # Print status update after each process completes
        print(f"\nTime {current_time}: Process {current_process.pid} completed")
        print_current_status(processes)
    
    return result

def print_current_status(processes):
    print("\nCurrent Process Status:")
    print("PID\tStatus\t\tTime in Current State")
    print("-" * 45)
    for process in processes:
        print(f"{process.pid}\t{process.status}\t\t{process.time_in_states[process.status]}")

def print_results(processes):
    print("\nFinal Process Scheduling Results:")
    print("PID\tArrival\tBurst\tCompletion\tTurnaround\tWaiting\tStatus")
    print("-" * 75)
    
    total_waiting_time = 0
    total_turnaround_time = 0
    
    for process in processes:
        print(f"{process.pid}\t{process.arrival_time}\t{process.burst_time}\t{process.completion_time}\t\t"
              f"{process.turnaround_time}\t\t{process.waiting_time}\t{process.status}")
        total_waiting_time += process.waiting_time
        total_turnaround_time += process.turnaround_time
    
    avg_waiting_time = total_waiting_time / len(processes)
    avg_turnaround_time = total_turnaround_time / len(processes)
    
    print(f"\nAverage Waiting Time: {avg_waiting_time:.2f}")
    print(f"Average Turnaround Time: {avg_turnaround_time:.2f}")
    
    # Print time spent in each state
    print("\nTime Spent in Each State:")
    print("PID\tNew\tPending\tReady\tProcessing\tDone")
    print("-" * 60)
    for process in processes:
        print(f"{process.pid}\t{process.time_in_states['new']}\t"
              f"{process.time_in_states['pending']}\t"
              f"{process.time_in_states['ready']}\t"
              f"{process.time_in_states['processing']}\t\t"
              f"{process.time_in_states['done']}")

def main():
    current_time = 0
    
    # Example processes: (pid, arrival_time, burst_time)
    process_data = [
        (1, 0, 6),
        (2, 2, 4),
        (3, 4, 2),
        (4, 6, 3)
    ]
    
    # Create processes with current time
    processes = [Process(pid, arrival, burst, current_time) for pid, arrival, burst in process_data]
    
    print("Initial Process Status:")
    print_current_status(processes)
    
    # Run SJF scheduling with core capacity of 2
    scheduled_processes = sjf_scheduling(processes, core_capacity=2)
    
    # Print final results
    print_results(scheduled_processes)

if __name__ == "__main__":
    main()
