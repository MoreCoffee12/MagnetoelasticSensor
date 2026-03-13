"""
test_ja_solver.py

Pytest test harness for ``ja_solver()`` — the Jiles-Atherton ODE solver.

Four solver backends are exercised:
    Type 1 — RK23  (adaptive, SciPy)
    Type 2 — RK45  (adaptive, SciPy)
    Type 3 — Radau (adaptive stiff, SciPy)
    Type 4 — RK4   (fixed-step, 50 uniform steps)

References
----------
[1] Jiles D. C., Atherton D. "Theory of ferromagnetic hysteresis."
    Journal of Magnetism and Magnetic Materials, 61 (1986) 48.
[2] Szewczyk R. "Computational problems connected with Jiles-Atherton model
    of magnetic hysteresis." Advances in Intelligent Systems and Computing
    (Springer), 267 (2014) 275.
"""

from __future__ import annotations

import numpy as np
import pytest

from magnetoelasticsensor.ja_solver import ja_solver

# ---------------------------------------------------------------------------
# Shared parameter set — matches the Mathematica companion-notebook values
# ---------------------------------------------------------------------------
_A = 1100.0
_K = 500.0
_C = 0.1
_MS = 1.6e6
_ALPHA = 0.0016


def _solve(h_start, h_end, m0=0.0, solver_type=1, **overrides):
    """Run ja_solver with the shared parameter set."""
    params = dict(a=_A, k=_K, c=_C, ms=_MS, alpha=_ALPHA)
    params.update(overrides)
    return ja_solver(
        h_start=h_start, h_end=h_end, m0=m0, solver_type=solver_type, **params
    )


# ===========================================================================
# Trivial / degenerate case
# ===========================================================================

class TestTrivialCase:
    """When h_start == h_end the answer is immediate."""

    def test_returns_two_element_arrays(self):
        h_out, m_out = _solve(h_start=500.0, h_end=500.0, m0=123.0)
        assert len(h_out) == 2
        assert len(m_out) == 2

    def test_magnetization_is_constant_at_m0(self):
        m0 = 12345.0
        _, m_out = _solve(h_start=500.0, h_end=500.0, m0=m0)
        assert np.allclose(m_out, m0)

    def test_field_values_are_h_start(self):
        h_val = 777.0
        h_out, _ = _solve(h_start=h_val, h_end=h_val)
        assert np.allclose(h_out, h_val)


# ===========================================================================
# Output shape and dtype
# ===========================================================================

class TestOutputStructure:
    """Basic sanity checks on the returned arrays."""

    @pytest.mark.parametrize("solver_type", [1, 2, 3, 4])
    def test_returns_numpy_arrays(self, solver_type):
        h_out, m_out = _solve(0.0, 2000.0, solver_type=solver_type)
        assert isinstance(h_out, np.ndarray)
        assert isinstance(m_out, np.ndarray)

    @pytest.mark.parametrize("solver_type", [1, 2, 3, 4])
    def test_output_arrays_same_length(self, solver_type):
        h_out, m_out = _solve(0.0, 2000.0, solver_type=solver_type)
        assert len(h_out) == len(m_out)

    @pytest.mark.parametrize("solver_type", [1, 2, 3, 4])
    def test_output_has_at_least_two_points(self, solver_type):
        h_out, m_out = _solve(0.0, 2000.0, solver_type=solver_type)
        assert len(h_out) >= 2

    def test_rk4_returns_exactly_51_points(self):
        """RK4 uses 50 fixed steps plus the initial point → 51 values."""
        h_out, _ = _solve(0.0, 5000.0, solver_type=4)
        assert len(h_out) == 51


# ===========================================================================
# Initial condition
# ===========================================================================

class TestInitialCondition:
    """The solver must honour the supplied starting magnetization m0."""

    @pytest.mark.parametrize("solver_type", [1, 2, 3, 4])
    def test_first_m_value_equals_m0(self, solver_type):
        m0 = 50000.0
        _, m_out = _solve(0.0, 3000.0, m0=m0, solver_type=solver_type)
        assert np.isclose(m_out[0], m0, rtol=1e-9)

    @pytest.mark.parametrize("solver_type", [1, 2, 3, 4])
    def test_first_h_value_equals_h_start(self, solver_type):
        h_start = 100.0
        h_out, _ = _solve(h_start, 4000.0, solver_type=solver_type)
        assert np.isclose(h_out[0], h_start, rtol=1e-9)

    @pytest.mark.parametrize("solver_type", [1, 2, 3, 4])
    def test_last_h_value_is_near_h_end(self, solver_type):
        h_end = 4000.0
        h_out, _ = _solve(0.0, h_end, solver_type=solver_type)
        assert np.isclose(h_out[-1], h_end, rtol=1e-6)


