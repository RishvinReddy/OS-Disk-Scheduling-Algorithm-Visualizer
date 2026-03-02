<<<<<<< HEAD
# Disk Scheduling Algorithm Visualizer

## Overview
A powerful and interactive Python-based GUI application to visualize, compare, and analyze Disk Scheduling Algorithms. This tool is designed for Operating Systems students and professionals to understand how different scheduling strategies optimize disk head movements.

This project visualizes disk head movement and compares disk scheduling algorithms based on total seek time.

## Features
- **Algorithms Implemented**:
  - **FCFS (First Come First Serve)**: Simple, servicing requests in order.
  - **SSTF (Shortest Seek Time First)**: Selects request closest to current head position.
  - **SCAN (Elevator Algorithm)**: Moves in one direction, servicing requests, then reverses.
- **Interactive GUI**:
  - **Comparison Table**: Side-by-side performance metrics (Total Head Movements).
  - **Visual Graphs**: `matplotlib` plots showing the seek operations for each algorithm.
  - **Best Algorithm Indicator**: Automatically highlights the most efficient algorithm.
- **Advanced Controls**:
  - **SCAN Direction**: Toggle start direction (Left/Right).
  - **Random Test Generator**: Generate random valid datasets (0-199 track range) for unbiased testing and demos.
  - **One-Click Run**: Execute all algorithms simultaneously.

## Requirements
- Python 3.x
- `matplotlib`
- `tkinter` (Standard Python library)

## Setup & Installation
1.  **Clone or Download** this repository.
2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## How to Run
Execute the main script:
```bash
python disk_scheduling_gui.py
```

##  Usage Guide
### 1. random Test Generation (Recommended)
-   Enter the **"Number of Requests"** (e.g., 8 or 10).
-   Click **"Generate Random Test"**.
-   The application will automatically fill the *Disk Requests* and *Initial Head Position* fields with valid data.

### 2. Manual Input
-   **Disk Requests**: Enter space-separated integers (e.g., `98 183 37 122 14 124 65 67`).
-   **Initial Head Position**: Enter a single integer (e.g., `53`).

### 3. Run & Analyze
-   Select **SCAN Direction** (Left or Right).
-   Click **"Run All Algorithms"**.
-   **View Results**: Check the Comparison Table for total head movements.
-   **View Graphs**: Interactive graphs will pop up for each algorithm.

##  Algorithms Brief (Viva Prep)
-   **FCFS**: Easiest to implement but often inefficient (high seek time).
-   **SSTF**: Reduces total head movement but can cause starvation for distant requests.
-   **SCAN**: "Elevator" approach; offers a good balance and prevents starvation by moving in a specific direction.

---
**Created for Operating Systems Project**
=======
# Talensync OS Simulation Engine
*(Formerly Disk Scheduling Algorithm Visualizer)*

## Overview
A powerful and comprehensive Python-based GUI application designed to simulate, visualize, and analyze various Operating System concepts. Initially created as a disk scheduling visualizer, this suite now encompasses a broad range of OS modules, making it an essential interactive toolkit for Operating Systems students, educators, and professionals.

## Modules & Features
- **OS Architecture Dashboard**: A central hub to monitor and orchestrate OS simulations.
- **Disk I/O Management**: Simulate and compare Disk Scheduling algorithms including FCFS, SSTF, SCAN, C-SCAN, LOOK, and C-LOOK. Features interactive metrics and animations.
- **Process Management (CPU Scheduling)**: Visualize how the CPU allocates time and executes processes using various scheduling algorithms.
- **Deadlock Detection & Analysis**: Simulate Resource Allocation Graphs (RAG) and evaluate safe states using the Banker's Algorithm with step-by-step table updates.
- **Process Synchronization**: Terminal-based simulation for Mutex locks and race conditions.
- **File System Allocation**: Visualizes Contiguous, Linked, and Indexed file allocation strategies.
- **Process Lifecycle States**: Interactive visualization of state transitions (New, Ready, Running, Waiting, Terminated).
- **Factory Hardware Monitoring**: Real-world application of deadlock scenarios in a simulated smart factory environment.

## Tech Stack
- **Python 3.x**
- **CustomTkinter**: Modern and dark/light mode responsive UI framework.
- **Tkinter**: Standard Python GUI toolkit.
- **Matplotlib & NetworkX**: For complex data visualizations, plots, and graphs.
- **ReportLab**: Export detailed simulation metrics as PDF reports.

## Setup & Installation
1. **Clone or Download** this repository.
2. Navigate to the `OS_Simulation_Suite` directory:
   ```bash
   cd "OS_Simulation_Suite"
   ```
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## How to Run
Execute the main application suite:
```bash
python main.py
```
*(Note: To run the legacy single-file disk visualizer, you can still run `python disk_scheduling_gui.py` from the root directory).*

## Usage Guide
### Navigating the Suite
- Use the **sidebar** to seamlessly switch between different OS modules.
- **Real-time Logs**: The Dashboard tab stores real-time simulation logs dynamically triggered by events across other tabs.

### Disk Scheduling Simulation
- **Random Data Generation**: Instantly populate requests with randomized valid inputs via the interactive UI controls.
- **One-Click Benchmarking**: Compare all disk scheduling algorithms side-by-side. The dashboard automatically highlights the most optimal sequence based on total seek time with an animated bar chart.
- **Visual Playback**: Control the speed of disk head animations, and use Play/Pause/Stop to examine seeks effectively.

---
**Designed and Developed for Operating Systems Analysis & Teaching Toolkit**
>>>>>>> 71fd2fa (Initial commit for Talensync OS Simulation Engine)
