# 🚑 Smart Emergency Response Routing System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.13-blue.svg)
![Tkinter](https://img.shields.io/badge/Tkinter-GUI-green.svg)
![AI](https://img.shields.io/badge/AI-Pathfinding-red.svg)
![Status](https://img.shields.io/badge/Status-Completed-success.svg)

**An AI-powered desktop application that helps ambulances find the fastest route to hospitals by intelligently avoiding traffic congestion and obstacles.**

</div>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [Key Features](#key-features)
- [AI Algorithms](#ai-algorithms)
- [Smart Routing Tools](#smart-routing-tools)
- [System Architecture](#system-architecture)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [How to Use](#how-to-use)
- [Project Structure](#project-structure)
- [Results & Performance](#results--performance)
- [Limitations](#limitations)
- [Future Scope](#future-scope)
- [Contributors](#contributors)
- [License](#license)

---

## 🎯 Overview

The **Smart Emergency Response Routing System** is a desktop-based application designed to assist ambulances in reaching hospitals as quickly as possible during critical situations. Unlike traditional GPS systems that focus on shortest distance, this system prioritizes **lowest Estimated Time of Arrival (ETA)** by considering real-world factors like traffic congestion, roadblocks, and accidents.

### The Problem

In busy cities, ambulances often get stuck in unpredictable traffic. Traditional GPS systems focus on the shortest *physical distance*, which may not be the *fastest route*, leading to critical delays during emergencies.

### Our Solution

We developed a **cost-aware AI system** that:
- Assigns higher "cost" values to congested roads (5 min penalty vs 1 min normal)
- Treats obstacles (accidents, construction) as impassable cells
- Dynamically calculates the fastest path using multiple AI algorithms
- Automatically selects the optimal route for emergency vehicles

---

## 🔑 Key Features

| Feature | Description |
|---------|-------------|
| 🗺️ **Interactive 2D Grid** | Custom city grid builder with click-and-draw interface |
| 🚦 **Dynamic Traffic Zones** | Mark congested areas with higher traversal costs |
| 🧱 **Obstacle Placement** | Add roadblocks, accidents, or construction sites |
| 🤖 **4 AI Algorithms** | A*, Dijkstra, Greedy BFS, and DFS for comparison |
| ⚡ **Find Best Route** | Auto-selects the optimal algorithm by comparing ETAs |
| 📊 **Compare All Tool** | Diagnostic window showing nodes explored & execution time |
| 🎬 **Real-time Animation** | Visualizes AI decision-making process step by step |
| 📈 **Performance Metrics** | Tracks time complexity and path cost for each algorithm |

---

## 🧠 AI Algorithms

### 1. A* Search (Optimal + Heuristic)

**How it works:** Balances actual traffic cost with a heuristic (Manhattan Distance) to efficiently target the destination.

**Result:** Finds the fastest route quickly without exploring unnecessary areas.
✓ Optimal path guaranteed
✓ Minimal nodes explored
✓ Best overall performance

text

### 2. Dijkstra's Algorithm (Exhaustive Cost-Based)

**How it works:** Spreads out in all directions, checking the cost of every road until finding the hospital.

**Result:** Guarantees the absolute fastest route but explores more nodes.
✓ Guaranteed optimal path
✗ Explores many unnecessary nodes
✗ Slower computation time

text

### 3. Greedy Best-First Search (Heuristic Only)

**How it works:** Focuses only on physical distance to the goal, ignoring traffic costs.

**Result:** Extremely fast but can drive straight into traffic jams.
✓ Very fast execution
✗ May choose suboptimal paths
✗ Blind to traffic penalties

text

### 4. Depth-First Search (Baseline)

**How it works:** Blindly follows a path until hitting a dead end, then backtracks.

**Result:** Included to demonstrate why advanced AI is necessary.
✗ Creates inefficient, winding routes
✗ Not suitable for emergencies
✓ Useful for educational comparison

text

---

## 🛠️ Smart Routing Tools

### Find Best Route (One-Click Solution)

Instead of guessing which algorithm to use, this tool:
1. Runs A*, Dijkstra, and Greedy BFS simultaneously
2. Compares their final ETAs
3. Automatically selects and displays the optimal route

### Compare All 4 Diagnostic Tool

Opens a comprehensive window showing:
- **Total path cost** (ETA in minutes)
- **Nodes explored** (search space size)
- **Execution time** (milliseconds)
- **Algorithm comparison** (mathematical proof of performance)

**Example Output:**
A*: 27 min | 107 nodes | 0.023 sec ✓ Best
Dijkstra: 27 min | 453 nodes | 0.089 sec
Greedy BFS: 35 min | 89 nodes | 0.012 sec
DFS: 52 min | 412 nodes | 0.041 sec

text

---

## 🏗️ System Architecture
┌─────────────────────────────────────────────────────────────┐
│ LAYER 1: VIEW │
│ (Tkinter GUI - gui.py) │
│ User draws grid, places obstacles, traffic │
└─────────────────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────┐
│ LAYER 2: MODEL │
│ (grid.py - Engine) │
│ Stores coordinates, traffic costs, obstacles │
└─────────────────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────┐
│ LAYER 3: LOGIC │
│ (algorithms/ - AI Core) │
│ A* | Dijkstra | Greedy BFS | DFS | Compare Tool │
└─────────────────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────┐
│ LAYER 4: OUTPUT │
│ Route visualization & statistics │
└─────────────────────────────────────────────────────────────┘

text

### Working Mechanism

1. **Step 1 (View):** User draws map on Tkinter GUI
2. **Step 2 (Model):** `grid.py` saves coordinates and costs
3. **Step 3 (Logic):** GUI sends map data to AI algorithms
4. **Step 4 (Execution):** AI calculates fastest path
5. **Step 5 (Animation):** GUI smoothly animates AI's decision process

---

## 💻 Tech Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.13 | Core language with powerful data structures |
| **Tkinter** | Standard | GUI framework for interactive dashboard |
| **Heapq** | Standard | Priority queues for efficient AI execution |
| **Time** | Standard | Performance tracking in milliseconds |
| **Math** | Standard | Manhattan distance heuristic calculations |

---

## 📦 Installation

### Prerequisites
- Python 3.13 or higher
- pip package manager

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/smart-emergency-routing.git
cd smart-emergency-routing

# 2. No external dependencies required! (uses Python standard library only)

# 3. Run the application
python gui.py
🎮 How to Use
Step-by-Step Guide
Launch the Application

bash
python gui.py
Set Up the Grid

Click on cells to place elements

Green: Ambulance (start point)

Red: Hospital (destination)

Black: Obstacles (blocked roads)

Orange: Traffic zones (congestion penalty = 5 min)

Select an Algorithm

Choose from: A*, Dijkstra, Greedy BFS, or DFS

Click "Run" to visualize the pathfinding process

Use Smart Tools

Find Best Route: Let AI choose the optimal algorithm

Compare All 4: Open diagnostic window for detailed comparison

Analyze Results

View path highlighted in cyan

Check statistics panel for ETA, nodes explored, execution time

Controls
Action	Method
Place Ambulance	Click on cell, select "Set Start"
Place Hospital	Click on cell, select "Set Goal"
Add Traffic	Click + drag on grid
Add Obstacles	Click + drag on grid
Clear Grid	Press "Clear" button
Reset All	Press "Reset" button
📁 Project Structure
text
smart-emergency-routing/
│
├── gui.py                    # Main application & interactive dashboard
├── grid.py                   # Environment engine (grid management)
│
├── algorithms/               # AI Pathfinding Core
│   ├── __init__.py
│   ├── a_star.py            # A* algorithm implementation
│   ├── dijkstra.py          # Dijkstra's algorithm
│   ├── greedy_bfs.py        # Greedy Best-First Search
│   ├── dfs.py               # Depth-First Search
│   └── comparator.py        # Compare All 4 diagnostic tool
│
├── utils/                    # Helper functions
│   ├── __init__.py
│   ├── heuristics.py        # Manhattan distance calculations
│   └── animations.py        # Path visualization logic
│
├── assets/                   # Images & icons
│   └── (screenshots)
│
└── README.md                # This file
📊 Results & Performance
Algorithm Comparison (Typical Scenario)
Algorithm	Path Cost	Nodes Explored	Time	Optimal
A*	27 min	107	0.023s	✓
Dijkstra	27 min	453	0.089s	✓
Greedy BFS	35 min	89	0.012s	✗
DFS	52 min	412	0.041s	✗
Key Findings
A achieves the best balance:* optimal path + minimal exploration

Dijkstra guarantees optimality but explores 4x more nodes than A*

Greedy BFS is fastest but sacrifices path quality in traffic

DFS proves unsuitable for time-critical emergency routing

⚠️ Limitations
Limitation	Reason
No diagonal movement	Mimics real city block layouts
Static traffic only	Traffic doesn't change during simulation
Single ambulance routing	No multi-agent coordination
No live API integration	Uses simulated grid, not real maps
No moving obstacles	Cars/pedestrians not simulated
🔮 Future Scope
Live API Integration - Connect to Google Maps/OpenStreetMap for real road data

Live Traffic Data - Fetch real-time congestion from traffic APIs

Multi-Agent Routing - Coordinate multiple ambulances simultaneously

Mobile App - Deploy as Android/iOS application

Voice Commands - Hands-free operation for dispatchers

Hospital Availability - Consider bed availability in routing

Machine Learning - Predict traffic patterns based on time/day

👥 Contributors
Name	Registration No.	Role
Umair Hassan	FA24-BCS-104	AI Algorithm Implementation
Muhammad Farhan	FA24-BCS-064	GUI & Visualization
Muhammad Furqan Arshad	FA24-BCS-065	System Architecture & Testing
Course: Artificial Intelligence (CSC262)
Instructor: Ma'am Farah Saeed
Department: Computer Science, COMSATS University Islamabad
Class: BCS-4B
Date: April 5, 2026

📚 References
CSC262: Artificial Intelligence - I Course Lectures, CUI Islamabad

Python Software Foundation - Tkinter GUI documentation

Russell, S., & Norvig, P. - Artificial Intelligence: A Modern Approach

Online literature on A* and Dijkstra applications in grid-based pathfinding

📄 License
This project is submitted as part of academic requirements for the Artificial Intelligence course at COMSATS University Islamabad.

