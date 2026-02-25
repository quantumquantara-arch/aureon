# Evercycle Codex — Visual Architecture Specification
Defines the visual grammar, diagram rules, iconography, color semantics, and layout guidelines for all Evercycle visualizations across Aureon's ecosystem.

This ensures consistency across:
- Evermap diagrams
- dashboards
- reports
- websites
- research publications
- internal visualization tools



# ------------------------------------
# 1. Visual Language Overview
# ------------------------------------

Evercycle visuals must follow three principles:

1. Concentricity  
   - All cycles are shown as nested rings.  
   - Outer = cosmic, middle = civilizational, inner = personal.

2. Angular Mapping  
   - Phase always maps to angle.  
   - 0–360° corresponds directly to normalized phase.

3. Coherence Field  
   - κ, τ, Σ influence color, texture, density, and gradients in the inner field.



# ------------------------------------
# 2. Primary Diagram — The Evermap
# ------------------------------------

Structure:
  Ring 1 (outer): Aeonic Wheel (12 segments)
  Ring 2 (middle): Civilizational Wave (6 segments)
  Ring 3 (inner): Coherence Field (continuous gradient)
  Marker: Personal-phase glyph or point

Layer order (top → bottom):
  - Personal marker
  - Coherence field
  - Civilizational ring
  - Cosmic ring
  - Background field



# ------------------------------------
# 3. Color Semantics
# ------------------------------------

Colors must reflect meaning, not aesthetics.

Cosmic phases (recommended palette):
  1–2   Emergence      → cool neutrals, soft dawn tones
  3–4   Expansion      → bright, outward blues/greens
  5–6   Tension        → amber/yellow warnings
  7–8   Crisis         → red spectrum
  9–10  Reconfiguration→ violet/indigo transitions
  11–12 Integration    → teal/cyan coherence tones

Civilizational phases:
  1 Initiation → muted blue-gray
  2 Expansion → soft green
  3 Tension → amber
  4 Crisis → red
  5 Reorganization → violet
  6 Stabilization → deep green/blue coherent tones


Coherence field (κ, τ, Σ):
  - High κ: smooth gradients
  - Low κ: fractured texture or sharp contrasts
  - High Σ: turbulent patterns
  - High τ: rhythmic, harmonious structure



# ------------------------------------
# 4. Personal Phase Markers
# ------------------------------------

Marker types:
  dot
  ring
  triangle glyph
  arc highlight

Mapping options:
  - Angle = phase number (1–108 normalized)
  - Radius = coherence (e.g., κ or SI)
  - Color accent = risk (Σ)

Example:
  P = 83, κ=0.7, Σ=0.2
    - angle: (83/108) * 360°
    - radius: moderately outward
    - color: coherent (teal/blue)



# ------------------------------------
# 5. Secondary Diagrams
# ------------------------------------

### Timeline View
Horizontal or radial timeline showing:
  - phase progression
  - transition events
  - risk windows
  - opportunity windows

### Coherence Vector Triangle
A triangular diagram representing:
  - κ (integration)
  - τ (alignment)
  - Σ (risk; inverted axis)

### Stress Topography Map
A 2D or 3D visualization of:
  - pressure zones
  - instability gradients
  - coherence pockets

### Archetype Wheel (108)
A circular mapping of:
  - all 108 archetypes
  - five arc regions
  - arc boundaries highlighted
  - transitions indicated



# ------------------------------------
# 6. Typography & Symbolism
# ------------------------------------

Typeface:
  - Clean, modern sans-serif (e.g., Inter, Roboto, Source Sans)
  - No serif fonts for primary diagrams

Symbolism:
  - Avoid mystical symbols in core diagrams; scientific tone
  - Optional “glyph set” may be used in secondary diagrams

Phase Glyphs (recommended):
  - Simple geometric shapes
  - Unambiguous
  - Minimalist



# ------------------------------------
# 7. Layout Guidelines
# ------------------------------------

Preferred aspect ratios:
  - 1:1 (square)
  - 16:9 (dashboards)
  - 4:3 (reports)

Padding:
  - 10–15% outer boundary padding
  - Rings spaced evenly

Contrast:
  - Maintain WCAG accessibility standards
  - Coherence field must not obscure rings



# ------------------------------------
# 8. Animation Guidelines (Optional)
# ------------------------------------

Allowed animations:
  - subtle rotation to indicate temporal flow
  - gentle pulsation for coherence field
  - marker transitions for personal phase changes

Forbidden:
  - rapid flashing
  - disorienting motion
  - complex 3D spins



# ------------------------------------
# 9. Export Specifications
# ------------------------------------

Supported output formats:
  - SVG (preferred)
  - PNG
  - WebGL canvas for interactive use
  - JSON for raw data exports

Minimum resolution:
  - 1024×1024 for diagrams
  - 1920×1080 for dashboards



# ------------------------------------
# 10. Purpose
# ------------------------------------

This visual architecture ensures:
- scientific clarity  
- aesthetic unity  
- interpretive precision  
- accessibility  
- compatibility across the Quantara ecosystem  

With these rules, anyone can build Evercycle visuals that look, feel, and operate exactly the same.
