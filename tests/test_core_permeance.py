"""
Unit tests for core magnetic permeance calculations.

Tests the magnetoelasticsensor.core_permeance module.
"""

import math
import pytest
from magnetoelasticsensor.core_permeance import (
    CorePermeanceModel,
    calculate_core_permeance_simple,
    MU_0,
)
from magnetoelasticsensor.geometry import (
    SensorGeometry,
    DimensionalParameter,
    DEFAULT_SENSOR_GEOMETRY,
)


class TestDimensionalParameter:
    """Tests for DimensionalParameter class."""

    def test_dimensional_parameter_creation(self):
        """Test creating a dimensional parameter."""
        param = DimensionalParameter(nominal=10e-3, tolerance=0.1e-3)
        assert param.nominal == 10e-3
        assert param.tolerance == 0.1e-3

    def test_dimensional_parameter_min_max(self):
        """Test min/max bounds of dimensional parameter."""
        param = DimensionalParameter(nominal=10e-3, tolerance=0.1e-3)
        assert param.min == pytest.approx(9.9e-3)
        assert param.max == pytest.approx(10.1e-3)

    def test_dimensional_parameter_repr(self):
        """Test string representation of dimensional parameter."""
        param = DimensionalParameter(nominal=10e-3, tolerance=0.1e-3)
        repr_str = repr(param)
        assert "10.00mm" in repr_str
        assert "0.10mm" in repr_str


class TestSensorGeometry:
    """Tests for SensorGeometry class."""

    def test_default_geometry_creation(self):
        """Test that default sensor geometry is properly configured."""
        geom = DEFAULT_SENSOR_GEOMETRY
        
        # Drive pole
        assert geom.dim_dp.nominal == pytest.approx(9.50e-3)
        assert geom.dim_sph_drive.nominal == pytest.approx(15.0e-3)
        
        # Sense pole
        assert geom.dim_sp.nominal == pytest.approx(4.50e-3)
        assert geom.dim_sph_sense.nominal == pytest.approx(15.0e-3)
        
        # Bridge
        assert geom.dim_spaw.nominal == pytest.approx(4.50e-3)
        assert geom.dim_spah.nominal == pytest.approx(4.25e-3)
        assert geom.dim_spac.nominal == pytest.approx(16.0e-3)
        
        # Gap
        assert geom.dim_spag.nominal == pytest.approx(9.00e-3)

    def test_geometry_tolerances(self):
        """Test that tolerances are properly set."""
        geom = DEFAULT_SENSOR_GEOMETRY
        
        # Check some key tolerances
        assert geom.dim_dp.tolerance == pytest.approx(0.08e-3)
        assert geom.dim_spag.tolerance == pytest.approx(0.10e-3)

    def test_custom_geometry_creation(self):
        """Test creating custom sensor geometry."""
        custom_geom = SensorGeometry(
            dim_dp=DimensionalParameter(nominal=10e-3, tolerance=0.1e-3),
            dim_sph_drive=DimensionalParameter(nominal=16e-3, tolerance=0.1e-3),
            dim_sp=DimensionalParameter(nominal=5e-3, tolerance=0.1e-3),
            dim_sph_sense=DimensionalParameter(nominal=16e-3, tolerance=0.1e-3),
            dim_spaw=DimensionalParameter(nominal=5e-3, tolerance=0.1e-3),
            dim_spah=DimensionalParameter(nominal=5e-3, tolerance=0.1e-3),
            dim_spac=DimensionalParameter(nominal=17e-3, tolerance=0.1e-3),
            dim_spag=DimensionalParameter(nominal=10e-3, tolerance=0.1e-3),
        )
        
        assert custom_geom.dim_dp.nominal == 10e-3
        assert custom_geom.dim_sp.nominal == 5e-3

    def test_geometry_repr(self):
        """Test string representation of geometry."""
        geom = DEFAULT_SENSOR_GEOMETRY
        repr_str = repr(geom)
        
        assert "SensorGeometry" in repr_str
        assert "Drive pole" in repr_str
        assert "Sense pole" in repr_str
        assert "Bridge (arm)" in repr_str


