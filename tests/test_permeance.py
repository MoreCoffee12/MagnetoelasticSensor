"""
Unit tests for cross-leakage permeance calculations.

Tests the magnetoelasticsensor.permeance module against Fleming's equations.
"""

import math
import pytest
from magnetoelasticsensor.permeance import (
    cross_leakage_gu,
    cross_leakage_u_parameter,
    MU_0,
)
from magnetoelasticsensor.geometry import SensorGeometry, DEFAULT_SENSOR_GEOMETRY

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
        dimspagi = DEFAULT_SENSOR_GEOMETRY.dim_spag.nominal
        dimdp = DEFAULT_SENSOR_GEOMETRY.dim_dp.nominal  
        dimspi = DEFAULT_SENSOR_GEOMETRY.dim_sp.nominal

        # Call the function under test        
        u = cross_leakage_u_parameter(dimspagi, dimdp, dimspi)
        
        # Manual calculation in "Cross-leakage  permeance calculations" 
        # section in "UncertaintyChain.nb" notebook.
        expected = 10.68421052631579
        assert math.isclose(u, expected, rel_tol=1e-10)

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

    def test_full_calculation_workflow(self, dim_spagi, dim_dp, dim_spi, dim_sphi, dim_spahi, g2):
        """Test complete workflow from geometry to permeance."""
        
        # Calculate u parameter
        u = cross_leakage_u_parameter(dim_spagi, dim_dp, dim_spi)
        assert 1 < u <= 100
        
        # Calculate g_u coefficient
        gu = cross_leakage_gu(u)
        assert gu > 0
        
