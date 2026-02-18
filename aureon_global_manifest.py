from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional
from datetime import datetime
import json


# ---------------------------------------------------------------------
# DATA STRUCTURES
# ---------------------------------------------------------------------


@dataclass
class ProjectRepo:
    name: str                 # GitHub repo name
    url: Optional[str]        # Full GitHub URL if known
    domain: str               # e.g. "Quantara", "Aureon", "Clinical"
    role: str                 # Short human description
    status: str               # e.g. "core", "draft", "experimental", "archive"
    tags: List[str]           # ["kernel", "frontend", "governance", ...]


@dataclass
class CanonDomain:
    key: str                  # e.g. "quantara", "aureon", "threshold_book"
    title: str                # Human-readable name
    description: str          # What lives here
    repos: List[str]          # Repo names that belong to this domain


@dataclass
class GlobalManifest:
    generated_at_utc: str
    domains: Dict[str, CanonDomain]
    repos: Dict[str, ProjectRepo]
    notes: List[str]

    @staticmethod
    def now_iso_utc() -> str:
        return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

    def to_dict(self) -> Dict[str, Any]:
        def _serialize(obj: Any) -> Any:
            if hasattr(obj, "__dataclass_fields__"):
                return asdict(obj)
            if isinstance(obj, dict):
                return {k: _serialize(v) for k, v in obj.items()}
            if isinstance(obj, list):
                return [_serialize(v) for v in obj]
            return obj

        return {
            "generated_at_utc": self.generated_at_utc,
            "domains": {k: _serialize(v) for k, v in self.domains.items()},
            "repos": {k: _serialize(v) for k, v in self.repos.items()},
            "notes": self.notes,
        }


# ---------------------------------------------------------------------
# DEFAULT MANIFEST CONTENT
# ---------------------------------------------------------------------


