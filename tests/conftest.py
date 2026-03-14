"""
conftest.py
-----------
Shared pytest fixtures and configuration for mechanicsdsl-notebooks tests.
"""
import pytest
from pathlib import Path


@pytest.fixture(scope="session")
def notebooks_dir():
    return Path(__file__).parent.parent / "notebooks"


@pytest.fixture(scope="session")
def all_notebooks(notebooks_dir):
    return sorted(notebooks_dir.glob("*.ipynb"))


@pytest.fixture(scope="session")
def docs_dir():
    return Path(__file__).parent.parent / "docs"
