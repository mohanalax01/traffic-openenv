---
title: traffic-openenv
emoji: 🚦
colorFrom: blue
colorTo: green
sdk: docker
app_file: app.py
pinned: false
---

# Traffic Signal Optimization Environment

## Overview
Simulates a real-world traffic system with emergency handling and congestion control.

## Tasks
- Easy: Low traffic
- Medium: Moderate traffic
- Hard: Heavy traffic + emergencies + spikes

## Action Space
- 0 → North-South green (lanes 0 & 2 move)
- 1 → East-West green (lanes 1 & 3 move)

## Observation Space
- cars: cars in each lane
- signal: current signal
- emergency: emergency presence
- queue_length: total cars waiting
- time_since_last_change: steps since signal switch

## Reward Function
- Minimize waiting time
- Handle emergency vehicles
- Penalize imbalance and switching

## Reproducibility
Use:
GET /reset?task=hard&seed=42