"""
Unit tests for cross-leakage permeance calculations.

Tests the magnetoelasticsensor.permeance module against Fleming's equations.
"""

import math
import pytest
from magnetoelasticsensor.permeance import (
    cross_leakage_gu,
    cross_leakage_u_parameter,
    cross_leakage_permeance,
    MU_0,
)


class TestCrossLeakageGu:
    """Tests for g_u normalized permeance coefficient calculation."""

    def test_gu_valid_u_equals_2(self):
        """Test g_u calculation with u = 2."""
        u = 2.0
        gu = cross_leakage_gu(u)
        
        # Manual calculation: g_u = 2π / ln(2 + √3)
        expected = 2 * math.pi / math.log(2 + math.sqrt(3))
        assert math.isclose(gu, expected, rel_tol=1e-10)

    def test_gu_valid_u_equals_1_8(self):
        """Test g_u calculation with u = 1.8."""
        u = 1.8
        gu = cross_leakage_gu(u)
        
        expected = 2 * math.pi / math.log(u + math.sqrt(u**2 - 1))
        assert math.isclose(gu, expected, rel_tol=1e-10)

    def test_gu_large_u_approaches_limit(self):
        """Test that g_u decreases with increasing u (approaches 0 limit)."""
        gu_small = cross_leakage_gu(1.1)
        gu_large = cross_leakage_gu(10.0)
        assert gu_small > gu_large

    def test_gu_raises_for_u_equals_1(self):
        """Test that g_u raises ValueError when u = 1 (sqrt(u² - 1) = 0, log singularity)."""
        with pytest.raises(ValueError, match="u must be > 1"):
            cross_leakage_gu(1.0)

    def test_gu_raises_for_u_less_than_1(self):
        """Test that g_u raises ValueError when u < 1."""
        with pytest.raises(ValueError, match="u must be > 1"):
            cross_leakage_gu(0.5)

    def test_gu_raises_for_negative_u(self):
        """Test that g_u raises ValueError for negative u."""
        with pytest.raises(ValueError, match="u must be > 1"):
            cross_leakage_gu(-2.0)

    def test_gu_returns_positive(self):
        """Test that g_u returns positive values for valid u."""
        for u in [1.01, 1.5, 2.0, 5.0, 100.0]:
            assert cross_leakage_gu(u) > 0


class TestCrossLeakageUParameter:
    """Tests for normalized geometric parameter u calculation."""

    def test_u_parameter_nominal_geometry(self):
        """Test u calculation with nominal sensor dimensions."""
        dim_spagi = 1e-3    # 1 mm
        dim_dp = 5e-3       # 5 mm
        dim_spi = 4e-3      # 4 mm
        
        u = cross_leakage_u_parameter(dim_spagi, dim_dp, dim_spi)
        
        # Manual calculation: u = 1 + (2 * spagi * (dp + spi + spagi)) / (dp * spi)
        expected = 1 + (2 * dim_spagi * (dim_dp + dim_spi + dim_spagi)) / (dim_dp * dim_spi)
        assert math.isclose(u, expected, rel_tol=1e-10)
        assert u == 2.0  # Specific case should give exactly 2.0

    def test_u_parameter_compact_geometry(self):
        """Test u calculation with compact sensor dimensions."""
        dim_spagi = 0.5e-3
        dim_dp = 3e-3
        dim_spi = 2.5e-3
        
        u = cross_leakage_u_parameter(dim_spagi, dim_dp, dim_spi)
        
        expected = 1 + (2 * dim_spagi * (dim_dp + dim_spi + dim_spagi)) / (dim_dp * dim_spi)
        assert math.isclose(u, expected, rel_tol=1e-10)
        assert u == pytest.approx(1.8, rel=1e-10)

    def test_u_parameter_always_greater_than_1(self):
        """Test that u is always > 1 for positive dimensions."""
        test_cases = [
            (0.1e-3, 1e-3, 1e-3),
            (1e-3, 5e-3, 4e-3),
            (10e-3, 50e-3, 40e-3),
        ]
        for dim_spagi, dim_dp, dim_spi in test_cases:
            u = cross_leakage_u_parameter(dim_spagi, dim_dp, dim_spi)
            assert u > 1, f"u={u} should be > 1 for dims: {(dim_spagi, dim_dp, dim_spi)}"

    def test_u_parameter_raises_for_zero_dim_dp(self):
        """Test that ValueError is raised when dim_dp = 0."""
        with pytest.raises(ValueError, match="Dimensions must be positive"):
            cross_leakage_u_parameter(1e-3, 0, 2e-3)

    def test_u_parameter_raises_for_zero_dim_spi(self):
        """Test that ValueError is raised when dim_spi = 0."""
        with pytest.raises(ValueError, match="Dimensions must be positive"):
            cross_leakage_u_parameter(1e-3, 5e-3, 0)

    def test_u_parameter_raises_for_negative_dim_dp(self):
        """Test that ValueError is raised when dim_dp < 0."""
        with pytest.raises(ValueError, match="Dimensions must be positive"):
            cross_leakage_u_parameter(1e-3, -5e-3, 2e-3)

    def test_u_parameter_raises_for_negative_dim_spi(self):
        """Test that ValueError is raised when dim_spi < 0."""
        with pytest.raises(ValueError, match="Dimensions must be positive"):
            cross_leakage_u_parameter(1e-3, 5e-3, -2e-3)

    def test_u_parameter_increases_with_spagi(self):
        """Test that u increases as dim_spagi increases."""
        dim_dp = 5e-3
        dim_spi = 4e-3
        
        u_small_spagi = cross_leakage_u_parameter(0.5e-3, dim_dp, dim_spi)
        u_large_spagi = cross_leakage_u_parameter(2.0e-3, dim_dp, dim_spi)
        
        assert u_large_spagi > u_small_spagi


