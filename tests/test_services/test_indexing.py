# tests/test_services/test_indexing.py
import pytest
import numpy as np
from app.services.indexing.brute_force import BruteForceIndex

def test_brute_force_index_creation():
    index = BruteForceIndex()
    assert len(index.vectors) == 0
    assert len(index.ids) == 0

def test_brute_force_index_add():
    index = BruteForceIndex()
    index.add([1.0, 2.0, 3.0], 1)
    assert len(index.vectors) == 1
    assert len(index.ids) == 1
    assert np.array_equal(index.vectors[0], np.array([1.0, 2.0, 3.0]))
    assert index.ids[0] == 1

def test_brute_force_index_search():
    index = BruteForceIndex()
    index.add([1.0, 2.0, 3.0], 1)
    index.add([4.0, 5.0, 6.0], 2)
    index.add([7.0, 8.0, 9.0], 3)

    results = index.search([1.0, 2.0, 3.0], k=2)
    assert len(results) == 2
    assert results[0][0] == 1  # First result should be the exact match
    assert results[0][1] == 0.0  # Distance should be 0 for exact match
    assert results[1][0] in [2, 3]  # Second result should be one of the other vectors

def test_brute_force_index_search_with_more_results_than_vectors():
    index = BruteForceIndex()
    index.add([1.0, 2.0, 3.0], 1)
    index.add([4.0, 5.0, 6.0], 2)

    results = index.search([1.0, 2.0, 3.0], k=3)
    assert len(results) == 2  # Should only return 2 results even though k=3

def test_brute_force_index_search_empty_index():
    index = BruteForceIndex()
    results = index.search([1.0, 2.0, 3.0], k=1)
    assert len(results) == 0