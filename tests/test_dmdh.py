"""
test_dmdh.py

Pytest test harness for ``dmdh()`` — the dM/dH right-hand side of the
isotropic Jiles-Atherton hysteresis model (Equation 34 of [1]).

References
----------
[1] Jiles D. C., Atherton D. "Theory of ferromagnetic hysteresis."
    Journal of Magnetism and Magnetic Materials, 61 (1986) 48.
[2] Chwastek K., Szczyglowski J. "Identification of a hysteresis model
    parameters with genetic algorithms." Mathematics and Computers in
    Simulation, 71 (2006) 206.
"""

from __future__ import annotations

import numpy as np
import pytest

from magnetoelasticsensor.anhyst_iso import anhysteretic_magnetization_deriv
from magnetoelasticsensor.dmdh import dmdh

# ---------------------------------------------------------------------------
# Shared parameter set — matches the Mathematica companion-notebook values
# used in the anhyst_iso tests (ref [2] Fig. 3 parameters).
# ---------------------------------------------------------------------------
_A = 1100.0        # domain density / anhysteretic shape, A/m
_K = 500.0         # pinning energy, A/m
_C = 0.1           # magnetization reversibility, -
_MS = 1.6e6        # saturation magnetization, A/m
_ALPHA = 0.0016    # mean-field coupling, -


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _call(h, m, h_start=-1000.0, h_end=1000.0, **overrides):
    """Call dmdh with the shared parameter set, optionally overriding params."""
    params = dict(a=_A, k=_K, c=_C, ms=_MS, alpha=_ALPHA)
    params.update(overrides)
    return dmdh(h=h, m=m, h_start=h_start, h_end=h_end, **params)


# ===========================================================================
# At the origin (H=0, M=0)
# ===========================================================================

class TestAtOrigin:
    """
    At H=0, M=0 the effective field is zero, so Man=0 and the irreversible
    numerator (Man-M) = 0 regardless of sweep direction.

    The only contribution is the reversible term:
        dM/dH = c/(1+c) * (ms/a) * L'(0) = c/(1+c) * ms/(3a)
    """

    def _expected_dm3(self, a=_A, c=_C, ms=_MS):
        return (c / (1.0 + c)) * ms / (3.0 * a)

    def test_increasing_field(self):
        """dM/dH at origin, field increasing."""
        result = _call(h=0.0, m=0.0, h_start=-1000.0, h_end=1000.0)
        assert np.isclose(result, self._expected_dm3(), rtol=1e-9)

    def test_decreasing_field(self):
        """dM/dH at origin, field decreasing — same value by symmetry."""
        result = _call(h=0.0, m=0.0, h_start=1000.0, h_end=-1000.0)
        assert np.isclose(result, self._expected_dm3(), rtol=1e-9)

    def test_matches_figure03_ref01_parameters(self):
        """
        Validate against the companion Mathematica notebook parameter set.
        At H=0, M=0:  dM/dH = c*ms / (3*a*(1+c))
        = 0.1 * 1.6e6 / (3 * 1100 * 1.1) = 160000 / 3630 ≈ 44.077...
        """
        expected = 0.1 * 1.6e6 / (3.0 * 1100.0 * 1.1)
        result = _call(h=0.0, m=0.0)
        assert np.isclose(result, expected, rtol=1e-10)


# ===========================================================================
# Equilibrium: M already equals Man
# ===========================================================================

class TestAtEquilibrium:
    """
    When M == Man, the irreversible term (Man-M) is zero, so dM/dH equals
    only the reversible contribution dm3.

    Using alpha=0 makes Man independent of M (Man = ms*L(H/a)), so the
    equilibrium point M = Man(H) is trivially well-defined without a
    fixed-point iteration.
    """

    def test_irreversible_term_vanishes_at_man(self):
        """dM/dH = dm3 when M is exactly on the anhysteretic curve."""
        from magnetoelasticsensor.anhyst_iso import anhysteretic_magnetization
        h = 300.0
        # With alpha=0, Man(H) = ms*L(H/a) is independent of M
        m_man = float(
            anhysteretic_magnetization(h=h, m=0.0, ms=_MS, a=_A, alpha=0.0)
        )

        expected_dm3 = (
            (_C / (1.0 + _C))
            * anhysteretic_magnetization_deriv(
                h=h, m=m_man, ms=_MS, a=_A, alpha=0.0
            )
        )
        result = dmdh(
            h=h, m=m_man,
            a=_A, k=_K, c=_C, ms=_MS, alpha=0.0,
            h_start=-1000.0, h_end=1000.0,
        )
        assert np.isclose(result, expected_dm3, rtol=1e-9)


