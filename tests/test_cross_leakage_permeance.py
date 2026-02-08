"""
Unit tests for cross-leakage magnetic permeance calculations.

Tests the magnetoelasticsensor.cross_leakage_permeance module.
"""
import math
import pytest
from magnetoelasticsensor.cross_leakage_permeance import (
    CrossLeakagePermeanceModel
)
from magnetoelasticsensor.geometry import (
    SensorGeometry,
    DimensionalParameter,
    DEFAULT_SENSOR_GEOMETRY,
)


class TestCrossLeakagePermeanceModel:
    """Tests for CrossLeakagePermeanceModel class."""

    def test_model_initialization_default(self):
        """Test model initialization with default geometry."""
        model = CrossLeakagePermeanceModel()
        assert model.geometry is not None
        assert model.geometry == DEFAULT_SENSOR_GEOMETRY

    def test_model_initialization_custom_geometry(self):
        """Test model initialization with custom geometry."""
        custom_geom = SensorGeometry(
            dim_dp=DimensionalParameter(nominal=10e-3, tolerance=0.08e-3),
            dim_sph_drive=DimensionalParameter(nominal=16e-3, tolerance=0.1e-3),
            dim_sp=DimensionalParameter(nominal=5e-3, tolerance=0.04e-3),
            dim_sph_sense=DimensionalParameter(nominal=16e-3, tolerance=0.1e-3),
            ndrive=DimensionalParameter(nominal=800.0, tolerance=0.0),
            nsense=DimensionalParameter(nominal=60.0, tolerance=0.0),
            dim_spaw=DimensionalParameter(nominal=5e-3, tolerance=0.1e-3),
            dim_spah=DimensionalParameter(nominal=5e-3, tolerance=0.1e-3),
            dim_spac=DimensionalParameter(nominal=17e-3, tolerance=0.1e-3),
            dim_spag=DimensionalParameter(nominal=10e-3, tolerance=0.10e-3),
            muo=DimensionalParameter(nominal=4e-7*math.pi, tolerance=0.0),
            mur=DimensionalParameter(nominal=2000.0, tolerance=0.0),
            rho=DimensionalParameter(nominal=1e-6, tolerance=0.0),
            murt=DimensionalParameter(nominal=2000.0, tolerance=0.0),
            omega=DimensionalParameter(nominal=2*math.pi*1e3, tolerance=0.0),
            theta3_deg=DimensionalParameter(nominal=45.0, tolerance=0.0),
            avg_gap=DimensionalParameter(nominal=1.143e-3, tolerance=1e-5),
            sigmac=DimensionalParameter(nominal=100/22, tolerance=5/22),
        )
        model = CrossLeakagePermeanceModel(geometry=custom_geom)
        assert model.geometry == custom_geom

    def test_cross_leakage_permeance_calculation_default(self):
        """Test cross-leakage permeance calculation with default parameters."""
        model = CrossLeakagePermeanceModel()
        permeance = model.calculate_cross_leakage_permeance()
        
        # Super basic sanity checks
        assert isinstance(permeance, float)
        assert permeance > 0

        # From "Cross-leakage  permeance calculations" section in "ModelAndUncertainty.nb" notebook,
        expected_permeance = 2.329754661676527e-8 
        assert math.isclose(permeance, expected_permeance, rel_tol=1e-8)

    def test_cross_leakage_permeance_returns_float(self):
        """Test that cross-leakage permeance returns float type."""
        model = CrossLeakagePermeanceModel()
        permeance = model.calculate_cross_leakage_permeance()
        
        assert isinstance(permeance, float)

    def test_cross_leakage_with_parameter_overrides(self):
        """Test cross-leakage calculation with all parameters overridden."""
        model = CrossLeakagePermeanceModel()
        permeance = model.calculate_cross_leakage_permeance(
            muo=4e-7*math.pi,
        )
        
        assert permeance > 0
        assert isinstance(permeance, float)


class TestCrossLeakagePermeanceFunctional:
    """Tests for functional interface to cross-leakage permeance."""

    def test_simple_permeance_with_default_geometry(self):
        """Test convenience function with default geometry."""
        model = CrossLeakagePermeanceModel()
        permeance = model.calculate_cross_leakage_permeance()
        
        assert permeance > 0
        assert isinstance(permeance, float)

    def test_convenience_function_with_geometry(self):
        """Test convenience function with custom geometry."""
        custom_geom = SensorGeometry(
            dim_dp=DimensionalParameter(nominal=10e-3, tolerance=0.08e-3),
            dim_sph_drive=DimensionalParameter(nominal=16e-3, tolerance=0.1e-3),
            dim_sp=DimensionalParameter(nominal=5e-3, tolerance=0.04e-3),
            dim_sph_sense=DimensionalParameter(nominal=16e-3, tolerance=0.1e-3),
            ndrive=DimensionalParameter(nominal=800.0, tolerance=0.0),
            nsense=DimensionalParameter(nominal=60.0, tolerance=0.0),
            dim_spaw=DimensionalParameter(nominal=5e-3, tolerance=0.1e-3),
            dim_spah=DimensionalParameter(nominal=5e-3, tolerance=0.1e-3),
            dim_spac=DimensionalParameter(nominal=17e-3, tolerance=0.1e-3),
            dim_spag=DimensionalParameter(nominal=10e-3, tolerance=0.10e-3),
            muo=DimensionalParameter(nominal=4e-7*math.pi, tolerance=0.0),
            mur=DimensionalParameter(nominal=2000.0, tolerance=0.0),
            rho=DimensionalParameter(nominal=1e-6, tolerance=0.0),
            murt=DimensionalParameter(nominal=2000.0, tolerance=0.0),
            omega=DimensionalParameter(nominal=2*math.pi*1e3, tolerance=0.0),
            theta3_deg=DimensionalParameter(nominal=45.0, tolerance=0.0),
            avg_gap=DimensionalParameter(nominal=1.143e-3, tolerance=1e-5),
            sigmac=DimensionalParameter(nominal=100/22, tolerance=5/22),
        )
        model = CrossLeakagePermeanceModel(geometry=custom_geom)
        permeance = model.calculate_cross_leakage_permeance()
        
        assert permeance > 0




