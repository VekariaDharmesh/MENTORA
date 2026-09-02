"""
Subject-Aware Visual Engine
Dynamically generates educational SVG visuals for Physics circuits, Hydraulic water-pipes, Equations, and I-V curves.
"""

from typing import Dict, Any

class VisualEngineService:
    def render_circuit_svg(self, voltage: float = 9.0, resistance: float = 10.0, switch_closed: bool = True) -> Dict[str, Any]:
        """
        Generates clean electrical circuit SVG with dynamic calculated current.
        """
        current = round(voltage / resistance, 2) if switch_closed and resistance > 0 else 0.0
        glow_opacity = 0.25 if switch_closed else 0.0
        switch_x2 = 23 if switch_closed else 10
        switch_y2 = 0 if switch_closed else -22
        status_text = f"Continuous loop active • I = {current}A" if switch_closed else "Circuit broken • Current I = 0A"

        svg = f"""
        <svg class="circuit-svg" viewBox="0 0 460 210" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path class="circuit-wire" d="M 60 105 L 60 40 L 400 40 L 400 105" stroke="#29251F" stroke-width="2.2" stroke-linecap="round" />
          <path class="circuit-wire" d="M 60 135 L 60 175 L 400 175 L 400 135" stroke="#29251F" stroke-width="2.2" stroke-linecap="round" />
          <g class="circuit-battery" transform="translate(60, 105)">
            <line x1="-16" y1="0" x2="16" y2="0" stroke="#29251F" stroke-width="2.5" />
            <line x1="-9" y1="16" x2="9" y2="16" stroke="#29251F" stroke-width="3" />
            <text x="-38" y="11" font-family="'JetBrains Mono', monospace" font-size="11" fill="#766E63" font-weight="600">{voltage}V</text>
            <text x="-24" y="-4" font-family="'JetBrains Mono', monospace" font-size="10" fill="#B86D52">+</text>
            <text x="-24" y="24" font-family="'JetBrains Mono', monospace" font-size="11" fill="#766E63">−</text>
          </g>
          <g class="circuit-switch" transform="translate(210, 40)">
            <circle cx="-25" cy="0" r="3.5" fill="#29251F" />
            <circle cx="25" cy="0" r="3.5" fill="#29251F" />
            <line x1="-25" y1="0" x2="{switch_x2}" y2="{switch_y2}" stroke="#29251F" stroke-width="2.5" stroke-linecap="round" />
            <text x="-16" y="-12" font-family="'JetBrains Mono', monospace" font-size="9" fill="#766E63">SWITCH ({'CLOSED' if switch_closed else 'OPEN'})</text>
          </g>
          <g class="circuit-lamp" transform="translate(400, 120)">
            <circle cx="0" cy="0" r="22" fill="#D79A4B" opacity="{glow_opacity}" />
            <circle cx="0" cy="0" r="16" stroke="#29251F" stroke-width="2" fill="#FFF9F0" />
            <line x1="-10" y1="-10" x2="10" y2="10" stroke="#D79A4B" stroke-width="2" />
            <line x1="-10" y1="10" x2="10" y2="-10" stroke="#D79A4B" stroke-width="2" />
            <text x="24" y="5" font-family="'JetBrains Mono', monospace" font-size="11" fill="#766E63">R = {resistance}Ω</text>
          </g>
          <g transform="translate(130, 40)"><polygon points="0,-4 8,0 0,4" fill="#D79A4B" /><text x="-4" y="-8" font-family="'JetBrains Mono', monospace" font-size="9" fill="#D79A4B">I = {current}A →</text></g>
        </svg>
        """
        return {
            "type": "circuit",
            "voltage": voltage,
            "resistance": resistance,
            "current": current,
            "switch_closed": switch_closed,
            "status_text": status_text,
            "svg": svg.strip()
        }

    def render_water_pipe_svg(self, pressure_level: str = "High", pipe_width: str = "Narrow") -> Dict[str, Any]:
        """
        Generates hydraulic water-pipe analogy SVG comparing constriction vs flow.
        """
        is_narrow = (pipe_width.lower() == "narrow")
        constriction_height = 20 if is_narrow else 40
        flow_desc = "Restricted Flow (High Resistance)" if is_narrow else "High Flow (Low Resistance)"
        color = "#B86D52" if is_narrow else "#71886B"

        svg = f"""
        <svg class="player-svg-interactive" viewBox="0 0 460 210" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="2" y="2" width="456" height="206" rx="8" fill="#FFFDF9" stroke="{color}" />
          <!-- Pipe body -->
          <rect x="50" y="45" width="160" height="40" rx="4" fill="#EBF1EA" stroke="#71886B" stroke-width="1.8" />
          <text x="130" y="68" font-family="'JetBrains Mono', monospace" font-size="11" fill="#71886B" font-weight="600" text-anchor="middle">WIDE PIPE: FAST FLOW</text>
          
          <rect x="250" y="55" width="160" height="{constriction_height}" rx="4" fill="#F7E9E4" stroke="{color}" stroke-width="1.8" />
          <text x="330" y="68" font-family="'JetBrains Mono', monospace" font-size="11" fill="{color}" font-weight="600" text-anchor="middle">NARROW: CONSTRICTED</text>

          <!-- Water flow streamlines -->
          <path d="M 60 65 Q 100 60 140 65 T 200 65" stroke="#71886B" stroke-width="2.5" />
          <path d="M 260 65 Q 300 62 340 65 T 400 65" stroke="{color}" stroke-width="1.5" />

          <text x="130" y="115" font-family="'Fraunces', serif" font-size="12" fill="#29251F" text-anchor="middle">Low Resistance = High Current</text>
          <text x="330" y="115" font-family="'Fraunces', serif" font-size="12" fill="#29251F" text-anchor="middle">{flow_desc}</text>
        </svg>
        """
        return {
            "type": "water_pipe",
            "pressure": pressure_level,
            "pipe_width": pipe_width,
            "flow_description": flow_desc,
            "svg": svg.strip()
        }
