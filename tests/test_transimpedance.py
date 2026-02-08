"""
Unit tests for transimpedance calculations.

Tests the magnetoelasticsensor.transimpedance module for complex impedance
calculations in magnetoelastic sensor circuits.
"""

import math
import cmath
import pytest
from magnetoelasticsensor.air_gap_permeance import calculate_air_gap_permeance
from magnetoelasticsensor.cross_leakage_permeance import CrossLeakagePermeanceModel
from magnetoelasticsensor.geometry import DEFAULT_SENSOR_GEOMETRY
from magnetoelasticsensor.permeance import calculate_effective_permeance
from magnetoelasticsensor.transimpedance import (
    calculate_normalized_impedance,
    calculate_transimpedance,
    calculate_transimpedance_magnitude,
    calculate_transimpedance_phase,
)
from magnetoelasticsensor.target_permeance import (
    TargetPermeanceModel,
    calculate_target_permeance,
)

class TestNormalizedImpedance:
    """Tests for complex normalized impedance calculation."""

    def test_normalized_impedance_returns_complex(self):
        """Test that normalized impedance returns a complex number."""
        z = calculate_normalized_impedance(
            p3=1e-8,
            p_sd=3e-9,
            p=2e-8,
            epsilon=0.1,
        )
        assert isinstance(z, complex)

    def test_normalized_impedance_zero_epsilon(self):
        """Test normalized impedance with zero damping factor."""
        z = calculate_normalized_impedance(
            p3=1e-8,
            p_sd=3e-9,
            p=2e-8,
            epsilon=0.0,
        )
        assert isinstance(z, complex)
        # With epsilon=0, impedance should still be finite and well-defined
        assert math.isfinite(abs(z))

    def test_normalized_impedance_default_values(self):
        """Test with default magnetoelastic sensor values."""
        model = TargetPermeanceModel()
        pt,p3 = model.calculate_target_permeance()
        p_gaps, p_gapd = calculate_air_gap_permeance()
        p = calculate_effective_permeance(pt=pt, p_gapd=p_gapd, p_gaps=p_gaps)    

        model = CrossLeakagePermeanceModel()
        p_sd = model.calculate_cross_leakage_permeance()
        epsilon = math.tan(math.radians(DEFAULT_SENSOR_GEOMETRY.theta3_deg.nominal))  

        # Call the function under test        
        z = calculate_normalized_impedance(p3=p3, p_sd=p_sd, p=p, epsilon=epsilon)

        # Low-level sanity checks on the output
        assert isinstance(z, complex)
        assert math.isfinite(abs(z))

        # Copied over from "Calculate the normalized impedance" section in "UncertaintyChain.nb" notebook
        z_expected = complex(0.32936430169468783, -0.01725711423759577)  
        
        assert cmath.isclose(z, z_expected, rel_tol=1e-8)

    def test_normalized_impedance_raises_for_zero_p3(self):
        """Test that ValueError is raised for zero target permeance."""
        with pytest.raises(ValueError, match="All permeances must be positive"):
            calculate_normalized_impedance(p3=0, p_sd=1e-8, p=1e-8, epsilon=0.1)

    def test_normalized_impedance_raises_for_zero_p_sd(self):
        """Test that ValueError is raised for zero cross-leakage."""
        with pytest.raises(ValueError, match="All permeances must be positive"):
            calculate_normalized_impedance(p3=1e-8, p_sd=0, p=1e-8, epsilon=0.1)

    def test_normalized_impedance_raises_for_zero_p(self):
        """Test that ValueError is raised for zero effective permeance."""
        with pytest.raises(ValueError, match="All permeances must be positive"):
            calculate_normalized_impedance(p3=1e-8, p_sd=1e-8, p=0, epsilon=0.1)

    def test_normalized_impedance_raises_for_negative_epsilon(self):
        """Test that ValueError is raised for negative damping factor."""
        with pytest.raises(ValueError, match="epsilon must be non-negative"):
            calculate_normalized_impedance(
                p3=1e-8, p_sd=1e-8, p=1e-8, epsilon=-0.01
            )

    def test_normalized_impedance_raises_for_negative_p3(self):
        """Test that ValueError is raised for negative target permeance."""
        with pytest.raises(ValueError, match="All permeances must be positive"):
            calculate_normalized_impedance(p3=-1e-8, p_sd=1e-8, p=1e-8, epsilon=0.1)

    @pytest.mark.parametrize(
        "p3,p_sd,p,epsilon",
        [
            (1e-8, 5e-9, 2e-8, 0.05),
            (5e-8, 2e-8, 1e-8, 0.1),
            (1e-7, 3e-8, 5e-8, 0.02),
        ],
    )
    def test_normalized_impedance_parametric(self, p3, p_sd, p, epsilon):
        """Test normalized impedance with various parameter combinations."""
        z = calculate_normalized_impedance(p3=p3, p_sd=p_sd, p=p, epsilon=epsilon)
        assert isinstance(z, complex)
        assert math.isfinite(abs(z))