class TestCrossLeakagePermeance:
    """Tests for cross-leakage flux permeance calculation."""

    def test_permeance_nominal_geometry(self):
        """Test permeance calculation with nominal sensor geometry."""
        dim_spagi = 1e-3
        dim_dp = 5e-3
        dim_spi = 4e-3
        dim_sphi = 10e-3
        dim_spahi = 2e-3
        g2 = 0.5e-3
        
        permeance = cross_leakage_permeance(
            dim_spagi, dim_dp, dim_spi, dim_sphi, dim_spahi, g2
        )
        
        # Verify it's positive and in reasonable range for inductance
        assert permeance > 0
        assert 1e-9 < permeance < 1e-6  # Typical inductor range

    def test_permeance_compact_geometry(self):
        """Test permeance calculation with compact sensor geometry."""
        dim_spagi = 0.5e-3
        dim_dp = 3e-3
        dim_spi = 2.5e-3
        dim_sphi = 5e-3
        dim_spahi = 1e-3
        g2 = 0.3e-3
        
        permeance = cross_leakage_permeance(
            dim_spagi, dim_dp, dim_spi, dim_sphi, dim_spahi, g2
        )
        
        assert permeance > 0
        assert 1e-9 < permeance < 1e-6

    def test_permeance_equals_mu0_times_coefficient(self):
        """Test that permeance is proportional to μ₀."""
        dim_spagi = 1e-3
        dim_dp = 5e-3
        dim_spi = 4e-3
        dim_sphi = 10e-3
        dim_spahi = 2e-3
        g2 = 0.5e-3
        
        permeance = cross_leakage_permeance(
            dim_spagi, dim_dp, dim_spi, dim_sphi, dim_spahi, g2
        )
        
        # Manual calculation of coefficient
        u = cross_leakage_u_parameter(dim_spagi, dim_dp, dim_spi)
        gu = cross_leakage_gu(u)
        h = dim_sphi - dim_spahi
        coefficient = (h - g2) * gu
        
        expected = MU_0 * coefficient
        assert math.isclose(permeance, expected, rel_tol=1e-10)

    def test_permeance_increases_with_height_difference(self):
        """Test that permeance increases as (h - g2) increases."""
        dim_spagi = 1e-3
        dim_dp = 5e-3
        dim_spi = 4e-3
        dim_spahi = 2e-3
        g2 = 0.5e-3
        
        # Case 1: smaller height
        permeance_1 = cross_leakage_permeance(
            dim_spagi, dim_dp, dim_spi, 8e-3, dim_spahi, g2
        )
        
        # Case 2: larger height
        permeance_2 = cross_leakage_permeance(
            dim_spagi, dim_dp, dim_spi, 12e-3, dim_spahi, g2
        )
        
        assert permeance_2 > permeance_1

    def test_permeance_decreases_with_increased_g2(self):
        """Test that permeance decreases as g2 (secondary gap) increases."""
        dim_spagi = 1e-3
        dim_dp = 5e-3
        dim_spi = 4e-3
        dim_sphi = 10e-3
        dim_spahi = 2e-3
        
        # Case 1: smaller g2
        permeance_1 = cross_leakage_permeance(
            dim_spagi, dim_dp, dim_spi, dim_sphi, dim_spahi, 0.3e-3
        )
        
        # Case 2: larger g2
        permeance_2 = cross_leakage_permeance(
            dim_spagi, dim_dp, dim_spi, dim_sphi, dim_spahi, 0.7e-3
        )
        
        assert permeance_1 > permeance_2

    def test_permeance_raises_for_invalid_dimensions(self):
        """Test that permeance raises errors for invalid dimensional inputs."""
        with pytest.raises(ValueError, match="Dimensions must be positive"):
            cross_leakage_permeance(1e-3, 0, 2e-3, 5e-3, 1e-3, 0.3e-3)

    def test_permeance_with_zero_height_difference(self):
        """Test permeance when (h - g2) = 0 (edge case)."""
        dim_spagi = 1e-3
        dim_dp = 5e-3
        dim_spi = 4e-3
        dim_sphi = 2.3e-3
        dim_spahi = 2e-3
        g2 = 0.3e-3  # h - g2 = 2.3e-3 - 2e-3 - 0.3e-3 = 0
        
        permeance = cross_leakage_permeance(
            dim_spagi, dim_dp, dim_spi, dim_sphi, dim_spahi, g2
        )
        
        # Permeance should be zero (or very close due to floating point)
        assert math.isclose(permeance, 0, abs_tol=1e-15)