# ===========================================================================
# Physical realizability clipping
# ===========================================================================

class TestIrreversibleClipping:
    """
    The irreversible numerator (Man-M) must be clipped to zero when the
    magnetization overshoots the anhysteretic curve in a way that violates
    the sweep direction.
    """

    def test_clip_to_zero_when_m_above_man_increasing_field(self):
        """
        When H is increasing and M > Man, the irreversible term is clipped
        to zero.  The result should equal only the reversible dm3.

        Setup: H=0, alpha=0 → Man=0 by symmetry.  Set M=1000 > 0 = Man.
        """
        h, m = 0.0, 1000.0
        a, k, c, ms, alpha = 10.0, 100.0, 0.1, 1.6e6, 0.0

        expected_dm3 = (c / (1.0 + c)) * anhysteretic_magnetization_deriv(
            h=h, m=m, ms=ms, a=a, alpha=alpha
        )
        result = dmdh(
            h=h, m=m, a=a, k=k, c=c, ms=ms, alpha=alpha,
            h_start=-1000.0, h_end=1000.0,
        )
        assert np.isclose(result, expected_dm3, rtol=1e-9)

    def test_clip_to_zero_when_m_below_man_decreasing_field(self):
        """
        When H is decreasing and M < Man, the irreversible term is clipped
        to zero.  The result should equal only the reversible dm3.

        Setup: H=0, alpha=0 → Man=0.  Set M=-1000 < 0 = Man.
        """
        h, m = 0.0, -1000.0
        a, k, c, ms, alpha = 10.0, 100.0, 0.1, 1.6e6, 0.0

        expected_dm3 = (c / (1.0 + c)) * anhysteretic_magnetization_deriv(
            h=h, m=m, ms=ms, a=a, alpha=alpha
        )
        result = dmdh(
            h=h, m=m, a=a, k=k, c=c, ms=ms, alpha=alpha,
            h_start=1000.0, h_end=-1000.0,
        )
        assert np.isclose(result, expected_dm3, rtol=1e-9)

    def test_positive_dmdh_when_m_below_man_increasing(self):
        """
        Physical case: H increasing, M < Man → irreversible term is positive
        and the total dM/dH > 0.
        """
        # H is moderate, M=0 so Man > M for positive H
        result = _call(h=300.0, m=0.0, h_start=0.0, h_end=5000.0)
        assert result > 0.0

    def test_dmdh_positive_when_m_above_man_decreasing(self):
        """
        Physical case: H decreasing, M > Man.

        dM/dH is always ≥ 0 in the J-A model: M and H always change in the
        same direction (both decrease together on the upper branch).  The
        irreversible numerator (Man-M < 0) divided by the negative denominator
        (δk < 0 for δ=-1) yields a *positive* quotient, so dM/dH > 0.

        Use H=0, alpha=0 → Man=0; set M=1e5 > 0, decreasing sweep.
        """
        h, m = 0.0, 1.0e5
        a, k, c, ms, alpha = 10.0, 100.0, 0.0, 1.6e6, 0.0
        result = dmdh(
            h=h, m=m, a=a, k=k, c=c, ms=ms, alpha=alpha,
            h_start=5000.0, h_end=-5000.0,
        )
        assert result > 0.0


# ===========================================================================
# Input validation
# ===========================================================================

class TestInputValidation:
    """ValueError is raised for invalid inputs."""

    @pytest.mark.parametrize("bad_param", ["a", "k", "c", "ms", "alpha", "h_start", "h_end"])
    def test_raises_on_nonscalar_parameter(self, bad_param):
        """A non-scalar model parameter must raise ValueError."""
        kwargs = dict(
            h=0.0, m=0.0,
            a=_A, k=_K, c=_C, ms=_MS, alpha=_ALPHA,
            h_start=-1000.0, h_end=1000.0,
        )
        kwargs[bad_param] = np.array([1.0, 2.0])
        with pytest.raises(ValueError, match=bad_param):
            dmdh(**kwargs)

    def test_raises_on_mismatched_h_m_shapes(self):
        """h and m with incompatible shapes must raise ValueError."""
        with pytest.raises(ValueError, match="same shape"):
            dmdh(
                h=np.array([0.0, 1.0, 2.0]),
                m=np.array([0.0, 0.0]),
                a=_A, k=_K, c=_C, ms=_MS, alpha=_ALPHA,
                h_start=-1000.0, h_end=1000.0,
            )


