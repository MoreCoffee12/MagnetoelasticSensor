"""
anhyst_iso_test.py

Pytest test harness for anhysteretic_magnetization() of an isotropic material.

References
----------
[1] 	D. Jiles and D. Atherton, "Ferromagnetic hysteresis," in IEEE Transactions 
        on Magnetics, vol. 19, no. 5, pp. 2183-2185, September 1983, 
        doi: 10.1109/TMAG.1983.1062594.
[2]  	Jiles, D. C., and D. L. Atherton. "Theory of Ferromagnetic Hysteresis." 
        Journal of Magnetism and Magnetic Materials, vol. 61, nos. 1\[Dash]2, 
        1986, pp. 48\[Dash]60.
"""

from __future__ import annotations

import numpy as np
import pytest

from magnetoelasticsensor.anhyst_iso import (
    anhysteretic_magnetization,
    anhysteretic_magnetization_deriv,
    anhysteretic_magnetization_differential,
)
from magnetoelasticsensor.ja_props import JAProps


def test_returns_zero_at_zero_effective_field() -> None:
    """
    When H + alpha*M = 0, the Langevin function tends to zero, so
    Man should be zero.
    """
    result = anhysteretic_magnetization(
        h=0.0,
        m=0.0,
        props=JAProps(ms=1.6, a=10.0, alpha=0.02),
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
        props=JAProps(ms=ms, a=a, alpha=alpha),
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
        props=JAProps(ms=ms, a=a, alpha=0.0),
    )
    neg = anhysteretic_magnetization(
        h=-75.0,
        m=0.0,
        props=JAProps(ms=ms, a=a, alpha=0.0),
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
        props=JAProps(ms=ms, a=10.0, alpha=0.0),
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
        props=JAProps(ms=ms, a=10.0, alpha=0.0),
    )

    assert np.isclose(result, -ms, rtol=0.0, atol=1e-4)


def test_validate_figure03_ref02_m0() -> None:
    """
    Test case for the value in Fig (3) in [2]. Validation number
    from the companian Mathematia notebook.
    """

    # Saturation magnetization is 1.6e6 A/m
    ms = 1.6e6

    # Internal magnetic field, A/m
    h = 300

    # Bulk magnetization, A/m
    m = 0.0

    # Anhysteretic magnetization shape parameter, A/m
    a = 1100

    # mean field parameter, -
    alpha = 0.0016

    # Excecute the test case
    man = anhysteretic_magnetization(
        h=h,
        m=m,
        props=JAProps(ms=ms, a=a, alpha=alpha),
    )

    # Expected value
    man_expected = 144738.3548215022

    # Perform the assert to close out the test case
    assert np.isclose(man, man_expected, rtol=0.0, atol=1e-4)

def test_validate_figure03_ref02_m50000() -> None:
    """
    Test case for the value in Fig (3) in [2]. Validation number
    from the companian Mathematia notebook, M = 50000 A/m.
    """

    # Saturation magnetization is 1.6e6 A/m
    ms = 1.6e6

    # Internal magnetic field, A/m
    h = 300

    # Bulk magnetization, A/m
    m = 50000.0

    # Anhysteretic magnetization shape parameter, A/m
    a = 1100

    # mean field parameter, -
    alpha = 0.0016

    # Excecute the test case
    man = anhysteretic_magnetization(
        h=h,
        m=m,
        props=JAProps(ms=ms, a=a, alpha=alpha),
    )

    # Expected value
    man_expected = 182793.0691901564

    # Perform the assert to close out the test case
    assert np.isclose(man, man_expected, rtol=0.0, atol=1e-4)

def test_supports_numpy_arrays() -> None:
    """
    Verify vectorized operation with NumPy arrays.
    """
    h = np.array([-100.0, 0.0, 100.0])
    m = np.zeros_like(h)

    result = anhysteretic_magnetization(
        h=h,
        m=m,
        props=JAProps(ms=2.0, a=20.0, alpha=0.0),
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
            props=JAProps(ms=1.0, a=0.0, alpha=0.01),
        )


