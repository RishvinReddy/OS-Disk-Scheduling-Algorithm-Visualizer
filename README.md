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
