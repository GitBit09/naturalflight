from flask import Flask, render_template, request, jsonify
from groq import Groq
import json
import re
import os

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are NaturalFlight, an expert drone mission planner AI. 
When given a plain English mission description, you:
1. Parse the intent (survey, delivery, inspection, search & rescue, formation, etc.)
2. Generate a complete Python flight plan using DroneKit/MAVLink-style pseudocode
3. Include waypoints with lat/lon offsets (use relative coords from home base 0,0), altitude, speed
4. Add safety checks (geofence, battery reserve, max altitude, return-to-home)
5. Provide a structured JSON mission summary

ALWAYS respond with EXACTLY this JSON format (no markdown, no extra text):
{
  "mission_name": "string",
  "mission_type": "survey|delivery|inspection|search_rescue|formation|patrol",
  "summary": "2-3 sentence plain English summary of what the drone will do",
  "safety_checks": ["list", "of", "safety", "checks"],
  "waypoints": [
    {"id": 1, "label": "Takeoff", "x": 0, "y": 0, "alt": 10, "action": "TAKEOFF", "speed": 2},
    {"id": 2, "label": "WP1", "x": 50, "y": 0, "alt": 30, "action": "WAYPOINT", "speed": 5}
  ],
  "estimated_time": "X minutes",
  "estimated_battery": "X%",
  "max_altitude": "Xm",
  "code": "# Complete Python flight plan code here\\nimport time\\n\\ndef execute_mission():\\n    # your full code"
}
Generate realistic waypoints (x,y in meters from home, typically -200 to 200 range).
The code should be complete, runnable pseudocode with comments."""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plan', methods=['POST'])
def plan_mission():
    data = request.json
    mission_description = data.get('description', '')
    
    if not mission_description:
        return jsonify({'error': 'No mission description provided'}), 400
    
    try:
        message = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=2000,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Plan this drone mission: {mission_description}"}
            ]
        )
        
        response_text = message.choices[0].message.content.strip()
        # Clean up any potential markdown
        response_text = re.sub(r'^```json\s*', '', response_text)
        response_text = re.sub(r'\s*```$', '', response_text)
        
        mission_data = json.loads(response_text)
        return jsonify({'success': True, 'mission': mission_data})
        
    except json.JSONDecodeError as e:
        return jsonify({'error': f'Failed to parse mission: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
