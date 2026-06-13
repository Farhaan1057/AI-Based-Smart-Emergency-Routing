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
