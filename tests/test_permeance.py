"""
Unit tests for cross-leakage permeance calculations.

Tests the magnetoelasticsensor.permeance module against Fleming's equations.
"""

import math
import pytest
from magnetoelasticsensor.permeance import (
    cross_leakage_gu,
    cross_leakage_u_parameter,
    calculate_skin_depth,
    calculate_series_permeance,
    MU_0,
)
from magnetoelasticsensor.geometry import SensorGeometry, DEFAULT_SENSOR_GEOMETRY
from magnetoelasticsensor.air_gap_permeance import (
    AirGapPermeanceModel,
    calculate_air_gap_permeance,
)
from magnetoelasticsensor.target_permeance import (
    TargetPermeanceModel,
    calculate_target_permeance,
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


class TestSkinDepth:
    """Tests for eddy current skin depth calculation."""

    def test_skin_depth_nominal_geometry(self):
        
        """Test skin depth calculation with nominal geometry."""
        muo = DEFAULT_SENSOR_GEOMETRY.muo.nominal
        murt = DEFAULT_SENSOR_GEOMETRY.murt.nominal
        omega = DEFAULT_SENSOR_GEOMETRY.omega.nominal
        sigma_c = DEFAULT_SENSOR_GEOMETRY.sigmac.nominal
        
        delta = calculate_skin_depth(muo=muo, mur=murt, omega=omega, sigma_c=sigma_c)
        
        # Verify empirical formula: delta = sqrt(2) * sqrt(1 / (muo * mur * omega * sigma_c))
        expected = math.sqrt(2.0) * math.sqrt(1.0 / (muo * murt * omega * sigma_c))
        assert math.isclose(delta, expected, rel_tol=1e-10)

        # Sanity check against the 4140 shaft values in "SkinDepthStress.nb" notebook
        expected_delta = 0.00003338462250895936
        assert math.isclose(delta, expected_delta, rel_tol=1e-10)

    def test_skin_depth_returns_positive(self):
        """Test that skin depth returns positive values."""
        muo = DEFAULT_SENSOR_GEOMETRY.muo.nominal
        mur = DEFAULT_SENSOR_GEOMETRY.mur.nominal
        omega = DEFAULT_SENSOR_GEOMETRY.omega.nominal
        sigma_c = DEFAULT_SENSOR_GEOMETRY.sigmac.nominal
        
        delta = calculate_skin_depth(muo=muo, mur=mur, omega=omega, sigma_c=sigma_c)
        assert delta > 0

    def test_skin_depth_decreases_with_frequency(self):
        """Test that skin depth decreases with increasing frequency."""
        muo = DEFAULT_SENSOR_GEOMETRY.muo.nominal
        mur = DEFAULT_SENSOR_GEOMETRY.mur.nominal
        sigma_c = 1e6
        
        delta_low_freq = calculate_skin_depth(
            muo=muo, mur=mur, omega=2*math.pi*10e3, sigma_c=sigma_c
        )
        delta_high_freq = calculate_skin_depth(
            muo=muo, mur=mur, omega=2*math.pi*100e3, sigma_c=sigma_c
        )
        
        # Higher frequency → lower skin depth
        assert delta_low_freq > delta_high_freq

    def test_skin_depth_decreases_with_conductivity(self):
        """Test that skin depth decreases with increasing conductivity."""
        muo = DEFAULT_SENSOR_GEOMETRY.muo.nominal
        mur = DEFAULT_SENSOR_GEOMETRY.mur.nominal
        omega = DEFAULT_SENSOR_GEOMETRY.omega.nominal
        
        delta_low_sigma = calculate_skin_depth(
            muo=muo, mur=mur, omega=omega, sigma_c=5e5
        )
        delta_high_sigma = calculate_skin_depth(
            muo=muo, mur=mur, omega=omega, sigma_c=2e6
        )
        
        # Higher conductivity → lower skin depth
        assert delta_low_sigma > delta_high_sigma

    def test_skin_depth_decreases_with_permeability(self):
        """Test that skin depth decreases with increasing permeability."""
        muo = 4 * math.pi * 1e-7
        omega = 2 * math.pi * 50e3
        sigma_c = 1e6
        
        delta_low_mur = calculate_skin_depth(
            muo=muo, mur=500.0, omega=omega, sigma_c=sigma_c
        )
        delta_high_mur = calculate_skin_depth(
            muo=muo, mur=2000.0, omega=omega, sigma_c=sigma_c
        )
        
        # Higher permeability → lower skin depth
        assert delta_low_mur > delta_high_mur

    def test_skin_depth_raises_for_zero_muo(self):
        """Test that ValueError is raised for zero permeability."""
        with pytest.raises(ValueError, match="must all be positive"):
            calculate_skin_depth(muo=0, mur=1000.0, omega=2*math.pi*50e3, sigma_c=1e6)

    def test_skin_depth_raises_for_zero_mur(self):
        """Test that ValueError is raised for zero relative permeability."""
        with pytest.raises(ValueError, match="must all be positive"):
            calculate_skin_depth(muo=4*math.pi*1e-7, mur=0, omega=2*math.pi*50e3, sigma_c=1e6)

    def test_skin_depth_raises_for_zero_omega(self):
        """Test that ValueError is raised for zero frequency."""
        with pytest.raises(ValueError, match="must all be positive"):
            calculate_skin_depth(muo=4*math.pi*1e-7, mur=1000.0, omega=0, sigma_c=1e6)

    def test_skin_depth_raises_for_zero_sigma_c(self):
        """Test that ValueError is raised for zero conductivity."""
        with pytest.raises(ValueError, match="must all be positive"):
            calculate_skin_depth(muo=4*math.pi*1e-7, mur=1000.0, omega=2*math.pi*50e3, sigma_c=0)

    def test_skin_depth_raises_for_negative_muo(self):
        """Test that ValueError is raised for negative permeability."""
        with pytest.raises(ValueError, match="must all be positive"):
            calculate_skin_depth(muo=-4*math.pi*1e-7, mur=1000.0, omega=2*math.pi*50e3, sigma_c=1e6)

    def test_skin_depth_raises_for_negative_sigma_c(self):
        """Test that ValueError is raised for negative conductivity."""
        with pytest.raises(ValueError, match="must all be positive"):
            calculate_skin_depth(muo=4*math.pi*1e-7, mur=1000.0, omega=2*math.pi*50e3, sigma_c=-1e6)

    @pytest.mark.parametrize(
        "muo,mur,omega,sigma_c",
        [
            (4*math.pi*1e-7, 500.0, 2*math.pi*10e3, 1e6),
            (4*math.pi*1e-7, 1000.0, 2*math.pi*50e3, 5e5),
            (4*math.pi*1e-7, 2000.0, 2*math.pi*100e3, 2e6),
            (4*math.pi*1e-7, 1500.0, 2*math.pi*75e3, 1.5e6),
        ],
    )
    def test_skin_depth_parametric(self, muo, mur, omega, sigma_c):
        """Test skin depth calculation with various parameter combinations."""
        delta = calculate_skin_depth(muo=muo, mur=mur, omega=omega, sigma_c=sigma_c)
        assert delta > 0
        assert math.isfinite(delta)


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


class TestSeriesPermeance:
    """Tests for series permeance calculation."""

    def test_series_permeance_equal_values(self):
        """Test series permeance with equal permeance values."""
        p = 1e-8  # 10 nH
        result = calculate_series_permeance(pt=p, p_gapd=p, p_gaps=p)
        
        # For three equal permeances: 1/P_total = 1/P + 1/P + 1/P = 3/P
        # Therefore: P_total = P/3
        expected = p / 3.0
        assert math.isclose(result, expected, rel_tol=1e-10)

    def test_series_permeance_two_large_one_small(self):
        """Test that smallest permeance dominates in series."""
        p_large = 1e-6  # 1000 nH
        p_small = 1e-9  # 1 nH
        
        result = calculate_series_permeance(pt=p_large, p_gapd=p_large, p_gaps=p_small)
        
        # When one permeance is much smaller than others, it dominates
        # Result should be close to but less than p_small
        assert result < p_small
        assert result > 0

    def test_series_permeance_default_values(self):
        """Get geometry, calculate the permeance values."""

        """Test with realistic magnetoelastic sensor permeance values."""
        pt, p3 = calculate_target_permeance()
        p_gaps, p_gapd = calculate_air_gap_permeance()
        
        result = calculate_series_permeance(pt=pt, p_gapd=p_gapd, p_gaps=p_gaps)
        
        # Manual calculation: 1/result = 1/pt + 1/p_gapd + 1/p_gaps
        reciprocal_sum = (1.0/pt) + (1.0/p_gapd) + (1.0/p_gaps)
        expected = 1.0 / reciprocal_sum
        
        assert math.isclose(result, expected, rel_tol=1e-10)
        assert result > 0

        # The maths worked, validate against the "Effective Permeance" section in "UncertaintyChain.nb" notebook.
        expected_effective_permeance = 2.493130356444797e-8
        assert math.isclose(result, expected_effective_permeance, rel_tol=1e-8)

    def test_series_permeance_returns_positive(self):
        """Test that series permeance always returns positive values."""
        test_cases = [
            (1e-8, 1e-8, 1e-8),
            (1e-7, 5e-8, 2e-8),
            (1e-6, 1e-9, 1e-7),
        ]
        
        for pt, p_gapd, p_gaps in test_cases:
            result = calculate_series_permeance(pt=pt, p_gapd=p_gapd, p_gaps=p_gaps)
            assert result > 0

    def test_series_permeance_less_than_smallest(self):
        """Test that series permeance is always less than the smallest component."""
        pt = 1e-7
        p_gapd = 5e-8
        p_gaps = 2e-8
        
        result = calculate_series_permeance(pt=pt, p_gapd=p_gapd, p_gaps=p_gaps)
        
        # Series combination must be less than smallest component
        min_component = min(pt, p_gapd, p_gaps)
        assert result < min_component

    def test_series_permeance_raises_for_zero_pt(self):
        """Test that ValueError is raised when pt = 0."""
        with pytest.raises(ValueError, match="All permeances must be positive"):
            calculate_series_permeance(pt=0, p_gapd=1e-8, p_gaps=1e-8)

    def test_series_permeance_raises_for_zero_p_gapd(self):
        """Test that ValueError is raised when p_gapd = 0."""
        with pytest.raises(ValueError, match="All permeances must be positive"):
            calculate_series_permeance(pt=1e-8, p_gapd=0, p_gaps=1e-8)

    def test_series_permeance_raises_for_zero_p_gaps(self):
        """Test that ValueError is raised when p_gaps = 0."""
        with pytest.raises(ValueError, match="All permeances must be positive"):
            calculate_series_permeance(pt=1e-8, p_gapd=1e-8, p_gaps=0)

    def test_series_permeance_raises_for_negative_pt(self):
        """Test that ValueError is raised when pt < 0."""
        with pytest.raises(ValueError, match="All permeances must be positive"):
            calculate_series_permeance(pt=-1e-8, p_gapd=1e-8, p_gaps=1e-8)

    def test_series_permeance_raises_for_negative_p_gapd(self):
        """Test that ValueError is raised when p_gapd < 0."""
        with pytest.raises(ValueError, match="All permeances must be positive"):
            calculate_series_permeance(pt=1e-8, p_gapd=-1e-8, p_gaps=1e-8)

    def test_series_permeance_raises_for_negative_p_gaps(self):
        """Test that ValueError is raised when p_gaps < 0."""
        with pytest.raises(ValueError, match="All permeances must be positive"):
            calculate_series_permeance(pt=1e-8, p_gapd=1e-8, p_gaps=-1e-8)

    @pytest.mark.parametrize(
        "pt,p_gapd,p_gaps",
        [
            (1e-7, 1e-8, 5e-9),
            (5e-8, 2e-8, 1e-8),
            (1e-6, 1e-7, 1e-8),
            (1.9e-7, 4.5e-9, 3.2e-9),
        ],
    )
    def test_series_permeance_parametric(self, pt, p_gapd, p_gaps):
        """Test series permeance calculation with various parameter combinations."""
        result = calculate_series_permeance(pt=pt, p_gapd=p_gapd, p_gaps=p_gaps)
        
        # Verify result is positive and less than smallest component
        assert result > 0
        assert result < min(pt, p_gapd, p_gaps)
        assert math.isfinite(result)

    def test_series_permeance_formula_verification(self):
        """Verify the mathematical formula: P = 1/(1/Pt + 1/P_gapd + 1/P_gaps)."""
        pt = 1.5e-7
        p_gapd = 8e-9
        p_gaps = 6e-9
        
        result = calculate_series_permeance(pt=pt, p_gapd=p_gapd, p_gaps=p_gaps)
        
        # Direct formula calculation
        expected = 1.0 / ((1.0/pt) + (1.0/p_gapd) + (1.0/p_gaps))
        
        assert math.isclose(result, expected, rel_tol=1e-12)