class TestTransimpedance:
    """Tests for complex transimpedance calculation."""

    def test_transimpedance_returns_complex(self):
        """Test that transimpedance returns a complex number."""
        z = calculate_transimpedance(
            nd=100,
            ns=100,
            p_eq=3e-8,
            omega=2 * math.pi * 50e3,
            p3=8.6e-8,
            p_sd=2.3e-8,
            p=2.5e-8,
            epsilon=0.05,
        )
        assert isinstance(z, complex)

    def test_transimpedance_increases_with_frequency(self):
        """Test that transimpedance magnitude generally increases with frequency."""
        nd, ns = 100, 100
        p_eq = 3e-8
        p3, p_sd, p = 8.6e-8, 2.3e-8, 2.5e-8
        epsilon = 0.05
        
        z_low = calculate_transimpedance(
            nd=nd, ns=ns, p_eq=p_eq, omega=2*math.pi*10e3,
            p3=p3, p_sd=p_sd, p=p, epsilon=epsilon
        )
        z_high = calculate_transimpedance(
            nd=nd, ns=ns, p_eq=p_eq, omega=2*math.pi*100e3,
            p3=p3, p_sd=p_sd, p=p, epsilon=epsilon
        )
        
        # Generally, impedance magnitude should increase with frequency
        # due to the ω term
        assert abs(z_high) > abs(z_low)

    def test_transimpedance_turns_dependence(self):
        """Test that transimpedance scales with turn counts."""
        p_eq = 3e-8
        omega = 2 * math.pi * 50e3
        p3, p_sd, p = 8.6e-8, 2.3e-8, 2.5e-8
        epsilon = 0.05
        
        z_100_100 = calculate_transimpedance(
            nd=100, ns=100, p_eq=p_eq, omega=omega,
            p3=p3, p_sd=p_sd, p=p, epsilon=epsilon
        )
        z_50_50 = calculate_transimpedance(
            nd=50, ns=50, p_eq=p_eq, omega=omega,
            p3=p3, p_sd=p_sd, p=p, epsilon=epsilon
        )
        
        # Scaling by 1/4 in turn product (50*50 vs 100*100)
        assert abs(z_100_100) == pytest.approx(4 * abs(z_50_50), rel=1e-10)

    def test_transimpedance_raises_for_zero_turns(self):
        """Test that ValueError is raised for zero turn count."""
        with pytest.raises(ValueError, match="nd must be a positive integer"):
            calculate_transimpedance(
                nd=0, ns=100, p_eq=3e-8, omega=2*math.pi*50e3,
                p3=8.6e-8, p_sd=2.3e-8, p=2.5e-8, epsilon=0.05
            )

    def test_transimpedance_raises_for_negative_turns(self):
        """Test that ValueError is raised for negative turn count."""
        with pytest.raises(ValueError, match="ns must be a positive integer"):
            calculate_transimpedance(
                nd=100, ns=-50, p_eq=3e-8, omega=2*math.pi*50e3,
                p3=8.6e-8, p_sd=2.3e-8, p=2.5e-8, epsilon=0.05
            )

    def test_transimpedance_raises_for_zero_omega(self):
        """Test that ValueError is raised for zero frequency."""
        with pytest.raises(ValueError, match="omega must be positive"):
            calculate_transimpedance(
                nd=100, ns=100, p_eq=3e-8, omega=0,
                p3=8.6e-8, p_sd=2.3e-8, p=2.5e-8, epsilon=0.05
            )

    def test_transimpedance_raises_for_zero_p_eq(self):
        """Test that ValueError is raised for zero equivalent permeance."""
        with pytest.raises(ValueError, match="p_eq must be positive"):
            calculate_transimpedance(
                nd=100, ns=100, p_eq=0, omega=2*math.pi*50e3,
                p3=8.6e-8, p_sd=2.3e-8, p=2.5e-8, epsilon=0.05
            )

    @pytest.mark.parametrize(
        "nd,ns,p_eq,omega,p3,p_sd,p,epsilon",
        [
            (100, 100, 3e-8, 2*math.pi*10e3, 8.6e-8, 2.3e-8, 2.5e-8, 0.05),
            (50, 100, 4e-8, 2*math.pi*50e3, 9e-8, 2.5e-8, 2.8e-8, 0.1),
            (200, 200, 2e-8, 2*math.pi*100e3, 7e-8, 2e-8, 2.2e-8, 0.02),
        ],
    )
    def test_transimpedance_parametric(
        self, nd, ns, p_eq, omega, p3, p_sd, p, epsilon
    ):
        """Test transimpedance with various parameter combinations."""
        z = calculate_transimpedance(
            nd=nd, ns=ns, p_eq=p_eq, omega=omega,
            p3=p3, p_sd=p_sd, p=p, epsilon=epsilon
        )
        assert isinstance(z, complex)
        assert math.isfinite(abs(z))


