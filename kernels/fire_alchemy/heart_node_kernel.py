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
