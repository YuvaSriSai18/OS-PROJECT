# **CPU Scheduler Simulation**

## **Description**

This Python program simulates a **CPU Scheduler** that dynamically manages multiple jobs across available CPU cores based on priority and core availability. The scheduler incorporates features such as **preemptive scheduling**, **job queueing**, and **fallback mechanisms** for core allocation. It is designed to provide insights into CPU scheduling concepts, job handling, and efficient resource allocation strategies.

The scheduler supports real-time job generation, prioritization, burst time updates, and core assignment. It also demonstrates key principles such as:

- **Priority-Based Scheduling**: Higher priority jobs are prioritized for execution.
- **Preemption**: Low-priority jobs may be replaced if a higher-priority job arrives.
- **Dynamic Queue Management**: Jobs waiting for resources are maintained in a priority queue.

---

## **Features**

- **Dynamic Job Creation**: Users can generate jobs with random parameters or specify job details.
- **Priority-Based Execution**: Jobs with higher priority are executed first. Equal-priority jobs follow a shortest job first (SJF) policy.
- **Core Management**: Allocates jobs to the most suitable cores based on requirements and availability.
- **Preemption**: Replaces lower-priority jobs with higher-priority ones.
- **Real-Time Updates**: Continuously updates burst times and manages job queues.
- **Simulation Clock**: Real-time simulation where 1 second equals 1 minute.
- **Job Completion Handling**: Automatically frees up cores and records completed jobs.

---

## **Core Configuration**

The system has the following CPU cores:

| Core Frequency | Quantity |
|----------------|----------|
| 4 GHz          | 2        |
| 3 GHz          | 4        |
| 2 GHz          | 4        |

---

## **Job Parameters**

Each job is defined by:
- **Name**: User-defined or system-generated.
- **Burst Time**: Execution time in minutes.
- **Priority**: Integer from 1 (highest) to 19 (lowest).
- **Core Requirement**: Specifies the desired CPU core frequency.
- **Arrival Time**: Automatically generated as the time since the scheduler started.

---

## **How It Works**

1. **Initialization**: The program initializes the cores, starts a simulation clock, and prepares for job scheduling.
2. **Job Creation**: Users can create jobs via the menu.
3. **Job Scheduling**:
   - Assigns jobs to cores based on priority and availability.
   - Falls back to lower-priority cores if required cores are unavailable.
   - Queues jobs if no cores are available or preemption is not possible.
4. **Preemption**: If a higher-priority job arrives, a lower-priority running job may be preempted and re-queued.
5. **Burst Time Update**: Reduces the burst time of running jobs at each clock tick, freeing cores upon job completion.
6. **Status Monitoring**: Displays the current state of the scheduler, including running jobs, queued jobs, and core availability.

---

## **Usage**

1. Run the program using Python 3:
   ```bash
   python cpu_scheduler.py
   ```
2. Follow the menu prompts:
   - **Start an App**: Create a new job.
   - **Exit Scheduler**: Stop the simulation and display the final status.

---

## **Dependencies**

- Python 3.x
- No external libraries are required.

---

## **Example Workflow**

1. **Start the Scheduler**: The program initializes cores and starts the clock.
2. **Create Jobs**: Add jobs with varying burst times, priorities, and core requirements.
3. **Observe Preemption**: Watch as higher-priority jobs preempt lower-priority ones.
4. **Monitor Queue**: Jobs waiting for execution are managed in a priority queue.
5. **View Status**: Continuously monitor job execution, core allocation, and queue status.
6. **Exit Scheduler**: Stop the simulation to view the final state.

---

## **Future Enhancements**

- Add support for additional scheduling algorithms (e.g., Round Robin, Multilevel Queue).
- Enable visualization of scheduling operations.
- Provide logging for job execution history and core utilization.
- Introduce user-defined job parameters for more control.

---

This program is an educational tool designed to demonstrate the principles of CPU scheduling and resource management. Happy scheduling! 🎉