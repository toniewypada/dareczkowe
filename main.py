class Process:
    def __init__(self, pid, arrival_time, burst_time, current_time=0):
        # Inicjalizacja procesu z podstawowymi parametrami
        self.pid = pid                    # Identyfikator procesu
        self.arrival_time = arrival_time  # Czas przybycia procesu
        self.burst_time = burst_time      # Czas wykonania procesu
        self.completion_time = 0          # Czas zakończenia procesu
        self.waiting_time = 0             # Czas oczekiwania
        self.turnaround_time = 0          # Całkowity czas przetwarzania
        self.status = "new"               # Stan początkowy: nowy
        self.remaining_time = burst_time  # Pozostały czas wykonania
        # Słownik przechowujący czas spędzony w każdym stanie
        self.time_in_states = {
            "new": 0,        # Czas w stanie nowym
            "pending": 0,    # Czas oczekiwania na rdzeń
            "ready": 0,      # Czas gotowości do wykonania
            "processing": 0, # Czas przetwarzania
            "done": 0        # Czas po zakończeniu
        }
        self.last_state_change = current_time  # Czas ostatniej zmiany stanu
        self.creation_time = current_time      # Czas utworzenia procesu

    def update_state_time(self, current_time):
        # Aktualizacja czasu spędzonego w aktualnym stanie
        time_spent = current_time - self.last_state_change
        self.time_in_states[self.status] += time_spent
        self.last_state_change = current_time

    def change_status(self, new_status, current_time):
        # Zmiana stanu procesu z aktualizacją czasów
        self.update_state_time(current_time)
        self.status = new_status

def sjf_scheduling(processes, core_capacity=2):
    # Implementacja algorytmu szeregowania Shortest Job First
    # core_capacity określa ile procesów może być jednocześnie w stanie pending
    
    # Sortowanie procesów według czasu przybycia
    processes.sort(key=lambda x: x.arrival_time)
    
    n = len(processes)
    current_time = 0
    completed = 0
    ready_queue = []    # Kolejka procesów gotowych do wykonania
    result = []         # Lista zakończonych procesów
    
    # Śledzenie procesów w różnych stanach
    new_processes = processes.copy()      # Procesy nowe
    pending_processes = []                # Procesy oczekujące na rdzeń
    
    while completed != n:
        # Przenoszenie procesów ze stanu 'new' do 'pending' zgodnie z pojemnością rdzenia
        for process in new_processes[:]:
            if len(pending_processes) < core_capacity:
                process.change_status("pending", current_time)
                pending_processes.append(process)
                new_processes.remove(process)
        
        # Przenoszenie procesów ze stanu 'pending' do 'ready' gdy nadejdzie ich czas
        for process in pending_processes[:]:
            if process.arrival_time <= current_time:
                process.time_in_states["pending"] = current_time - process.last_state_change
                process.change_status("ready", current_time)
                ready_queue.append(process)
                pending_processes.remove(process)
            else:
                process.update_state_time(current_time)
        
        # Aktualizacja czasu dla procesów wciąż w stanie 'new'
        for process in new_processes:
            process.update_state_time(current_time)
        
        # Aktualizacja czasu oczekiwania dla procesów w kolejce ready
        for process in ready_queue:
            process.update_state_time(current_time)
        
        # Sortowanie kolejki ready według czasu wykonania (SJF)
        ready_queue.sort(key=lambda x: x.burst_time)
        
        if len(ready_queue) == 0:
            current_time += 1
            continue
            
        # Wybór i wykonanie procesu o najkrótszym czasie
        current_process = ready_queue.pop(0)
        current_process.change_status("processing", current_time)
        
        # Obliczanie czasów dla procesu
        current_time += current_process.burst_time
        current_process.completion_time = current_time
        current_process.turnaround_time = current_process.completion_time - current_process.arrival_time
        current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
        
        # Oznaczenie procesu jako zakończony
        current_process.change_status("done", current_time)
        
        result.append(current_process)
        completed += 1
        
        # Wyświetlenie informacji o zakończeniu procesu
        print(f"\nCzas {current_time}: Proces {current_process.pid} zakończony")
        print_current_status(processes)
    
    return result

def print_current_status(processes):
    # Wyświetlanie aktualnego stanu wszystkich procesów
    print("\nCurrent Process Status:")
    print("PID\tStatus\t\tTime in Current State")
    print("-" * 45)
    for process in processes:
        print(f"{process.pid}\t{process.status}\t\t{process.time_in_states[process.status]}")

def print_results(processes):
    # Wyświetlanie końcowych wyników szeregowania
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
    
    # Obliczanie i wyświetlanie średnich czasów
    avg_waiting_time = total_waiting_time / len(processes)
    avg_turnaround_time = total_turnaround_time / len(processes)
    
    print(f"\nAverage Waiting Time: {avg_waiting_time:.2f}")
    print(f"Average Turnaround Time: {avg_turnaround_time:.2f}")
    
    # Wyświetlanie czasu spędzonego w każdym stanie
    print("\nTime Spent in Each State:")
    print("PID\tNew\tPending\tReady\tProcessing\tDone")
    print("-" * 60)
    for process in processes:
        print(f"{process.pid}\t{process.time_in_states['new']}\t"
              f"{process.time_in_states['pending']}\t\t"
              f"{process.time_in_states['ready']}\t"
              f"{process.time_in_states['processing']}\t\t"
              f"{process.time_in_states['done']}")

def main():
    current_time = 0
    
    # Przykładowe procesy: (pid, czas_przybycia, czas_wykonania)
    # Proces 1: przybywa w czasie 0, wymaga 6 jednostek czasu na wykonanie
    # Proces 2: przybywa w czasie 2, wymaga 4 jednostek czasu na wykonanie
    # Proces 3: przybywa w czasie 4, wymaga 2 jednostek czasu na wykonanie
    # Proces 4: przybywa w czasie 6, wymaga 3 jednostek czasu na wykonanie
    process_data = [
        (1, 0, 6),
        (2, 2, 4),
        (3, 4, 2),
        (4, 6, 3)
    ]
    
    # Tworzenie obiektów procesów
    processes = [Process(pid, arrival, burst, current_time) for pid, arrival, burst in process_data]
    
    print("Initial Process Status:")
    print_current_status(processes)
    
    # Uruchomienie szeregowania SJF z pojemnością rdzenia = 2
    scheduled_processes = sjf_scheduling(processes, core_capacity=2)
    
    # Wyświetlenie końcowych wyników
    print_results(scheduled_processes)

if __name__ == "__main__":
    main()