# ===========================================================================
# Vectorized (NumPy array) inputs
# ===========================================================================

class TestVectorizedInputs:
    """dmdh() must accept and correctly process NumPy arrays."""

    def test_returns_array_for_array_inputs(self):
        h = np.linspace(-500.0, 500.0, 11)
        m = np.zeros_like(h)
        result = _call(h=h, m=m)
        assert isinstance(result, np.ndarray)
        assert result.shape == h.shape

    def test_array_result_matches_scalar_calls(self):
        """Vectorized result must match scalar calls element-wise."""
        h_vals = np.array([-200.0, 0.0, 200.0])
        m_vals = np.zeros_like(h_vals)
        vec_result = _call(h=h_vals, m=m_vals)
        for i, (hi, mi) in enumerate(zip(h_vals, m_vals)):
            scalar_result = _call(h=float(hi), m=float(mi))
            assert np.isclose(vec_result[i], scalar_result, rtol=1e-12)

    def test_returns_scalar_for_scalar_inputs(self):
        result = _call(h=100.0, m=0.0)
        assert np.isscalar(result) or isinstance(result, (int, float))


# ===========================================================================
# Derivative of anhysteretic magnetization (dMah_iso equivalent)
# ===========================================================================

class TestAnhystereticDeriv:
    """
    Tests for the ``anhysteretic_magnetization_deriv`` helper that replaces
    the MATLAB ``dMah_iso`` function.
    """

    def test_at_origin_equals_ms_over_3a(self):
        """L'(0) = 1/3, so dMan/dH_eff(0) = ms/(3a)."""
        result = anhysteretic_magnetization_deriv(
            h=0.0, m=0.0, ms=_MS, a=_A, alpha=0.0
        )
        expected = _MS / (3.0 * _A)
        assert np.isclose(result, expected, rtol=1e-9)

    def test_positive_everywhere(self):
        """L'(x) = 1/x^2 - csch^2(x) > 0 for all x ≠ 0, so dMan/dH_eff > 0."""
        h_vals = np.linspace(-1000.0, 1000.0, 200)
        h_vals = h_vals[h_vals != 0.0]
        result = anhysteretic_magnetization_deriv(
            h=h_vals, m=np.zeros_like(h_vals), ms=_MS, a=_A, alpha=0.0
        )
        assert np.all(result > 0.0)

    def test_vanishes_at_large_field(self):
        """For large |H|, L'(x) → 0, so dMan/dH_eff → 0."""
        result = anhysteretic_magnetization_deriv(
            h=1.0e8, m=0.0, ms=_MS, a=_A, alpha=0.0
        )
        assert np.isclose(result, 0.0, atol=1e-6)

    def test_is_even_function_when_alpha_zero(self):
        """L'(x) is an even function, so dMan/dH_eff(H) == dMan/dH_eff(-H)."""
        h = 300.0
        pos = anhysteretic_magnetization_deriv(
            h=h, m=0.0, ms=_MS, a=_A, alpha=0.0
        )
        neg = anhysteretic_magnetization_deriv(
            h=-h, m=0.0, ms=_MS, a=_A, alpha=0.0
        )
        assert np.isclose(pos, neg, rtol=1e-12)

    def test_numpy_array_input(self):
        h = np.array([-500.0, 0.0, 500.0])
        result = anhysteretic_magnetization_deriv(
            h=h, m=np.zeros_like(h), ms=_MS, a=_A, alpha=0.0
        )
        assert isinstance(result, np.ndarray)
        assert result.shape == h.shape

    def test_raises_when_a_is_zero(self):
        with pytest.raises(ValueError, match="must be nonzero"):
            anhysteretic_magnetization_deriv(
                h=10.0, m=0.0, ms=_MS, a=0.0, alpha=0.0
            )