class TestTransimpedanceMagnitude:
    """Tests for transimpedance magnitude calculation."""

    def test_magnitude_is_positive(self):
        """Test that magnitude is always positive."""
        mag = calculate_transimpedance_magnitude(
            nd=100, ns=100, p_eq=3e-8, omega=2*math.pi*50e3,
            p3=8.6e-8, p_sd=2.3e-8, p=2.5e-8, epsilon=0.05
        )
        assert mag >= 0

    def test_magnitude_matches_complex_abs(self):
        """Test that magnitude matches abs() of complex impedance."""
        nd, ns, p_eq, omega = 100, 100, 3e-8, 2*math.pi*50e3
        p3, p_sd, p, epsilon = 8.6e-8, 2.3e-8, 2.5e-8, 0.05
        
        z = calculate_transimpedance(
            nd=nd, ns=ns, p_eq=p_eq, omega=omega,
            p3=p3, p_sd=p_sd, p=p, epsilon=epsilon
        )
        mag = calculate_transimpedance_magnitude(
            nd=nd, ns=ns, p_eq=p_eq, omega=omega,
            p3=p3, p_sd=p_sd, p=p, epsilon=epsilon
        )
        
        assert mag == pytest.approx(abs(z), rel=1e-12)

    def test_magnitude_increases_with_turns(self):
        """Test that magnitude scales with turn counts."""
        p_eq = 3e-8
        omega = 2 * math.pi * 50e3
        p3, p_sd, p = 8.6e-8, 2.3e-8, 2.5e-8
        epsilon = 0.05
        
        mag_100_100 = calculate_transimpedance_magnitude(
            nd=100, ns=100, p_eq=p_eq, omega=omega,
            p3=p3, p_sd=p_sd, p=p, epsilon=epsilon
        )
        mag_50_50 = calculate_transimpedance_magnitude(
            nd=50, ns=50, p_eq=p_eq, omega=omega,
            p3=p3, p_sd=p_sd, p=p, epsilon=epsilon
        )
        
        assert mag_100_100 == pytest.approx(4 * mag_50_50, rel=1e-10)


class TestTransimpedancePhase:
    """Tests for transimpedance phase angle calculation."""

    def test_phase_is_in_range(self):
        """Test that phase angle is within [-π, π]."""
        phase = calculate_transimpedance_phase(
            nd=100, ns=100, p_eq=3e-8, omega=2*math.pi*50e3,
            p3=8.6e-8, p_sd=2.3e-8, p=2.5e-8, epsilon=0.05
        )
        assert -math.pi <= phase <= math.pi

    def test_phase_matches_complex_angle(self):
        """Test that phase matches cmath.phase() of complex impedance."""
        nd, ns, p_eq, omega = 100, 100, 3e-8, 2*math.pi*50e3
        p3, p_sd, p, epsilon = 8.6e-8, 2.3e-8, 2.5e-8, 0.05
        
        z = calculate_transimpedance(
            nd=nd, ns=ns, p_eq=p_eq, omega=omega,
            p3=p3, p_sd=p_sd, p=p, epsilon=epsilon
        )
        phase = calculate_transimpedance_phase(
            nd=nd, ns=ns, p_eq=p_eq, omega=omega,
            p3=p3, p_sd=p_sd, p=p, epsilon=epsilon
        )
        
        assert phase == pytest.approx(cmath.phase(z), rel=1e-12)

    def test_phase_frequency_dependent(self):
        """Test that phase is computed for different frequencies."""
        nd, ns, p_eq = 100, 100, 3e-8
        p3, p_sd, p = 8.6e-8, 2.3e-8, 2.5e-8
        epsilon = 0.05
        
        phase_low = calculate_transimpedance_phase(
            nd=nd, ns=ns, p_eq=p_eq, omega=2*math.pi*10e3,
            p3=p3, p_sd=p_sd, p=p, epsilon=epsilon
        )
        phase_high = calculate_transimpedance_phase(
            nd=nd, ns=ns, p_eq=p_eq, omega=2*math.pi*500e3,
            p3=p3, p_sd=p_sd, p=p, epsilon=epsilon
        )
        
        # Phase should be computed and finite at both frequencies
        assert math.isfinite(phase_low)
        assert math.isfinite(phase_high)


