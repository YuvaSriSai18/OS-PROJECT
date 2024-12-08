import time
import random
import heapq

# Core Configuration
CPU_CORES = {"4GHz": 2, "3GHz": 4, "2GHz": 4}


# Job class to hold job details
class Job:
    def __init__(self, name, burst_time, priority, core_requirement, arrival_time):
        self.name = name
        self.burst_time = burst_time  # Remaining burst time in minutes
        self.priority = priority
        self.core_requirement = core_requirement
        self.arrival_time = arrival_time  # Arrival time in seconds

    def __lt__(self, other):
        # Priority comparison for the queue
        if self.priority == other.priority:
            return self.burst_time < other.burst_time  # SJF if priorities are equal
        return self.priority < other.priority


# Scheduler class
class Scheduler:
    def __init__(self):
        self.start_time = time.time()  # Program start time
        self.jobs = []  # List of all jobs
        self.running_jobs = []  # Currently running jobs (core, job)
        self.queue = []  # Priority queue for waiting jobs
        self.completed_jobs = []  # Completed jobs
        self.available_cores = CPU_CORES.copy()
        self.clock_running = True  # Flag to control clock simulation

    def generate_job(self, name):
        """
        Dynamically generate a single job.
        """
        burst_time = random.randint(50, 300)  # Job burst time (minutes)
        priority = random.randint(1, 19)  # Priority from 1 (highest) to 19 (lowest)
        core_requirement = random.choice(["2GHz", "3GHz", "4GHz"])  # Core requirement
        arrival_time = int(time.time() - self.start_time)  # Dynamic arrival time
        return Job(name, burst_time, priority, core_requirement, arrival_time)

    def assign_job_to_core(self, job):
        """
        Attempt to assign a job to its desired core or a fallback core.
        """
        # Check if there's a lower-priority job on the same core to preempt
        core_to_replace = None
        lowest_priority_job = None

        for core, running_job in self.running_jobs:
            if core == job.core_requirement:
                if not lowest_priority_job or running_job.priority > lowest_priority_job.priority:
                    core_to_replace = core
                    lowest_priority_job = running_job

        # Preempt the lowest-priority job
        if lowest_priority_job and job.priority < lowest_priority_job.priority:
            print(
                f"Preempting {lowest_priority_job.name} (Priority: {lowest_priority_job.priority}) "
                f"for {job.name} (Priority: {job.priority})"
            )
            self.running_jobs.remove((core_to_replace, lowest_priority_job))
            self.available_cores[core_to_replace] += 1
            heapq.heappush(self.queue, lowest_priority_job)  # Save state and requeue
            self.available_cores[core_to_replace] -= 1
            self.running_jobs.append((core_to_replace, job))
            return True

        # Check for any completely free core
        if self.available_cores[job.core_requirement] > 0:
            self.available_cores[job.core_requirement] -= 1
            self.running_jobs.append((job.core_requirement, job))
            print(f"Assigned {job.name} to {job.core_requirement} (Priority: {job.priority})")
            return True

        # Attempt fallback to lower-priority cores
        for fallback_core in ["3GHz", "2GHz"]:
            if self.available_cores[fallback_core] > 0:
                self.available_cores[fallback_core] -= 1
                self.running_jobs.append((fallback_core, job))
                print(f"Fallback: Assigned {job.name} to {fallback_core} (Priority: {job.priority})")
                return True

        return False  # No cores available or preemption possible

    def handle_queue(self):
        """
        Check the queue and assign jobs to any available cores, maintaining priority order.
        """
        new_queue = []
        while self.queue:
            job = heapq.heappop(self.queue)

            # Attempt to assign the job to a core, considering preemption
            if not self.assign_job_to_core(job):
                new_queue.append(job)  # Retain in the queue if no assignment possible

        self.queue = new_queue

    def fallback_or_queue(self, job):
        """
        Handle fallback or queueing when a job cannot be directly assigned.
        """
        # Identify the lowest-priority running job for potential preemption
        lowest_priority_job = None
        core_to_replace = None

        for core, running_job in self.running_jobs:
            if not lowest_priority_job or running_job.priority > lowest_priority_job.priority:
                lowest_priority_job = running_job
                core_to_replace = core

        # Preempt if the new job has a higher priority than the lowest-priority running job
        if lowest_priority_job and job.priority < lowest_priority_job.priority:
            print(
                f"Preempting {lowest_priority_job.name} (Priority: {lowest_priority_job.priority}) "
                f"for {job.name} (Priority: {job.priority})"
            )
            self.running_jobs.remove((core_to_replace, lowest_priority_job))
            self.available_cores[core_to_replace] += 1
            heapq.heappush(self.queue, lowest_priority_job)  # Requeue the preempted job
            self.available_cores[core_to_replace] -= 1
            self.running_jobs.append((core_to_replace, job))
            return

        # If no preemption possible, queue the new job
        print(f"Queueing {job.name} (Priority: {job.priority}, Core Req: {job.core_requirement})")
        heapq.heappush(self.queue, job)

    def update_burst_times(self):
        """
        Update burst times of running jobs based on core frequency.
        """
        completed_jobs = []
        for i, (core, job) in enumerate(self.running_jobs):
            decrement = int(core[0])  # Extract GHz as integer
            job.burst_time -= decrement
            if job.burst_time <= 0:
                completed_jobs.append((core, job))

        for core, job in completed_jobs:
            self.terminate_job(job.name)

    def terminate_job(self, job_name):
        """
        Terminate a specific job and free its core.
        """
        for i, (core, job) in enumerate(self.running_jobs):
            if job.name == job_name:
                self.running_jobs.pop(i)
                self.available_cores[core] += 1
                self.completed_jobs.append(job)
                print(f"Completed {job_name} on {core}")
                return True
        return False

    def show_status(self):
        """
        Display the current scheduler status.
        """
        elapsed_time = int(time.time() - self.start_time)
        print("\n=== CPU Scheduler Status ===")
        print(f"Clock: {elapsed_time} seconds")
        print("\nRunning Jobs:")
        for core, job in sorted(self.running_jobs, key=lambda x: x[1].priority):
            print(f"- {job.name} on {core} (Priority: {job.priority}, Remaining Time: {job.burst_time} mins)")
        print("\nQueued Jobs:")
        for job in sorted(self.queue):
            print(f"- {job.name} (Priority: {job.priority}, Core Req: {job.core_requirement})")
        print("\nAvailable Cores:")
        for core_type, count in self.available_cores.items():
            print(f"- {core_type}: {count} available")
        print("===========================\n")

    def start_clock(self):
        """
        Continuously update burst times and handle job completion.
        """
        while self.clock_running:
            time.sleep(1)  # 1 real second = 1 simulated minute
            self.update_burst_times()
            self.handle_queue()

    def start(self):
        """
        Main loop for the scheduler.
        """
        from threading import Thread

        clock_thread = Thread(target=self.start_clock, daemon=True)
        clock_thread.start()

        while True:
            self.show_status()
            print("1. Start an app")
            print("2. Exit Scheduler")
            choice = input("Enter your choice: ")

            if choice == "1":
                app_name = input("Enter app name: ")
                new_job = self.generate_job(app_name)
                self.jobs.append(new_job)
                self.fallback_or_queue(new_job)

            elif choice == "2":
                self.clock_running = False
                print("Exiting Scheduler...")
                break

            else:
                print("Invalid option! Please try again.")

        print("\nFinal status:")
        self.show_status()


# Run the scheduler
if __name__ == "__main__":
    scheduler = Scheduler()
    scheduler.start()