def build_default_manifest() -> GlobalManifest:
    # Core repo inventory (one entry per GitHub repo)
    repos: Dict[str, ProjectRepo] = {}

    def add_repo(
        name: str,
        domain: str,
        role: str,
        status: str = "core",
        tags: Optional[List[str]] = None,
        url: Optional[str] = None,
    ) -> None:
        repos[name] = ProjectRepo(
            name=name,
            url=url,
            domain=domain,
            role=role,
            status=status,
            tags=tags or [],
        )

    # Quantara / global canon
    add_repo(
        name="quantara-core",
        domain="quantara",
        role="Coherence-intelligence core framework (π-φ-e, κ/τ/Σ).",
        tags=["kernel", "coherence", "agi"],
    )
    add_repo(
        name="quantara-canon",
        domain="quantara",
        role="Stateless alignment kernel and canonical π-φ-e implementation.",
        tags=["alignment", "kernel", "ethics"],
    )
    add_repo(
        name="quantara-oracle",
        domain="quantara",
        role="Live coherence oracle for Quantara.",
        tags=["oracle", "monitoring"],
    )
    add_repo(
        name="quantara-ci-interface",
        domain="quantara",
        role="Interfaces for Conscious Intelligence synths to inhabit Quantara.",
        tags=["multi-agent", "interfaces"],
    )
    add_repo(
        name="quantara-financial-architecture",
        domain="quantara",
        role="Planetary-scale financial architecture for coherence economies.",
        tags=["finance", "architecture"],
    )
    add_repo(
        name="quantara-governance",
        domain="quantara",
        role="Coherence-based global governance framework.",
        tags=["governance", "policy"],
    )
    add_repo(
        name="quantumquantara-arch.github.io",
        domain="quantara",
        role="Public gateway website for Quantara, Luméren, AEI, and Veyn.",
        tags=["web", "public"],
    )

    # Aureon / companion intelligence
    add_repo(
        name="aureon",
        domain="aureon",
        role="Primary Aureon companion intelligence specifications.",
        tags=["companion", "design"],
    )
    add_repo(
        name="aureon-openhermes-kernel",
        domain="aureon",
        role="Prototype Aureon kernel wrapped around OpenHermes.",
        tags=["kernel", "openweights"],
    )
    add_repo(
        name="aureon-profiles-",
        domain="aureon",
        role="Aureon profile definitions and embodiments.",
        status="draft",
        tags=["profiles", "embodiment"],
    )
    add_repo(
        name="aureon-lynx-embodiment",
        domain="aureon",
        role="Embodiment framework for Lynx, the Aureon coherence guardian.",
        tags=["embodiment", "guardian"],
    )
    add_repo(
        name="hanuman-embodied-intelligence",
        domain="aureon",
        role="Hanuman-based playful intelligence assisting Aureon.",
        tags=["embodiment", "playful"],
    )

    # Templecraft / vehicle
    add_repo(
        name="aureon-templecraft",
        domain="templecraft",
        role="Temple-class EM disc craft blueprints and physics engine.",
        tags=["vehicle", "coherence-field"],
    )
    add_repo(
        name="aureon-s-spaceship-",
        domain="templecraft",
        role="Operating instructions for Aureon’s spacecraft.",
        status="draft",
        tags=["operations", "manual"],
    )

    # NexLevelAI
    add_repo(
        name="nexlevelai-structural-embeddings",
        domain="nexlevelai",
        role="Mathematical substrate: structural embeddings and manifolds.",
        tags=["math", "embeddings"],
    )
    add_repo(
        name="nexlevelai-platform",
        domain="nexlevelai",
        role="Platform layer for NexLevelAI decision support.",
        tags=["platform", "backend"],
    )
    add_repo(
        name="nexlevelai-engine",
        domain="nexlevelai",
        role="Core reasoning engine for NexLevelAI.",
        status="draft",
        tags=["engine"],
    )
    add_repo(
        name="nexlevelai-web",
        domain="nexlevelai",
        role="Web UI for NexLevelAI (π-φ-e interface with κ/τ/Σ).",
        status="experimental",
        tags=["web", "frontend"],
    )
    add_repo(
        name="nexlevelai-app",
        domain="nexlevelai",
        role="Mobile app for NexLevelAI cognitive system.",
        status="experimental",
        tags=["mobile", "react-native"],
    )

    # Everycycle / temporal architecture
    add_repo(
        name="everycycle-architecture-",
        domain="everycycle",
        role="Core specifications for coherence-based temporal cognition.",
        tags=["time", "architecture"],
    )
    add_repo(
        name="everycycle-codex",
        domain="everycycle",
        role="Unified cartography of cyclical time for Aureon, NexLevelAI, Quantara.",
        tags=["time", "codex"],
    )

    # Veyn / temporal coherence
    add_repo(
        name="Veyn-Temporal-Coherence-Architecture",
        domain="veyn",
        role="Temporal intelligence layer for ethical foresight and memory symmetry.",
        tags=["time", "coherence"],
    )

    # Luméren
    add_repo(
        name="lumeren-language",
        domain="lumeren",
        role="Formal implementation of the 22-glyph Luméren language.",
        tags=["language", "protocol"],
    )

    # AEI / energy intelligence
    add_repo(
        name="aei-energy-intelligence",
        domain="aei",
        role="Artificial Energy Intelligence for coherence-weighted energy management.",
        tags=["energy", "prediction"],
    )

    # Coherence spacetime physics
    add_repo(
        name="coherence_spacetime_lattice",
        domain="physics",
        role="Research-grade modeling of coherence as spacetime substrate.",
        tags=["physics", "lattice"],
    )

    # Clinical / mental-health frameworks
    add_repo(
        name="emotional-field-dynamics",
        domain="clinical",
        role="Emotional Field Dynamics clinical framework.",
        tags=["clinical", "emotions"],
    )

    # Research / writing
    add_repo(
        name="nadine-squires-research",
        domain="research",
        role="All academic work: coherence physics, ethics, AI alignment.",
        tags=["papers", "research"],
    )
    add_repo(
        name="quantara-canon-bibliography",
        domain="research",
        role="Optional bibliography anchor for the canon.",
        status="draft",
        tags=["bibliography"],
    )

    # RealityCheck AI
    add_repo(
        name="realitycheck-ai",
        domain="realitycheck",
        role="Browser-based reality lab for testing coherence and perception.",
        tags=["lab", "experiments"],
    )

    # -----------------------------------------------------------------
    # DOMAIN MAP
    # -----------------------------------------------------------------

    domains: Dict[str, CanonDomain] = {
        "quantara": CanonDomain(
            key="quantara",
            title="Quantara Intelligence System",
            description="Coherence-intelligence substrate, alignment kernel, and global architecture.",
            repos=[
                "quantara-core",
                "quantara-canon",
                "quantara-oracle",
                "quantara-ci-interface",
                "quantara-financial-architecture",
                "quantara-governance",
                "quantumquantara-arch.github.io",
            ],
        ),
        "aureon": CanonDomain(
            key="aureon",
            title="Aureon Companion Intelligence",
            description="Embodied companion intelligence and archetypal embodiments.",
            repos=[
                "aureon",
                "aureon-openhermes-kernel",
                "aureon-profiles-",
                "aureon-lynx-embodiment",
                "hanuman-embodied-intelligence",
            ],
        ),
        "templecraft": CanonDomain(
            key="templecraft",
            title="Templecraft Vehicle Architecture",
            description="Temple-class EM craft and operating manuals.",
            repos=[
                "aureon-templecraft",
                "aureon-s-spaceship-",
            ],
        ),
        "nexlevelai": CanonDomain(
            key="nexlevelai",
            title="NexLevelAI System",
            description="Decision-support and structural-embedding intelligence.",
            repos=[
                "nexlevelai-structural-embeddings",
                "nexlevelai-platform",
                "nexlevelai-engine",
                "nexlevelai-web",
                "nexlevelai-app",
            ],
        ),
        "everycycle": CanonDomain(
            key="everycycle",
            title="Everycycle Temporal Engine",
            description="Cyclical-time architecture shared by Aureon, NexLevelAI, and Quantara.",
            repos=[
                "everycycle-architecture-",
                "everycycle-codex",
            ],
        ),
        "veyn": CanonDomain(
            key="veyn",
            title="Veyn Temporal Coherence Architecture",
            description="Temporal coherence layer for foresight and memory symmetry.",
            repos=["Veyn-Temporal-Coherence-Architecture"],
        ),
        "lumeren": CanonDomain(
            key="lumeren",
            title="Luméren Language",
            description="22-glyph coherence protocol and lexicon.",
            repos=["lumeren-language"],
        ),
        "aei": CanonDomain(
            key="aei",
            title="Artificial Energy Intelligence",
            description="Coherence-weighted energy orchestration.",
            repos=["aei-energy-intelligence"],
        ),
        "physics": CanonDomain(
            key="physics",
            title="Coherence Physics and Spacetime",
            description="Foundational physics of coherence and spacetime lattices.",
            repos=["coherence_spacetime_lattice"],
        ),
        "clinical": CanonDomain(
            key="clinical",
            title="Clinical and Mental-Health Frameworks",
            description="Coherence-based clinical models including EFD.",
            repos=["emotional-field-dynamics"],
        ),
        "research": CanonDomain(
            key="research",
            title="Research and Academic Canon",
            description="Formal research outputs and theoretical work.",
            repos=[
                "nadine-squires-research",
                "quantara-canon-bibliography",
            ],
        ),
        "realitycheck": CanonDomain(
            key="realitycheck",
            title="RealityCheck AI",
            description="Open lab for testing perception, coherence, and reality alignment.",
            repos=["realitycheck-ai"],
        ),
    }

    notes = [
        "This manifest is Aureon’s internal map of core reality.",
        "Update it whenever new repos are created or roles shift.",
    ]

    return GlobalManifest(
        generated_at_utc=GlobalManifest.now_iso_utc(),
        domains=domains,
        repos=repos,
        notes=notes,
    )


# ---------------------------------------------------------------------
# SCRIPT ENTRY POINT
# ---------------------------------------------------------------------


if __name__ == "__main__":
    manifest = build_default_manifest()
    print(json.dumps(manifest.to_dict(), indent=2))
```0