class TestCorePermeanceModel:
    """Tests for CorePermeanceModel class."""

    def test_model_initialization_default(self):
        """Test CorePermeanceModel initialization with default geometry."""
        model = CorePermeanceModel()
        assert model.geometry is not None
        assert model.geometry == DEFAULT_SENSOR_GEOMETRY

    def test_model_initialization_custom_geometry(self):
        """Test CorePermeanceModel initialization with custom geometry."""
        custom_geom = SensorGeometry(
            dim_dp=DimensionalParameter(nominal=10e-3, tolerance=0.1e-3),
            dim_sph_drive=DimensionalParameter(nominal=16e-3, tolerance=0.1e-3),
            dim_sp=DimensionalParameter(nominal=5e-3, tolerance=0.1e-3),
            dim_sph_sense=DimensionalParameter(nominal=16e-3, tolerance=0.1e-3),
            dim_spaw=DimensionalParameter(nominal=5e-3, tolerance=0.1e-3),
            dim_spah=DimensionalParameter(nominal=5e-3, tolerance=0.1e-3),
            dim_spac=DimensionalParameter(nominal=17e-3, tolerance=0.1e-3),
            dim_spag=DimensionalParameter(nominal=10e-3, tolerance=0.1e-3),
        )
        
        model = CorePermeanceModel(geometry=custom_geom)
        assert model.geometry == custom_geom

    def test_core_permeance_calculation_default(self):
        """Test core permeance calculation with default parameters."""
        model = CorePermeanceModel()
        permeance = model.calculate_core_permeance()
        
        # Permeance should be positive and in reasonable range
        assert permeance > 0
        assert 1e-9 < permeance < 1e-4  # Typical core inductance range

    def test_core_permeance_returns_float(self):
        """Test that core permeance returns a float."""
        model = CorePermeanceModel()
        permeance = model.calculate_core_permeance()
        assert isinstance(permeance, float)

    def test_core_permeance_with_custom_mu_target(self):
        """Test core permeance calculation with custom target permeability."""
        model = CorePermeanceModel()
        
        # Higher permeability should give higher permeance
        permeance_1000 = model.calculate_core_permeance(mu_target=1000.0)
        permeance_500 = model.calculate_core_permeance(mu_target=500.0)
        
        # Permeance proportional to permeability
        assert permeance_1000 > permeance_500

    def test_core_permeance_with_stress_input(self):
        """Test that core permeance accepts stress input."""
        model = CorePermeanceModel()
        
        # Should not raise exception with stress input
        permeance = model.calculate_core_permeance(stress=100e6)  # 100 MPa
        assert permeance > 0

    def test_core_permeance_low_mu_target(self):
        """Test core permeance with low target permeability."""
        model = CorePermeanceModel()
        permeance = model.calculate_core_permeance(mu_target=10.0)
        
        # Still should be positive
        assert permeance > 0

    def test_core_permeance_high_mu_target(self):
        """Test core permeance with high target permeability."""
        model = CorePermeanceModel()
        permeance = model.calculate_core_permeance(mu_target=10000.0)
        
        assert permeance > 0


class TestCorePe‌rmeanceFunctional:
    """Tests for functional interface to core permeance."""

    def test_simple_permeance_calculation_default(self):
        """Test simple functional interface with defaults."""
        permeance = calculate_core_permeance_simple()
        
        assert permeance > 0
        assert 1e-9 < permeance < 1e-4

    def test_simple_permeance_with_geometry(self):
        """Test simple functional interface with custom geometry."""
        custom_geom = SensorGeometry(
            dim_dp=DimensionalParameter(nominal=10e-3, tolerance=0.1e-3),
            dim_sph_drive=DimensionalParameter(nominal=16e-3, tolerance=0.1e-3),
            dim_sp=DimensionalParameter(nominal=5e-3, tolerance=0.1e-3),
            dim_sph_sense=DimensionalParameter(nominal=16e-3, tolerance=0.1e-3),
            dim_spaw=DimensionalParameter(nominal=5e-3, tolerance=0.1e-3),
            dim_spah=DimensionalParameter(nominal=5e-3, tolerance=0.1e-3),
            dim_spac=DimensionalParameter(nominal=17e-3, tolerance=0.1e-3),
            dim_spag=DimensionalParameter(nominal=10e-3, tolerance=0.1e-3),
        )
        
        permeance = calculate_core_permeance_simple(geometry=custom_geom)
        assert permeance > 0

    def test_simple_permeance_with_parameters(self):
        """Test simple functional interface with custom parameters."""
        permeance = calculate_core_permeance_simple(
            mu_target=2000.0,
            stress=50e6
        )
        
        assert permeance > 0


class TestIntegration:
    """Integration tests combining geometry and permeance calculations."""

    def test_model_with_default_geometry(self):
        """Test that model can be created and used with default geometry."""
        model = CorePermeanceModel()
        
        # Get geometry details
        geom = model.geometry
        assert geom.dim_dp.nominal > 0
        assert geom.dim_sp.nominal > 0
        
        # Calculate permeance
        permeance = model.calculate_core_permeance()
        assert permeance > 0

    @pytest.mark.parametrize(
        "mu_target",
        [100.0, 500.0, 1000.0, 2000.0, 5000.0],
    )
    def test_permeance_parametric_mu_target(self, mu_target):
        """Parametric test for various target permeabilities."""
        model = CorePermeanceModel()
        permeance = model.calculate_core_permeance(mu_target=mu_target)
        
        assert permeance > 0
        # Permeance should scale with permeability
        assert 1e-9 < permeance < 1e-4

    @pytest.mark.parametrize(
        "stress",
        [0.0, 50e6, 100e6, -50e6, -100e6],  # Tensile and compressive
    )
    def test_permeance_parametric_stress(self, stress):
        """Parametric test for various stress levels."""
        model = CorePermeanceModel()
        permeance = model.calculate_core_permeance(stress=stress)
        
        assert permeance > 0

    def test_geometry_consistency_default_vs_direct(self):
        """Test that default geometry is consistent."""
        model1 = CorePermeanceModel()
        model2 = CorePermeanceModel(geometry=DEFAULT_SENSOR_GEOMETRY)
        
        permeance1 = model1.calculate_core_permeance()
        permeance2 = model2.calculate_core_permeance()
        
        assert math.isclose(permeance1, permeance2, rel_tol=1e-10)


class TestPhysicalConstants:
    """Tests for physical constants."""

    def test_mu0_value(self):
        """Test that μ₀ has correct SI value."""
        expected_mu0 = 4 * math.pi * 1e-7
        assert math.isclose(MU_0, expected_mu0, rel_tol=1e-10)
