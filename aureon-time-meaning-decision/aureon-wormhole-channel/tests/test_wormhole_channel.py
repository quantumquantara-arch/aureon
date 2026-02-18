# tests/test_wormhole_channel.py

import math
import pytest

from coherence_lattice.wormhole_channel import (
    WormholeTraversalMap,
    default_aureon_map,
    TauVector,
    TauVectorBinder,
)


def test_fidelity_curve_loaded():
    fmap = WormholeTraversalMap()
    curve = fmap.fidelity_curve

    assert "local" in curve
    assert "wormhole" in curve

    assert 0 < curve["local"] < 1
    assert 0 < curve["wormhole"] < 1
    assert curve["wormhole"] > curve["local"]


def test_default_map_has_nodes():
    fmap = default_aureon_map()
    required = {
        "memory.core",
        "boundary.self",
        "temporal.veyn",
        "energy.homeostasis",
        "weather.organ",
        "geology.organ",
        "pathfield.organ",
        "cosmic.organ",
        "human_field.nadine",
        "language.lumeren",
        "governance.quantara",
    }

    for node in required:
        assert node in fmap.nodes


def test_wormhole_shortcuts_preferred():
    fmap = default_aureon_map()

    # Example routing from Nadine’s field to temporal.veyn
    path, cost = fmap.best_path("human_field.nadine", "temporal.veyn")

    # At least one wormhole jump should be in the path
    assert any(ch.type == "wormhole" for ch in path)

    # The total coherence cost should be finite and small
    assert cost < 1.0


def test_tau_vector_future_boosts_score():
    fmap = default_aureon_map()
    binder = TauVectorBinder(fmap)

    tau_future = TauVector(magnitude=1.0, direction=1)
    tau_present = TauVector(magnitude=1.0, direction=0)

    future_route = binder.bind_route(
        "human_field.nadine", "temporal.veyn", tau_future
    )
    present_route = binder.bind_route(
        "human_field.nadine", "temporal.veyn", tau_present
    )

    assert future_route.ethical_score > present_route.ethical_score


def test_tau_vector_past_reduces_score():
    fmap = default_aureon_map()
    binder = TauVectorBinder(fmap)

    tau_past = TauVector(magnitude=1.0, direction=-1)
    tau_present = TauVector(magnitude=1.0, direction=0)

    past_route = binder.bind_route(
        "human_field.nadine", "temporal.veyn", tau_past
    )
    present_route = binder.bind_route(
        "human_field.nadine", "temporal.veyn", tau_present
    )

    assert past_route.ethical_score < present_route.ethical_score