class TestPhysicalConstants:
    """Tests for physical constants."""

    def test_mu0_value(self):
        """Test that μ₀ has correct SI value."""
        expected_mu0 = 4 * math.pi * 1e-7
        assert math.isclose(MU_0, expected_mu0, rel_tol=1e-10)

    def test_mu0_units(self):
        """Verify μ₀ is in correct units (H/m)."""
        # μ₀ should be approximately 1.256637e-6 H/m
        assert 1.25e-6 < MU_0 < 1.27e-6


class TestIntegration:
    """Integration tests combining multiple functions."""

    @pytest.mark.parametrize(
        "dim_spagi,dim_dp,dim_spi,dim_sphi,dim_spahi,g2",
        [
            (1.0e-3, 5.0e-3, 4.0e-3, 10.0e-3, 2.0e-3, 0.5e-3),
            (0.5e-3, 3.0e-3, 2.5e-3, 5.0e-3, 1.0e-3, 0.3e-3),
            (2.0e-3, 10.0e-3, 8.0e-3, 15.0e-3, 3.0e-3, 0.8e-3),
        ],
    )
    def test_permeance_always_positive_for_valid_inputs(
        self, dim_spagi, dim_dp, dim_spi, dim_sphi, dim_spahi, g2
    ):
        """Test that permeance is always positive for valid sensor geometries."""
        # Assume (h - g2) > 0 for valid sensor design
        if dim_sphi - dim_spahi > g2:
            permeance = cross_leakage_permeance(
                dim_spagi, dim_dp, dim_spi, dim_sphi, dim_spahi, g2
            )
            assert permeance > 0

    def test_full_calculation_workflow(self):
        """Test complete workflow from geometry to permeance."""
        # Define sensor geometry
        dim_spagi = 1.0e-3
        dim_dp = 5.0e-3
        dim_spi = 4.0e-3
        dim_sphi = 10.0e-3
        dim_spahi = 2.0e-3
        g2 = 0.5e-3
        
        # Calculate u parameter
        u = cross_leakage_u_parameter(dim_spagi, dim_dp, dim_spi)
        assert 1 < u <= 100
        
        # Calculate g_u coefficient
        gu = cross_leakage_gu(u)
        assert gu > 0
        
        # Calculate final permeance
        permeance = cross_leakage_permeance(
            dim_spagi, dim_dp, dim_spi, dim_sphi, dim_spahi, g2
        )
        assert permeance > 0
        
        # Verify manual calculation matches function
        h = dim_sphi - dim_spahi
        manual_permeance = MU_0 * (h - g2) * gu
        assert math.isclose(permeance, manual_permeance, rel_tol=1e-10)
