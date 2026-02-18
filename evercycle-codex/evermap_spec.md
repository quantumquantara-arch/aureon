# Evermap Specification
Visualization layer for the Evercycle Codex

The Evermap is the primary visual expression of the Evercycle Codex.  
It is used in internal tools, dashboards, and (optionally) user-facing interfaces to show nested temporal context.


## 1. Conceptual layout

The Evermap is a circular, layered diagram:

1. Outer ring — Aeonic Wheel (12 segments)  
2. Middle ring — Civilizational Wave (6 segments)  
3. Inner field — Coherence Heatmap (κ, τ, Σ)  
4. Marker — Personal Continuity Phase (1–108)


## 2. Input payload

The Evermap consumes `evermap_payload` as defined in `evercycle_schema.md`.

Example payload (in JSON form):

{
  "cosmic": 7.3,
  "civilizational": 4.6,
  "personal": 88,
  "metrics": {
    "kappa": 0.62,
    "tau": 0.47,
    "sigma": 0.71
  },
  "derived": {
    "stability_index": -0.09,
    "personal_resonance_score": 0.455,
    "collapse_probability": 0.38
  },
  "annotations": "Late-tension, pre-reorganization era; personal phase in late expansion."
}


## 3. Rendering rules

### 3.1 Aeonic Wheel

- 12 equal angular segments (30° each).  
- `cosmic` (aeon_phase) determines the highlighted segment.  
- For non-integer values (e.g., 7.3), visually blend between adjacent segments to show transition.

### 3.2 Civilizational Wave

- 6 segments forming a second ring inside the Aeonic Wheel.  
- `civilizational` determines the active slice (1–6, with interpolation allowed).  

Suggested semantic colors (implementation-specific):

- 1 Initiation — cool, emerging  
- 2 Expansion — bright, outward  
- 3 Tension — amber / warning  
- 4 Crisis — red / high alert  
- 5 Reorganization — violet / transformative  
- 6 Stabilization — green/blue / coherent  


### 3.3 Coherence Heatmap

- The inner circular field visualizes κ, τ, Σ.  

Suggested mapping:

- High κ, high τ, low Σ → calm, coherent palette (smooth gradients).  
- Low κ, low τ, high Σ → turbulent palette (sharp contrasts, “stormy”).  
- Intermediate values → graded transitions.

Exact color choices are up to the UI layer, but semantics must stay consistent so users can learn to “read” the map.


### 3.4 Personal Continuity Marker

- If `personal` is present:
  - Render a point, ring, or glyph indicating the current personal_phase (1–108).  
  - Option 1 (simpler): map phases to angle only (e.g., 108 steps around the circle).  
  - Option 2 (richer): use angle for phase arc (dissolution → integration) and radius for coherence (function of κ and Σ).

- If `personal` is null:
  - Omit the marker or show a neutral icon indicating “no personal data”.


## 4. Interaction (optional)

For interactive UIs:

- Hover / tap Aeonic ring:
  - Show phase number, name, and brief description.  

- Hover / tap Civilizational ring:
  - Show current civilizational_phase, risks, and opportunities.  

- Hover / tap personal marker:
  - Show current personal_phase band (e.g., “late expansion”) and κ, τ, Σ in human-readable form.  

- Provide toggle:
  - “Global view only”
  - “Global + Personal view”

All personal data displays must respect user consent.


## 5. Use cases

- Internal Quantara dashboards for monitoring global coherence and risk.  
- Aureon debug/ops tools for inspecting how temporal context is being read.  
- NexLevelAI simulation interfaces for visualizing different futures under varying Evercycle states.  
- Optional educational or public tools to help people see how personal and collective cycles intersect.


## 6. Implementation notes

- Rendering technology is flexible (SVG, Canvas, WebGL, React chart libraries, etc.).  
- The Evermap should support theming (light/dark) without changing semantic color meanings.  
- Degrade gracefully:
  - If only cosmic data: show Aeonic Wheel only.  
  - If cosmic + civilizational: show both rings, no personal marker.  

- Privacy:
  - Never encode sensitive personal context in the payload beyond what is strictly needed.  
  - Any user-facing Evermap for individuals must be explicitly opt-in.

The Evermap is not the Codex itself; it is the lens that makes the Evercycle Codex visible and intuitive to humans and systems.
```0