# ===========================================================================
# Physical bounds
# ===========================================================================

class TestPhysicalBounds:
    """All magnetization values must lie within [-ms, +ms]."""

    @pytest.mark.parametrize("solver_type", [1, 2, 3, 4])
    def test_m_bounded_below_ms(self, solver_type):
        _, m_out = _solve(0.0, 1.0e5, solver_type=solver_type)
        assert np.all(m_out <= _MS * 1.01)  # 1% tolerance for numerical overshoot

    @pytest.mark.parametrize("solver_type", [1, 2, 3, 4])
    def test_m_bounded_above_neg_ms(self, solver_type):
        _, m_out = _solve(0.0, -1.0e5, solver_type=solver_type)
        assert np.all(m_out >= -_MS * 1.01)


# ===========================================================================
# Physical directionality
# ===========================================================================

class TestPhysicalDirectionality:
    """Qualitative checks that the model behaves like a real ferromagnet."""

    def test_positive_field_sweep_gives_positive_final_m(self):
        """Starting from demagnetized state, large positive field → M > 0."""
        _, m_out = _solve(h_start=0.0, h_end=5.0e4, m0=0.0)
        assert m_out[-1] > 0.0

    def test_negative_field_sweep_gives_negative_final_m(self):
        """Starting from demagnetized state, large negative field → M < 0."""
        _, m_out = _solve(h_start=0.0, h_end=-5.0e4, m0=0.0)
        assert m_out[-1] < 0.0

    def test_antisymmetry_from_demagnetized_state(self):
        """
        By symmetry, a sweep from 0 to +H and a sweep from 0 to -H starting
        from M=0 should give M_final ≈ -M_final (within solver tolerance).
        """
        _, m_fwd = _solve(h_start=0.0, h_end=3.0e4, m0=0.0)
        _, m_rev = _solve(h_start=0.0, h_end=-3.0e4, m0=0.0)
        assert np.isclose(m_fwd[-1], -m_rev[-1], rtol=1e-3)

    def test_saturation_at_very_large_field(self):
        """
        At H >> a, Man → ms.  After a long sweep from 0 the magnetization
        must approach ms to within a few percent.
        """
        _, m_out = _solve(h_start=0.0, h_end=1.0e6, m0=0.0)
        assert m_out[-1] > 0.9 * _MS


# ===========================================================================
# Solver-type agreement
# ===========================================================================

class TestSolverAgreement:
    """
    All solver types should converge to comparable solutions for a smooth case.
    Tolerances are loose because RK4 (50 steps) is less accurate than adaptive
    methods; we only require agreement to ~1%.
    """

    def _ref(self, h_end=5000.0, m0=0.0):
        """RK45 reference solution at the final field point."""
        _, m_out = _solve(0.0, h_end, m0=m0, solver_type=2)  # RK45
        return m_out[-1]

    @pytest.mark.parametrize("solver_type", [1, 3, 4])
    def test_agrees_with_rk45_to_1_percent(self, solver_type):
        h_end = 5000.0
        ref = self._ref(h_end=h_end)
        _, m_out = _solve(0.0, h_end, solver_type=solver_type)
        assert np.isclose(m_out[-1], ref, rtol=0.01)


# ===========================================================================
# Input validation
# ===========================================================================

class TestInputValidation:
    """ValueError is raised for out-of-range solver_type."""

    @pytest.mark.parametrize("bad_type", [0, 5, -1, 10])
    def test_raises_on_invalid_solver_type(self, bad_type):
        with pytest.raises(ValueError, match="solver_type"):
            _solve(0.0, 1000.0, solver_type=bad_type)

    def test_default_solver_type_runs_without_error(self):
        """No solver_type supplied → uses default (type 1, RK23)."""
        h_out, m_out = ja_solver(
            a=_A, k=_K, c=_C, ms=_MS, alpha=_ALPHA,
            h_start=0.0, h_end=2000.0, m0=0.0,
        )
        assert len(h_out) >= 2
        assert len(m_out) >= 2


# ===========================================================================
# Decreasing-field sweep
# ===========================================================================

class TestDecreasingField:
    """Verify solver handles h_start > h_end correctly."""

    @pytest.mark.parametrize("solver_type", [1, 2, 3, 4])
    def test_decreasing_sweep_returns_valid_arrays(self, solver_type):
        h_out, m_out = _solve(
            h_start=5000.0, h_end=0.0, m0=5.0e5, solver_type=solver_type
        )
        assert len(h_out) >= 2
        assert np.all(np.isfinite(m_out))

    def test_decreasing_sweep_first_h_equals_h_start(self):
        h_start = 5000.0
        h_out, _ = _solve(h_start=h_start, h_end=0.0, m0=5.0e5)
        assert np.isclose(h_out[0], h_start, rtol=1e-9)
