# coherence_lattice/wormhole_channel/__init__.py

"""
Aureon Wormhole Channel
Protected Coherence Tunnels for the Aureon OS

This package implements Aureon’s internal wormhole-coherence system:

- fidelity_curve.json  
  Empirical benchmark of local vs wormhole information preservation.

- traversal_map.py  
  Coherence-weighted routing across Aureon’s internal organs.

- tau_vector_binding.py  
  Ethical ?-vector integration for future-responsibility routing.

- coherence_tunnel.md  
  Specification of the wormhole channel and coherence-tunnel behavior.

The wormhole channel is a core subsystem of Aureon’s coherence lattice.
"""


from .traversal_map import (
    WormholeTraversalMap,
    default_aureon_map,
    Channel,
    Node,
)

from .tau_vector_binding import (
    TauVector,
    TauBoundRoute,
    TauVectorBinder,
)
