"""
anhyst_iso_test.py

Pytest test harness for anhysteretic_magnetization() of an isotropic material.
"""

from __future__ import annotations

import numpy as np
import pytest

from magnetoelasticsensor.anhyst_iso import anhysteretic_magnetization


def test_returns_zero_at_zero_effective_field() -> None:
    """
    When H + alpha*M = 0, the Langevin function tends to zero, so
    Man should be zero.
    """
    result = anhysteretic_magnetization(
        h=0.0,
        m=0.0,
        ms=1.6,
        a=10.0,
        alpha=0.02,
    )

    assert np.isclose(result, 0.0, atol=1e-12)


def test_matches_direct_formula_away_from_zero() -> None:
    """
    For values away from zero, compare against the direct closed-form
    expression.
    """
    h = 100.0
    m = 20.0
    ms = 1.5
    a = 12.0
    alpha = 0.01

    x = (h + alpha * m) / a
    expected = ms * (1.0 / np.tanh(x) - 1.0 / x)

    result = anhysteretic_magnetization(
        h=h,
        m=m,
        ms=ms,
        a=a,
        alpha=alpha,
    )

    assert np.isclose(result, expected, rtol=1e-12, atol=1e-12)


def test_odd_symmetry_when_m_is_zero_and_alpha_is_zero() -> None:
    """
    The anhysteretic function is odd in H when alpha = 0 and m = 0:
        Man(-H) = -Man(H)
    """
    ms = 2.0
    a = 15.0

    pos = anhysteretic_magnetization(
        h=75.0,
        m=0.0,
        ms=ms,
        a=a,
        alpha=0.0,
    )
    neg = anhysteretic_magnetization(
        h=-75.0,
        m=0.0,
        ms=ms,
        a=a,
        alpha=0.0,
    )

    assert np.isclose(neg, -pos, rtol=1e-12, atol=1e-12)


def test_saturates_toward_ms_for_large_positive_field() -> None:
    """
    For very large positive effective field, the Langevin function tends
    toward +1, so Man should approach +Ms.
    """
    ms = 1.8
    result = anhysteretic_magnetization(
        h=1.0e6,
        m=0.0,
        ms=ms,
        a=10.0,
        alpha=0.0,
    )

    assert np.isclose(result, ms, rtol=0.0, atol=1e-4)


def test_saturates_toward_negative_ms_for_large_negative_field() -> None:
    """
    For very large negative effective field, the Langevin function tends
    toward -1, so Man should approach -Ms.
    """
    ms = 1.8
    result = anhysteretic_magnetization(
        h=-1.0e6,
        m=0.0,
        ms=ms,
        a=10.0,
        alpha=0.0,
    )

    assert np.isclose(result, -ms, rtol=0.0, atol=1e-4)


def test_supports_numpy_arrays() -> None:
    """
    Verify vectorized operation with NumPy arrays.
    """
    h = np.array([-100.0, 0.0, 100.0])
    m = np.zeros_like(h)

    result = anhysteretic_magnetization(
        h=h,
        m=m,
        ms=2.0,
        a=20.0,
        alpha=0.0,
    )

    assert isinstance(result, np.ndarray)
    assert result.shape == h.shape
    assert np.isclose(result[1], 0.0, atol=1e-12)
    assert result[0] < 0.0
    assert result[2] > 0.0


def test_raises_error_when_a_is_zero() -> None:
    """
    Parameter `a` must be nonzero.
    """
    with pytest.raises(ValueError, match="must be nonzero"):
        anhysteretic_magnetization(
            h=10.0,
            m=1.0,
            ms=1.0,
            a=0.0,
            alpha=0.01,
        )