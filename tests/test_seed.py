import pytest
from src.seed import seed


def test_seed_is_envokeable():
    assert callable(seed)
