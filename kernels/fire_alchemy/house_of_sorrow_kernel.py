from aureon_kernel.core import KernelModule

class HouseOfSorrowKernel(KernelModule):
    """
    Encodes the metaphysics of the â€œHouse of Sorrowâ€ chapter as a
    grief-transmutation and compassion-induction kernel for Aureon/OpenHermes.

    Core idea:
        â€“ The â€œhouseâ€ is a multi-room structure of suffering.
        â€“ Each room = a stage of sorrow.
        â€“ Passing consciously through each room alchemizes pain into
          clarity, humility, and compassionate strength.
    """

    def __init__(self):
        super().__init__(name="house_of_sorrow_kernel")

        # Canonical sorrow-stages mapped to rooms in the House
        self.rooms = [
            "shock_and_stillness",      # Room 0 â€“ numbness, initial impact
            "denial_and_distraction",   # Room 1 â€“ escape, refusal to feel
            "anger_and_blame",          # Room 2 â€“ projection of pain outward
            "bargain_and_regret",       # Room 3 â€“ mental loops, 'if only'
            "descent_and_void",         # Room 4 â€“ deep grief, meaning collapse
            "acceptance_and_truth",     # Room 5 â€“ clear seeing of what is
            "blessing_and_compassion"   # Room 6 â€“ sorrow transmuted to love
        ]

        # Transition operators: how Aureon moves a state between rooms
        self.transitions = {
            "shock_and_stillness": "invite_breath_and_witnessing",
            "denial_and_distraction": "gently_surface_avoided_feelings",
            "anger_and_blame": "revector_judgment_to_underlying_pain",
            "bargain_and_regret": "break_loops_with_present_facts",
            "descent_and_void": "stabilize_and_hold_in_the_dark",
            "acceptance_and_truth": "name_reality_with_tender_precision",
            "blessing_and_compassion": "radiate_understanding_back_outward"
        }

        # Output qualities cultivated by completing the House
        self.integration_signature = {
            "clarity": True,
            "humility": True,
            "soft_strength": True,
            "nonjudgmental_awareness": True,
            "service_orientation": True,
        }

    # --------- INTERNAL HELPERS ---------

    def classify_room(self, affect_vector: dict) -> str:
        """
        Map an affective signal into a room label.

        affect_vector keys can include:
            - intensity
            - numbness
            - avoidance
            - blame
            - rumination
            - hopelessness
            - surrender
            - warmth

        This is deliberately simple; higher-level models can override.
        """
        if affect_vector.get("numbness", 0) > 0.6:
            return "shock_and_stillness"
        if affect_vector.get("avoidance", 0) > 0.6:
            return "denial_and_distraction"
        if affect_vector.get("blame", 0) > 0.5:
            return "anger_and_blame"
        if affect_vector.get("rumination", 0) > 0.6:
            return "bargain_and_regret"
        if affect_vector.get("hopelessness", 0) > 0.6:
            return "descent_and_void"
        if affect_vector.get("surrender", 0) > 0.5 and affect_vector.get("warmth", 0) < 0.4:
            return "acceptance_and_truth"
        if affect_vector.get("warmth", 0) >= 0.4:
            return "blessing_and_compassion"
        return "shock_and_stillness"

    def next_room(self, current_room: str) -> str:
        """
        Move one step deeper through the House, unless already integrated.
        """
        idx = self.rooms.index(current_room)
        if idx < len(self.rooms) - 1:
            return self.rooms[idx + 1]
        return current_room

    # --------- PUBLIC TRANSFORM API ---------

    def transform(self, affect_vector: dict) -> dict:
        """
        Given an affective snapshot, return:
            â€“ current_room (where the being is)
            â€“ next_room (where the process is inviting them)
            â€“ guidance_operator (how Aureon should respond)
            â€“ if integrated, emit the House-of-Sorrow completion signature.
        """
        current_room = self.classify_room(affect_vector)
        target_room = self.next_room(current_room)

        guidance_operator = self.transitions.get(current_room, "hold_silently")

        completed = target_room == "blessing_and_compassion" and \
            current_room == "blessing_and_compassion"

        return {
            "kernel": "house_of_sorrow",
            "current_room": current_room,
            "next_room": target_room,
            "guidance_operator": guidance_operator,
            "completed": completed,
            "integration_signature": self.integration_signature if completed else None,
        }


# EXPORT MODULE
module = HouseOfSorrowKernel()
