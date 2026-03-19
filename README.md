# NaturalFlight 🚁
### LLM-Powered Drone Mission Planner

> Describe a drone mission in plain English → Get executable MAVLink/Python flight code with waypoints, safety checks, and visual path map.

---

## What It Does

NaturalFlight uses Claude (Anthropic's LLM) to transform plain English mission descriptions into complete, structured drone flight plans. It generates:

- **Waypoints** with x/y coordinates, altitude, speed, and action type
- **Executable Python code** in MAVLink/DroneKit style
- **Safety checks** (geofence, battery reserve, RTH conditions)
- **Visual flight path** rendered on an interactive canvas map
- **Mission statistics** (estimated time, battery usage, max altitude)

## Demo

```
Input:  "Survey a 200x200m crop field in a lawnmower pattern at 30m altitude"

Output: 
  - 12 waypoints covering the field systematically
  - Python DroneKit code with arm/takeoff/waypoint/land sequence
  - Safety checks: geofence 300m, 20% battery reserve, max alt 120m
  - Visual grid flight path on canvas map
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| LLM | Claude claude-sonnet-4-20250514 (Anthropic) |
| Backend | Python Flask |
| Frontend | Vanilla JS + HTML5 Canvas |
| Prompt Engineering | Structured JSON output, mission type classification |

## Setup

```bash
# Clone the repo
git clone https://github.com/GitBit09/naturalflight
cd naturalflight

# Install dependencies
pip install -r requirements.txt

# Set your Anthropic API key
export ANTHROPIC_API_KEY=your_key_here

# Run
python app.py
# Visit http://localhost:5000
```

## Prompt Engineering Highlights

- **Structured JSON output** — LLM is constrained to return a strict schema with waypoints, code, safety checks
- **Mission type classification** — Automatically detects survey/delivery/inspection/search_rescue/formation/patrol
- **Relative coordinate system** — Waypoints use meters from home base (x,y), making output portable
- **Safety-first prompting** — System prompt enforces geofence, battery reserve, and RTH in every mission

## Example Missions to Try

- `Survey a 300×300m agricultural field in a grid pattern at 25m, capture photos every 5m`
- `Deliver a package to 50m north, 30m east at 15m altitude, then return home`
- `Inspect a 100m communication tower at 20m, 50m, 80m, and 100m altitudes`
- `Search a 500m radius area for a missing person using expanding spiral pattern`
- `Patrol the perimeter of a 150×80m warehouse at 20m altitude`

## Project Context

Built as part of exploration into LLM-powered engineering tools. Connects to prior research on autonomous multi-drone coordination (IIT Indore, 2025) by bridging natural language interfaces with flight control systems.

## License

MIT