class TestIntegration:
    """Integration tests for transimpedance calculations."""

    def test_impedance_properties_consistency(self):
        """Test consistency between magnitude, phase, and complex impedance."""
        nd, ns, p_eq, omega = 100, 100, 3e-8, 2*math.pi*50e3
        p3, p_sd, p = 8.6e-8, 2.3e-8, 2.5e-8
        epsilon = 0.05
        
        z = calculate_transimpedance(
            nd=nd, ns=ns, p_eq=p_eq, omega=omega,
            p3=p3, p_sd=p_sd, p=p, epsilon=epsilon
        )
        mag = calculate_transimpedance_magnitude(
            nd=nd, ns=ns, p_eq=p_eq, omega=omega,
            p3=p3, p_sd=p_sd, p=p, epsilon=epsilon
        )
        phase = calculate_transimpedance_phase(
            nd=nd, ns=ns, p_eq=p_eq, omega=omega,
            p3=p3, p_sd=p_sd, p=p, epsilon=epsilon
        )
        
        # z = mag * e^(j*phase)
        z_reconstructed = mag * cmath.exp(1j * phase)
        
        assert z == pytest.approx(z_reconstructed, rel=1e-10)

    def test_frequency_sweep_response(self):
        """Test transimpedance response across frequency range."""
        nd, ns, p_eq = 100, 100, 3e-8
        p3, p_sd, p = 8.6e-8, 2.3e-8, 2.5e-8
        epsilon = 0.05
        
        frequencies_khz = [10, 20, 50, 100, 200, 500]
        magnitudes = []
        phases = []
        
        for f_khz in frequencies_khz:
            omega = 2 * math.pi * f_khz * 1e3
            mag = calculate_transimpedance_magnitude(
                nd=nd, ns=ns, p_eq=p_eq, omega=omega,
                p3=p3, p_sd=p_sd, p=p, epsilon=epsilon
            )
            phase = calculate_transimpedance_phase(
                nd=nd, ns=ns, p_eq=p_eq, omega=omega,
                p3=p3, p_sd=p_sd, p=p, epsilon=epsilon
            )
            magnitudes.append(mag)
            phases.append(phase)
        
        # Verify all are finite
        for mag in magnitudes:
            assert math.isfinite(mag)
        for phase in phases:
            assert math.isfinite(phase)
        
        # Verify monotonic increase in magnitude (approximately)
        # with frequency-dependent damping
        assert magnitudes[-1] > magnitudes[0]

    def test_damping_effect_on_impedance(self):
        """Test how damping factor (epsilon) affects impedance."""
        nd, ns, p_eq, omega = 100, 100, 3e-8, 2*math.pi*50e3
        p3, p_sd, p = 8.6e-8, 2.3e-8, 2.5e-8
        
        # Different damping factors
        mag_low_damping = calculate_transimpedance_magnitude(
            nd=nd, ns=ns, p_eq=p_eq, omega=omega,
            p3=p3, p_sd=p_sd, p=p, epsilon=0.01
        )
        mag_high_damping = calculate_transimpedance_magnitude(
            nd=nd, ns=ns, p_eq=p_eq, omega=omega,
            p3=p3, p_sd=p_sd, p=p, epsilon=0.2
        )
        
        # Damping should modify the impedance
        assert mag_low_damping != mag_high_damping
