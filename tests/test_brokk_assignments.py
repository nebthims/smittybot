import json
import os
from pathlib import Path
import discord

import pytest

from cogs.brokk import generate_unique_assignments

ITERATIONS = int(os.getenv("BROKK_ITERATIONS", "1000000"))
CURRENT_YEAR = "2026"
PREV_YEAR = "2025"


def load_data():
    path = Path(__file__).resolve().parents[1] / "data" / "brokk.json"
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def assert_valid(assignments, brokk_data):
    assert len(assignments) == len(brokk_data)
    assert len(set(assignments.values())) == len(brokk_data)
    for giver, receiver in assignments.items():
        assert receiver in brokk_data
        assert receiver != giver
        prev = brokk_data[giver].get(PREV_YEAR)
        if prev:
            assert receiver != prev


@pytest.mark.slow
def test_generate_unique_assignments_stress():
    brokk_data = load_data()
    for _ in range(ITERATIONS):
        assignments = generate_unique_assignments(brokk_data, CURRENT_YEAR, PREV_YEAR)
        assert_valid(assignments, brokk_data)