class TestAnhystereticDifferential:
    """Test harness for the analytical differential of the anhysteretic curve."""

    def test_matches_closed_form_away_from_zero(self) -> None:
        """
        Away from the origin, validate the helper against the exact closed form:

            dMan/dH = Ms * (a / H_eff^2 - csch(H_eff/a)^2 / a)
        """
        h = 125.0
        m = 30.0
        ms = 1.7
        a = 14.0
        alpha = 0.02

        h_eff = h + alpha * m
        expected = ms * (
            a / h_eff**2 - 1.0 / (a * np.sinh(h_eff / a) ** 2)
        )

        result = anhysteretic_magnetization_differential(
            h=h,
            m=m,
            props=JAProps(ms=ms, a=a, alpha=alpha),
        )

        assert np.isclose(result, expected, rtol=1e-12, atol=1e-12)

    def test_matches_origin_limit(self) -> None:
        """At H + alpha*M = 0, the analytical differential tends to Ms / (3a)."""
        ms = 1.6e6
        a = 1100.0

        result = anhysteretic_magnetization_differential(
            h=0.0,
            m=0.0,
            props=JAProps(ms=ms, a=a, alpha=0.0016),
        )

        assert np.isclose(result, ms / (3.0 * a), rtol=1e-9)

    def test_matches_central_difference_of_anhysteretic_curve(self) -> None:
        """The analytical helper should agree with a central-difference check."""
        h = 250.0
        m = 20.0
        ms = 1.9
        a = 18.0
        alpha = 0.015
        step = 1.0e-6

        analytical = anhysteretic_magnetization_differential(
            h=h,
            m=m,
            props=JAProps(ms=ms, a=a, alpha=alpha),
        )
        forward = anhysteretic_magnetization(
            h=h + step,
            m=m,
            props=JAProps(ms=ms, a=a, alpha=alpha),
        )
        backward = anhysteretic_magnetization(
            h=h - step,
            m=m,
            props=JAProps(ms=ms, a=a, alpha=alpha),
        )
        numerical = (forward - backward) / (2.0 * step)

        assert np.isclose(analytical, numerical, rtol=1e-7, atol=1e-9)

    def test_legacy_derivative_wrapper_matches_analytical_helper(self) -> None:
        """The existing derivative API should remain equivalent after the refactor."""
        h = np.array([-300.0, 0.0, 300.0])
        m = np.array([50.0, 0.0, -50.0])

        analytical = anhysteretic_magnetization_differential(
            h=h,
            m=m,
            props=JAProps(ms=1.6e6, a=1100.0, alpha=0.0016),
        )
        legacy = anhysteretic_magnetization_deriv(
            h=h,
            m=m,
            props=JAProps(ms=1.6e6, a=1100.0, alpha=0.0016),
        )

        assert np.allclose(analytical, legacy, rtol=1e-12, atol=1e-12)

    def test_validate_figure03_ref02_M0(self) -> None:
        """
        Test case for the value in Fig (3) in [2]. Validation number
        from the companian Mathematia notebook. In this case, the bulk
        magnetization is clamped to zero.
        """

        # Saturation magnetization is 1.6e6 A/m
        ms = 1.6e6

        # Internal magnetic field, A/m
        h = 300

        # Bulk magnetization, A/m
        m = 0.0

        # Anhysteretic magnetization shape parameter, A/m
        a = 1100

        # mean field parameter, -
        alpha = 0.0016

        # Excecute the test case
        man = anhysteretic_magnetization_differential(
            h=h,
            m=m,
            props=JAProps(ms=ms, a=a, alpha=alpha),
        )

        # Expected value from the companion Mathematica notebook
        man_expected = 477.7201394344288000000

        # Perform the assert to close out the test case
        assert np.isclose(man, man_expected, rtol=0.0, atol=1e-10)

    def test_raises_error_when_a_is_zero(self) -> None:
        """The analytical differential must reject a zero shape parameter."""
        with pytest.raises(ValueError, match="must be nonzero"):
            anhysteretic_magnetization_differential(
                h=10.0,
                m=1.0,
                props=JAProps(ms=1.0, a=0.0, alpha=0.01),
            )