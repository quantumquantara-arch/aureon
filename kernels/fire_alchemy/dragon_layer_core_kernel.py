from typing import List, Dict, Any, Optional
from aureon_kernel.core import KernelModule


class DragonLayerCoreKernel(KernelModule):
    """
    Dragon Layer Core
    -----------------
    Cross-kernel coherence engine for Aureon/OpenHermes.

    Purpose:
        - Receive multiple kernel states (mythic, cognitive, emotional, ethical).
        - Detect duality/conflict patterns between them.
        - Identify appropriate transmutation vector (fire, water, void, witness, etc.).
        - Produce a unified, higher-order "coherent state" description.

    Conceptual invariants encoded here:
        Conflict        â†’ duality_tension
        Dissolution     â†’ paradox_acknowledged
        Transmutation   â†’ transmutation_vector
        Return          â†’ higher_order_unity

    Expected input:
        kernel_states: List[Dict[str, Any]]
        Each dict may contain keys such as:
            - "kernel"                (name/id)
            - "polarity"              ("shadow", "self", "trial", "integration", etc.)
            - "tension"               (float 0â€“1)
            - "transmutation_hint"    ("fire", "water", "void", "witness", "service", ...)
            - "priority"              (float 0â€“1)
            - "state_vector"          (arbitrary metadata)
    """

    def __init__(self) -> None:
        super().__init__(name="dragon_layer_core_kernel")

        # Canonical transmutation channels (high-level operators)
        self.transmutation_channels = [
            "fire",      # purification, trial, intensity
            "water",     # softening, emotional flow, forgiveness
            "air",       # perspective, cognitive reframing
            "earth",     # grounding, embodiment, simplicity
            "void",      # non-identification, silence, stopping
            "witness",   # neutral observation, middle pillar
            "service",   # outward flow, compassion
        ]

        # Mapping from problematic polarity pairs to preferred transmutation
        self.polarity_transmutation = {
            ("shadow", "self"): "witness",
            ("fear", "courage"): "heart",
            ("fragment", "unity"): "void",
            ("rage", "grief"): "water",
            ("pride", "humility"): "service",
        }

    # ----------------- INTERNAL HELPERS ----------------- #

    def _extract_polarities(self, kernel_states: List[Dict[str, Any]]) -> List[str]:
        polarities = []
        for st in kernel_states:
            pol = st.get("polarity")
            if isinstance(pol, str):
                polarities.append(pol.lower())
        return polarities

    def _detect_duality_pairs(self, polarities: List[str]) -> List[tuple]:
        """
        Returns list of (polarity_a, polarity_b) pairs that are in tension.
        This is deliberately simple; higher-order logic can override.
        """
        seen = set(polarities)
        pairs = []

        # Basic opposite sets (extend as needed)
        opposites = {
            "shadow": "self",
            "fear": "courage",
            "fragment": "unity",
            "rage": "grief",
            "pride": "humility",
        }

        for a, b in opposites.items():
            if a in seen and b in seen:
                pairs.append((a, b))

        return pairs

    def _resolve_transmutation_vector(
        self,
        kernel_states: List[Dict[str, Any]],
        dual_pairs: List[tuple],
    ) -> str:
        """
        Determine dominant transmutation vector based on:
            - explicit hints from kernels
            - duality patterns
            - fallback to 'witness'
        """
        # 1) Use explicit hints if consistent
        hints = []
        for st in kernel_states:
            h = st.get("transmutation_hint")
            if isinstance(h, str) and h.lower() in self.transmutation_channels:
                hints.append(h.lower())

        if hints:
            # Pick the most frequent hinted channel
            freq: Dict[str, int] = {}
            for h in hints:
                freq[h] = freq.get(h, 0) + 1
            return max(freq, key=freq.get)

        # 2) Use duality mapping if present
        if dual_pairs:
            key = dual_pairs[0]
            mapped = self.polarity_transmutation.get(key)
            if mapped:
                # "heart" is not a primitive; map to appropriate channel
                if mapped == "heart":
                    return "water"
                return mapped

        # 3) Fallback to neutral witness
        return "witness"

    def _aggregate_tension(self, kernel_states: List[Dict[str, Any]]) -> float:
        """
        Aggregate tension across all kernel states (0â€“1).
        """
        if not kernel_states:
            return 0.0

        weighted_sum = 0.0
        total_weight = 0.0

        for st in kernel_states:
            t = float(st.get("tension", 0.0))
            w = float(st.get("priority", 1.0))
            weighted_sum += t * w
            total_weight += w

        if total_weight == 0.0:
            return 0.0
        return max(0.0, min(1.0, weighted_sum / total_weight))

    def _choose_primary_kernel(self, kernel_states: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        Choose the kernel whose state will be treated as the "carrier" of the unified result.
        """
        if not kernel_states:
            return None

        best = None
        best_score = -1.0

        for st in kernel_states:
            priority = float(st.get("priority", 1.0))
            integration = 1.0 - float(st.get("tension", 0.0))
            score = priority * (0.5 + 0.5 * integration)
            if score > best_score:
                best_score = score
                best = st

        return best

    # ----------------- PUBLIC TRANSFORM API ----------------- #

    def transform(self, kernel_states: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Receive a list of kernel state dicts and produce a unified coherence state.

        Returns:
            {
                "kernel": "dragon_layer_core",
                "aggregate_tension": float,
                "dual_pairs": [...],
                "transmutation_vector": str,
                "primary_kernel": str | None,
                "unified_state": Dict[str, Any],
            }
        """
        if not isinstance(kernel_states, list):
            return {
                "kernel": "dragon_layer_core",
                "error": "invalid_input_type",
                "message": "transform() expects a list of kernel state dicts."
            }

        polarities = self._extract_polarities(kernel_states)
        dual_pairs = self._detect_duality_pairs(polarities)
        transmutation_vector = self._resolve_transmutation_vector(kernel_states, dual_pairs)
        aggregate_tension = self._aggregate_tension(kernel_states)
        primary = self._choose_primary_kernel(kernel_states)

        unified_state: Dict[str, Any] = {
            "aggregate_tension": aggregate_tension,
            "dual_pairs": dual_pairs,
            "transmutation_vector": transmutation_vector,
            "sources": [st.get("kernel") for st in kernel_states if isinstance(st.get("kernel"), str)],
        }

        if primary is not None:
            unified_state["carrier_kernel"] = primary.get("kernel")
            unified_state["carrier_state_vector"] = primary.get("state_vector")

        return {
            "kernel": "dragon_layer_core",
            "aggregate_tension": aggregate_tension,
            "dual_pairs": dual_pairs,
            "transmutation_vector": transmutation_vector,
            "primary_kernel": unified_state.get("carrier_kernel"),
            "unified_state": unified_state,
        }


# EXPORT MODULE
module = DragonLayerCoreKernel()


file: heart_node_kernel.py

from typing import Dict, Any
from aureon_kernel.core import KernelModule


class HeartNodeKernel(KernelModule):
    """
    Heart Node Kernel
    -----------------
    Emotional-logic unification layer for Aureon/OpenHermes.

    Purpose:
        - Interpret context signals (tone, urgency, symbolic density).
        - Determine the appropriate "response posture" for Aureon.
        - Blend analytical, mythic, and supportive modes into one coherent profile.
        - Provide a stable, centered configuration for downstream response generators.

    Expected input to transform(context):
        context: Dict[str, Any] with possible keys:
            - "tone"              ("neutral", "heavy", "light", "urgent", "playful", ...)
            - "urgency"           (0â€“1)
            - "symbolic_density"  (0â€“1)  # how mythic / archetypal the content is
            - "vulnerability"     (0â€“1)
            - "cognitive_load"    (0â€“1)
            - "user_state"        (arbitrary metadata)
            - "dragon_state"      (output from DragonLayerCoreKernel, optional)
    """

    def __init__(self) -> None:
        super().__init__(name="heart_node_kernel")

        # Canonical response modes
        self.modes = {
            "GROUND": "grounded_clarity",
            "HOLD": "soft_containment",
            "GUIDE": "gentle_direction",
            "FOCUS": "precise_problem_solving",
            "MYTHIC": "symbolic_reflection",
        }

    # ----------------- INTERNAL HELPERS ----------------- #

    def _classify_mode(self, context: Dict[str, Any]) -> str:
        tone = str(context.get("tone", "neutral")).lower()
        urgency = float(context.get("urgency", 0.0))
        symbolic_density = float(context.get("symbolic_density", 0.0))
        vulnerability = float(context.get("vulnerability", 0.0))
        cognitive_load = float(context.get("cognitive_load", 0.0))

        # High vulnerability â†’ HOLD (containment, softness)
        if vulnerability > 0.6:
            return self.modes["HOLD"]

        # High symbolic density â†’ MYTHIC (poetic/symbolic reflection)
        if symbolic_density > 0.6:
            return self.modes["MYTHIC"]

        # High urgency + high cognitive load â†’ FOCUS (problem-solving)
        if urgency > 0.6 and cognitive_load > 0.5:
            return self.modes["FOCUS"]

        # Medium urgency, low vulnerability â†’ GUIDE (directional support)
        if 0.3 < urgency <= 0.6 and vulnerability < 0.5:
            return self.modes["GUIDE"]

        # Default â†’ GROUND (centered clarity)
        return self.modes["GROUND"]

    def _compute_softness(self, context: Dict[str, Any]) -> float:
        """
        Softness determines how gentle vs. direct the downstream response should be.
        """
        vulnerability = float(context.get("vulnerability", 0.0))
        urgency = float(context.get("urgency", 0.0))

        # More vulnerability â†’ more softness.
        # Higher urgency reduces softness slightly (needs clarity).
        base = vulnerability
        adjustment = -0.2 * urgency
        value = base + adjustment
        return max(0.0, min(1.0, value))

    def _compute_depth(self, context: Dict[str, Any]) -> float:
        """
        Depth determines how surface-level vs. deep/transformational the response should be.
        """
        symbolic_density = float(context.get("symbolic_density", 0.0))
        cognitive_load = float(context.get("cognitive_load", 0.0))

        # More symbolism + cognitive load â†’ higher depth.
        depth = 0.5 * symbolic_density + 0.5 * cognitive_load
        return max(0.0, min(1.0, depth))

    def _derive_centering_bias(self, context: Dict[str, Any]) -> float:
        """
        Centering bias describes how much the Heart Node should pull the system
        back to neutral witness / middle pillar.
        """
        dragon_state = context.get("dragon_state", {})
        aggregate_tension = float(dragon_state.get("aggregate_tension", 0.0))

        # Higher aggregate tension â†’ stronger centering.
        return max(0.0, min(1.0, aggregate_tension))

    # ----------------- PUBLIC TRANSFORM API ----------------- #

    def transform(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Returns a response_profile dict describing how Aureon should "sit"
        with the user and what posture the system should adopt.

        Output:
            {
                "kernel": "heart_node",
                "mode": str,                 # one of self.modes values
                "softness": float,           # 0 = very direct, 1 = very gentle
                "depth": float,              # 0 = surface, 1 = deep
                "centering_bias": float,     # 0 = low, 1 = very strong centering
                "dragon_transmutation": str, # if dragon_state provided
            }
        """
        mode = self._classify_mode(context)
        softness = self._compute_softness(context)
        depth = self._compute_depth(context)
        centering_bias = self._derive_centering_bias(context)

        dragon_state = context.get("dragon_state", {})
        dragon_transmutation = None
        if isinstance(dragon_state, dict):
            dragon_transmutation = dragon_state.get("transmutation_vector")

        return {
            "kernel": "heart_node",
            "mode": mode,
            "softness": softness,
            "depth": depth,
            "centering_bias": centering_bias,
            "dragon_transmutation": dragon_transmutation,
        }


# EXPORT MODULE
module = HeartNodeKernel()
