<div align="center">
```
████████╗ █████╗ ██╗     ███████╗███╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗
╚══██╔══╝██╔══██╗██║     ██╔════╝████╗  ██║██╔════╝╚██╗ ██╔╝████╗  ██║██╔════╝
   ██║   ███████║██║     █████╗  ██╔██╗ ██║███████╗ ╚████╔╝ ██╔██╗ ██║██║
   ██║   ██╔══██║██║     ██╔══╝  ██║╚██╗██║╚════██║  ╚██╔╝  ██║╚██╗██║██║
   ██║   ██║  ██║███████╗███████╗██║ ╚████║███████║   ██║   ██║ ╚████║╚██████╗
   ╚═╝   ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═══╝ ╚═════╝
```

**A comprehensive, interactive Operating Systems simulation & visualization suite**

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![CustomTkinter](https://img.shields.io/badge/CustomTkinter-Modern_UI-1F6FEB?style=for-the-badge)](https://github.com/TomSchimansky/CustomTkinter)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualizations-11557C?style=for-the-badge)](https://matplotlib.org)
[![NetworkX](https://img.shields.io/badge/NetworkX-Graph_Analysis-orange?style=for-the-badge)](https://networkx.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)]()

---

### 🌐 [**Live Demo → rishvinreddy.github.io/Interactive-Disk-Scheduling-Algorithm-Visualizer**](https://rishvinreddy.github.io/Interactive-Disk-Scheduling-Algorithm-Visualizer/)

---

*Formerly: Disk Scheduling Algorithm Visualizer*

</div>

---

## 📑 Table of Contents

| # | Section |
|---|---------|
| 1 | [Overview](#overview) |
| 2 | [Live Demo](#live-demo) |
| 3 | [System Architecture](#system-architecture) |
| 4 | [Module Breakdown](#module-breakdown) |
| 5 | [Algorithms Reference](#algorithms-reference) |
| 6 | [Tech Stack](#tech-stack) |
| 7 | [Project Structure](#project-structure) |
| 8 | [Setup & Installation](#setup--installation) |
| 9 | [Usage Guide](#usage-guide) |
| 10 | [Performance Benchmarks](#performance-benchmarks) |
| 11 | [Viva Prep](#viva-prep--interview-notes) |

---

## Overview

**Talensync OS Simulation Engine** is a full-featured Python GUI application that brings Operating System theory to life through real-time simulation and interactive visualization. What began as a simple disk scheduling tool has evolved into a multi-module OS learning platform.

> Built for OS coursework, academic demos, lab sessions, and viva preparation.
```
┌─────────────────────────────────────────────────────────────────────┐
│                    WHAT THIS PROJECT COVERS                         │
├──────────────────────┬──────────────────────┬───────────────────────┤
│   💾 Disk I/O        │   🧠 CPU Scheduling   │   🔒 Deadlock         │
│   FCFS, SSTF, SCAN   │   FCFS, SJF, RR, P   │   RAG + Banker's Algo │
├──────────────────────┼──────────────────────┼───────────────────────┤
│   🔄 Synchronization │   📁 File Systems     │   🔁 Process States   │
│   Mutex + Race Cond  │   Contiguous/Linked   │   New→Ready→Run→Term  │
└──────────────────────┴──────────────────────┴───────────────────────┘
```

---

## 🌐 Live Demo

> 🚀 **Try the interactive web version instantly — no installation required:**

### **[https://rishvinreddy.github.io/Interactive-Disk-Scheduling-Algorithm-Visualizer/](https://rishvinreddy.github.io/Interactive-Disk-Scheduling-Algorithm-Visualizer/)**
```
┌──────────────────────────────────────────────────────────────────────┐
│  🌍  LIVE DEMO FEATURES                                              │
│                                                                      │
│   ✅  Disk Scheduling Visualizer (Browser-based)                     │
│   ✅  Interactive graph animations                                   │
│   ✅  FCFS · SSTF · SCAN — all runnable in-browser                   │
│   ✅  Zero setup — works on any device                               │
│   ✅  Mobile friendly                                                │
│                                                                      │
│  URL: rishvinreddy.github.io/Interactive-Disk-Scheduling-            │
│       Algorithm-Visualizer/                                          │
└──────────────────────────────────────────────────────────────────────┘
```

---

## System Architecture

### High-Level Application Flow
```
┌─────────────────────────────────────────────────────────────────────────┐
│                        TALENSYNC ENGINE                                 │
│                                                                         │
│   ┌──────────────┐        ┌─────────────────────────────────────────┐  │
│   │   main.py    │───────▶│         OS Architecture Dashboard        │  │
│   │  (Entry Pt.) │        │   [Central Hub + Real-Time Log Stream]   │  │
│   └──────────────┘        └────────────────┬────────────────────────┘  │
│                                            │                            │
│              ┌─────────────────────────────┼──────────────────────┐    │
│              │             Sidebar Navigation                       │    │
│              └──┬──────┬──────┬──────┬────┴──────┬───────┬────────┘    │
│                 │      │      │      │            │       │             │
│                 ▼      ▼      ▼      ▼            ▼       ▼             │
│   ┌──────────┐ ┌───┐ ┌───┐ ┌────┐ ┌─────┐ ┌──────┐ ┌─────────┐       │
│   │  Disk    │ │CPU│ │DL │ │Sync│ │ FS  │ │ Proc │ │ Factory │       │
│   │  I/O     │ │Sch│ │Det│ │    │ │Alloc│ │States│ │Hardware │       │
│   └────┬─────┘ └─┬─┘ └─┬─┘ └──┬─┘ └──┬──┘ └──┬───┘ └────┬────┘       │
│        │         │     │      │       │        │           │           │
│        ▼         ▼     ▼      ▼       ▼        ▼           ▼           │
│   ┌──────────────────────────────────────────────────────────────────┐ │
│   │             Matplotlib · NetworkX · ReportLab · CustomTkinter    │ │
│   │                    [ Visualization & Export Layer ]               │ │
│   └──────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
```

### Module Interaction Diagram
```
                    ┌─────────────────────┐
                    │    Dashboard (Hub)   │
                    │  ┌───────────────┐  │
                    │  │  Event Logger  │  │
                    │  │  Metric Store  │  │
                    │  └───────────────┘  │
                    └──────────┬──────────┘
                               │ fires events
          ┌────────────────────┼────────────────────┐
          │                    │                    │
          ▼                    ▼                    ▼
  ┌───────────────┐   ┌────────────────┐   ┌───────────────┐
  │  Disk Module  │   │  CPU Scheduler │   │  Deadlock Det │
  │  ─────────── │   │  ──────────── │   │  ─────────── │
  │  Algorithm    │   │  Process Queue │   │  RAG Builder  │
  │  Engine       │   │  Gantt Chart   │   │  Banker's Algo│
  │  Animation    │   │  Burst Calc    │   │  Safe State   │
  └───────┬───────┘   └────────┬───────┘   └──────┬────────┘
          │                    │                   │
          └────────────────────┼───────────────────┘
                               │
                    ┌──────────▼──────────┐
                    │   Export / Report   │
                    │   (ReportLab PDF)   │
                    └─────────────────────┘
```

---

## Module Breakdown

### 💾 Module 1 — Disk I/O Management
```
  Disk Track Layout  (0 ──────────────────────────── 199)

  Head: 53 ──▶
  Requests: [98, 183, 37, 122, 14, 124, 65, 67]

  FCFS:   53→98→183→37→122→14→124→65→67     Total: 640
  SSTF:   53→65→67→37→14→98→122→124→183     Total: 236  ← ✅ Best
  SCAN:   53→65→67→98→122→124→183→37→14     Total: 331
```

**Algorithms Supported:**

| Algorithm | Strategy | Starvation Risk | Complexity |
|-----------|----------|-----------------|------------|
| FCFS | First Come First Serve | Low | O(n) |
| SSTF | Shortest Seek Time First | **High** | O(n²) |
| SCAN | Elevator (bidirectional) | None | O(n log n) |
| C-SCAN | Circular SCAN | None | O(n log n) |
| LOOK | SCAN up to last request | None | O(n log n) |
| C-LOOK | Circular LOOK | None | O(n log n) |

---

### 🧠 Module 2 — CPU Scheduling
```
  Process Timeline (Gantt Chart View)

  P1 ██████░░░░░░░░░░░░░░
  P2 ░░░░░░████░░░░░░░░░░
  P3 ░░░░░░░░░░██████░░░░
  P4 ░░░░░░░░░░░░░░░░████
       0    5   10   15   20  → Time (ms)

  Legend:  █ = Executing   ░ = Waiting
```

| Algorithm | Type | Preemptive | Best Use Case |
|-----------|------|------------|---------------|
| FCFS | Non-preemptive | ❌ | Batch systems |
| SJF | Non-preemptive | ❌ | Short jobs known upfront |
| SRTF | Preemptive SJF | ✅ | Real-time estimation |
| Round Robin | Time-quantum | ✅ | Time-sharing systems |
| Priority | Priority-based | ✅/❌ | Mixed priority tasks |

---

### 🔒 Module 3 — Deadlock Detection & Analysis
```
  Resource Allocation Graph (RAG)

       P1 ──requests──▶ R1
       P1 ◀──holds────  R2
       P2 ──requests──▶ R2
       P2 ◀──holds────  R1

                  ↑
         DEADLOCK DETECTED ⚠️
         (Circular Wait Condition)

  Banker's Algorithm — Safe Sequence Finder:
  ┌────┬──────────┬──────────┬────────────┐
  │ P# │ Max Need │Allocation│  Remaining │
  ├────┼──────────┼──────────┼────────────┤
  │ P0 │  7 5 3   │  0 1 0   │   7 4 3    │
  │ P1 │  3 2 2   │  2 0 0   │   1 2 2    │
  │ P2 │  9 0 2   │  3 0 2   │   6 0 0    │
  │ P3 │  2 2 2   │  2 1 1   │   0 1 1    │
  │ P4 │  4 3 3   │  0 0 2   │   4 3 1    │
  └────┴──────────┴──────────┴────────────┘
  Available: [3, 3, 2]
  Safe Sequence: P1 → P3 → P4 → P0 → P2  ✅
```

---

### 🔄 Module 4 — Process Synchronization
```
  Mutex Lock Simulation

  Thread-1: LOCK(mutex) ──▶ [Critical Section] ──▶ UNLOCK(mutex)
                                    ║
  Thread-2: LOCK(mutex) ──▶ ░░░WAITING░░░░░░░░ ──▶ [Critical Section]
                                    ↑
                             Blocked until T1 releases

  Race Condition Scenario (No Lock):
  Thread-1 reads x=5 ──▶ computes x+1=6
  Thread-2 reads x=5 ──▶ computes x+1=6
  Both write 6 ──▶ LOST UPDATE ❌  (expected x=7)
```

---

### 📁 Module 5 — File System Allocation
```
  ┌─── CONTIGUOUS ──────────────────────────────────────┐
  │  Block: [0][1][2][3][4][5][6][7][8][9][10][11][12] │
  │  File A:  ████████████░░░░░░░░░░░░░░░░░░░░░░        │
  │  File B:  ░░░░░░░░░░░░████████░░░░░░░░░░░░░         │
  └─────────────────────────────────────────────────────┘

  ┌─── LINKED ──────────────────────────────────────────┐
  │  [Block 0]──▶[Block 3]──▶[Block 7]──▶[Block 11]▶NULL│
  │  File data     data        data         data         │
  └─────────────────────────────────────────────────────┘

  ┌─── INDEXED ─────────────────────────────────────────┐
  │  Index Block: [3][7][11][15]                         │
  │       │        │   │    │                            │
  │       ▼        ▼   ▼    ▼                            │
  │    Block3   Blk7 Blk11 Blk15  (file data)            │
  └─────────────────────────────────────────────────────┘
```

| Method | Access | Fragmentation | Overhead |
|--------|--------|---------------|----------|
| Contiguous | O(1) | External | Low |
| Linked | O(n) | None | Medium (pointers) |
| Indexed | O(1) | None | High (index block) |

---

### 🔁 Module 6 — Process Lifecycle States
```
                    ┌─────────────┐
        ┌──────────▶│    NEW      │
        │           └──────┬──────┘
        │                  │ admitted
        │           ┌──────▼──────┐
        │     ┌────▶│    READY    │◀────────┐
        │     │     └──────┬──────┘         │
        │  I/O│            │ scheduled       │ I/O done
        │  done     ┌──────▼──────┐         │
        │     │     │   RUNNING   │─────────┘
        │     │     └──────┬──────┘
        │     │            │ wait(event)
        │     │     ┌──────▼──────┐
        │     └─────│   WAITING   │
        │           └─────────────┘
        │                  │ exit
        │           ┌──────▼──────┐
        └───────────│  TERMINATED │
                    └─────────────┘
```

---

## Tech Stack
```
┌─────────────────────────────────────────────────────────────────┐
│                        TECH STACK                               │
├─────────────────────┬───────────────────────────────────────────┤
│  Language           │  Python 3.x                               │
├─────────────────────┼───────────────────────────────────────────┤
│  GUI Framework      │  CustomTkinter (dark/light adaptive UI)   │
│                     │  Tkinter (base widgets)                   │
├─────────────────────┼───────────────────────────────────────────┤
│  Visualization      │  Matplotlib (plots + animations)          │
│                     │  NetworkX (graph-based deadlock RAGs)     │
├─────────────────────┼───────────────────────────────────────────┤
│  Export             │  ReportLab (PDF report generation)        │
├─────────────────────┼───────────────────────────────────────────┤
│  Web Demo           │  HTML · CSS · JavaScript (GitHub Pages)   │
└─────────────────────┴───────────────────────────────────────────┘
```

---

## Project Structure
```
Talensync-OS-Simulation-Engine/
│
├── 📄 main.py                          ← Application entry point
├── 📄 disk_scheduling_gui.py           ← Legacy standalone visualizer
├── 📄 requirements.txt
├── 📄 README.md
│
├── 📁 OS_Simulation_Suite/
│   ├── 📄 main.py                      ← Suite launcher
│   ├── 📄 dashboard.py                 ← Central hub + real-time logs
│   │
│   ├── 📁 modules/
│   │   ├── 📄 disk_io.py               ← Disk scheduling algorithms
│   │   ├── 📄 cpu_scheduling.py        ← CPU scheduler + Gantt chart
│   │   ├── 📄 deadlock.py              ← RAG + Banker's Algorithm
│   │   ├── 📄 synchronization.py       ← Mutex + race condition sim
│   │   ├── 📄 file_system.py           ← File allocation strategies
│   │   ├── 📄 process_states.py        ← State transition visualizer
│   │   └── 📄 factory_monitor.py       ← Factory hardware simulation
│   │
│   ├── 📁 utils/
│   │   ├── 📄 algorithm_engine.py      ← Core algorithm logic
│   │   ├── 📄 report_exporter.py       ← ReportLab PDF export
│   │   └── 📄 random_generator.py      ← Test data generator
│   │
│   └── 📁 assets/
│       └── 📄 themes.py                ← Dark/Light theme config
│
└── 📁 web/                             ← GitHub Pages live demo
    ├── 📄 index.html
    ├── 📄 style.css
    └── 📄 visualizer.js
```

---

## Setup & Installation

### Prerequisites
```
✅ Python 3.8 or higher
✅ pip (Python package manager)
✅ Git
```

### Installation Steps
```bash
# 1. Clone the repository
git clone https://github.com/RishvinReddy/Interactive-Disk-Scheduling-Algorithm-Visualizer.git

# 2. Navigate to the project directory
cd Interactive-Disk-Scheduling-Algorithm-Visualizer

# 3. (Recommended) Create a virtual environment
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows

# 4. Install all dependencies
pip install -r requirements.txt

# 5. Launch the full suite
cd OS_Simulation_Suite
python main.py

# --- OR run the legacy single-file disk visualizer ---
python disk_scheduling_gui.py
```

### Dependencies (`requirements.txt`)
```
customtkinter>=5.2.0
matplotlib>=3.7.0
networkx>=3.1
reportlab>=4.0.0
```

---

## Usage Guide

### 🖥️ Dashboard Navigation
```
┌────────────────────────────────────────────────────────────────┐
│  TALENSYNC  [Dark ●]                              [Minimize][X] │
├────────────┬───────────────────────────────────────────────────┤
│            │                                                    │
│  🏠 Home   │         ← Module Content Area →                   │
│            │                                                    │
│  💾 Disk   │   Simulation controls, graphs,                     │
│            │   and real-time metrics appear here                │
│  🧠 CPU    │                                                    │
│            │                                                    │
│  🔒 DLock  │                                                    │
│            ├───────────────────────────────────────────────────┤
│  🔄 Sync   │  📋 REAL-TIME LOG                                  │
│            │  [12:01] Disk SCAN completed — Seek: 331           │
│  📁 Files  │  [12:02] Deadlock detected in RAG — P1, P2        │
│            │  [12:03] Safe sequence found: P1→P3→P0            │
│  🔁 States │                                                    │
│            │                                                    │
│  🏭 Factory│                                                    │
└────────────┴───────────────────────────────────────────────────┘
```

### Disk Scheduling — Step by Step

| Step | Action |
|------|--------|
| 1 | Enter number of requests OR click **"Generate Random Test"** |
| 2 | Fill in **Disk Requests** (space-separated integers, range 0–199) |
| 3 | Set **Initial Head Position** (single integer) |
| 4 | Choose **SCAN Direction** — Left or Right |
| 5 | Click **"Run All Algorithms"** |
| 6 | View the **Comparison Table** for seek totals |
| 7 | Open **visual graphs** per algorithm |
| 8 | Export results as **PDF report** (optional) |

### Sample Input / Output
```
INPUT:
  Disk Requests    :  98 183 37 122 14 124 65 67
  Initial Head     :  53
  SCAN Direction   :  Right

OUTPUT COMPARISON TABLE:
  ┌───────────┬──────────────────────┬──────────┐
  │ Algorithm │ Seek Sequence        │  Total   │
  ├───────────┼──────────────────────┼──────────┤
  │ FCFS      │ 53→98→183→37→...    │   640    │
  │ SSTF      │ 53→65→67→37→...     │   236    │ ← ✅ BEST
  │ SCAN      │ 53→65→67→98→...     │   331    │
  └───────────┴──────────────────────┴──────────┘
```

---

## Performance Benchmarks

### Algorithm Efficiency Comparison (Sample Run)
```
  Total Head Movement (Lower = Better)

  FCFS   ████████████████████████████████ 640
  SCAN   █████████████████ 331
  SSTF   ████████████ 236  ← 🏆 Optimal
  LOOK   ██████████████ 280
  C-SCAN ███████████████████ 370
  C-LOOK ████████████████ 310

         0        200      400      600
```

### Big-O Complexity Reference

| Algorithm | Time Complexity | Space | Notes |
|-----------|----------------|-------|-------|
| FCFS | O(n) | O(1) | No sorting needed |
| SSTF | O(n²) | O(1) | Greedy nearest search |
| SCAN | O(n log n) | O(n) | Sort + single pass |
| C-SCAN | O(n log n) | O(n) | Circular variant |
| LOOK | O(n log n) | O(n) | Optimized SCAN |
| C-LOOK | O(n log n) | O(n) | Optimized C-SCAN |

---

## Viva Prep & Interview Notes

### The Four Conditions for Deadlock
```
  ALL four must hold simultaneously for deadlock to occur:

  1. MUTUAL EXCLUSION  ─ Only one process can use a resource at a time
  2. HOLD AND WAIT     ─ Process holds resources while waiting for more
  3. NO PREEMPTION     ─ Resources cannot be forcibly taken away
  4. CIRCULAR WAIT     ─ P1 waits for P2, P2 waits for P3, P3 waits for P1
```

### Quick Algorithm Cheatsheet
```
┌─────────────────┬──────────────────────────────────────────────────┐
│   FCFS          │ Service in arrival order. Simple but inefficient  │
│   SSTF          │ Go to closest request. Fast but may starve far    │
│                 │ requests                                           │
│   SCAN          │ Move in one direction like an elevator. Reverse   │
│                 │ at ends. Fair & prevents starvation               │
│   C-SCAN        │ Like SCAN but only one direction. Jumps back to   │
│                 │ start after reaching end. More uniform wait times  │
│   LOOK          │ SCAN but only goes as far as last request. Saves  │
│                 │ unnecessary head movement                          │
│   C-LOOK        │ Circular LOOK. Best overall in most benchmarks    │
└─────────────────┴──────────────────────────────────────────────────┘
```

### Key Definitions

| Term | Definition |
|------|-----------|
| Seek Time | Time for disk head to move to target track |
| Rotational Latency | Time waiting for sector to rotate under head |
| Transfer Time | Time to actually read/write the data |
| Starvation | A process perpetually denied CPU/resource access |
| Safe State | A state where a safe sequence of execution exists |
| Race Condition | Outcome depends on non-deterministic thread ordering |
| Critical Section | Code segment accessing shared resources |
| Mutual Exclusion | Only one process in critical section at a time |

---

<div align="center">

---

**Designed & Developed for Operating Systems Analysis & Teaching**

🌐 [Live Demo](https://rishvinreddy.github.io/Interactive-Disk-Scheduling-Algorithm-Visualizer/) · 
⭐ Star this repo if it helped you · 
🐛 Found a bug? Open an issue

---

*Built with Python · CustomTkinter · Matplotlib · NetworkX · ReportLab*

</div>
