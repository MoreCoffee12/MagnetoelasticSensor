"""
Unit tests for core magnetic permeance calculations.

Tests the magnetoelasticsensor.core_permeance module.
"""

import math
import pytest
from magnetoelasticsensor.core_permeance import (
    CorePermeanceModel
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
        assert geom.awi.nominal == pytest.approx(4.50e-3)
        assert geom.dim_spah.nominal == pytest.approx(4.25e-3)
        assert geom.drspi.nominal == pytest.approx(16.0e-3)
        
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
            ndrive=DimensionalParameter(nominal=800.0, tolerance=0.0),
            nsense=DimensionalParameter(nominal=60.0, tolerance=0.0),
            awi=DimensionalParameter(nominal=5e-3, tolerance=0.1e-3),
            dim_spah=DimensionalParameter(nominal=5e-3, tolerance=0.1e-3),
            drspi=DimensionalParameter(nominal=17e-3, tolerance=0.1e-3),
            dim_spag=DimensionalParameter(nominal=10e-3, tolerance=0.1e-3),
            muo=DimensionalParameter(nominal=4e-7*math.pi, tolerance=0.0),
            mur=DimensionalParameter(nominal=2000.0, tolerance=0.0),
            rho=DimensionalParameter(nominal=1e-6, tolerance=0.0),
            murt=DimensionalParameter(nominal=2000.0, tolerance=0.0),
            omega=DimensionalParameter(nominal=2*math.pi*1e3, tolerance=0.0),
            theta3_deg=DimensionalParameter(nominal=45.0, tolerance=0.0),
            avg_gap=DimensionalParameter(nominal=1.143e-3, tolerance=1e-5),
            sigmac=DimensionalParameter(nominal=100/22, tolerance=5/22),
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
            ndrive=DimensionalParameter(nominal=800.0, tolerance=0.0),
            nsense=DimensionalParameter(nominal=60.0, tolerance=0.0),
            awi=DimensionalParameter(nominal=5e-3, tolerance=0.1e-3),
            dim_spah=DimensionalParameter(nominal=5e-3, tolerance=0.1e-3),
            drspi=DimensionalParameter(nominal=17e-3, tolerance=0.1e-3),
            dim_spag=DimensionalParameter(nominal=10e-3, tolerance=0.1e-3),
            muo=DimensionalParameter(nominal=4e-7*math.pi, tolerance=0.0),
            mur=DimensionalParameter(nominal=2000.0, tolerance=0.0),
            rho=DimensionalParameter(nominal=1e-6, tolerance=0.0),
            murt=DimensionalParameter(nominal=2000.0, tolerance=0.0),
            omega=DimensionalParameter(nominal=2*math.pi*1e3, tolerance=0.0),
            theta3_deg=DimensionalParameter(nominal=45.0, tolerance=0.0),
            avg_gap=DimensionalParameter(nominal=1.143e-3, tolerance=1e-5),
            sigmac=DimensionalParameter(nominal=100/22, tolerance=5/22),    
        )
        
        model = CorePermeanceModel(geometry=custom_geom)
        assert model.geometry == custom_geom

    def test_core_permeance_calculation_default(self):
        """Test core permeance calculation with default parameters."""
        model = CorePermeanceModel()
        permeance = model.calculate_core_permeance()
        
        # This is from the section "Combined permeances" in the "ModelAndUncertainty.nb" notebook
        d_permeance_expected = 1.261860054772294e-6
        assert math.isclose(d_permeance_expected, permeance, rel_tol=1e-8)

    def test_core_permeance_returns_float(self):
        """Test that core permeance returns a float."""
        model = CorePermeanceModel()
        permeance = model.calculate_core_permeance()
        assert isinstance(permeance, float)



class TestCorePermeanceFunctional:
    """Tests for functional interface to core permeance."""

    def test_simple_permeance_with_geometry(self):
        """Test simple functional interface with custom geometry."""
        custom_geom = SensorGeometry(
            dim_dp=DimensionalParameter(nominal=10e-3, tolerance=0.1e-3),
            dim_sph_drive=DimensionalParameter(nominal=16e-3, tolerance=0.1e-3),
            dim_sp=DimensionalParameter(nominal=5e-3, tolerance=0.1e-3),
            dim_sph_sense=DimensionalParameter(nominal=16e-3, tolerance=0.1e-3),
            ndrive=DimensionalParameter(nominal=800.0, tolerance=0.0),
            nsense=DimensionalParameter(nominal=60.0, tolerance=0.0),
            awi=DimensionalParameter(nominal=5e-3, tolerance=0.1e-3),
            dim_spah=DimensionalParameter(nominal=5e-3, tolerance=0.1e-3),
            drspi=DimensionalParameter(nominal=17e-3, tolerance=0.1e-3),
            dim_spag=DimensionalParameter(nominal=10e-3, tolerance=0.1e-3),
            muo=DimensionalParameter(nominal=4e-7*math.pi, tolerance=0.0),
            mur=DimensionalParameter(nominal=2000.0, tolerance=0.0),
            rho=DimensionalParameter(nominal=1e-6, tolerance=0.0),
            murt=DimensionalParameter(nominal=2000.0, tolerance=0.0),
            omega=DimensionalParameter(nominal=2*math.pi*1e3, tolerance=0.0),
            theta3_deg=DimensionalParameter(nominal=45.0, tolerance=0.0),
            avg_gap=DimensionalParameter(nominal=1.143e-3, tolerance=1e-5),
            sigmac=DimensionalParameter(nominal=100/22, tolerance=5/22),    
        )
        
        permeance = CorePermeanceModel(geometry=custom_geom).calculate_core_permeance()
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
        "mu_core",
        [100.0, 500.0, 1000.0, 2000.0, 5000.0],
    )
    def test_permeance_parametric_mu_core(self, mu_core):
        """Parametric test for various core permeabilities."""
        model = CorePermeanceModel()
        permeance = model.calculate_core_permeance(mur=mu_core)
        
        assert permeance > 0
        # Permeance should scale with permeability
        assert 1e-9 < permeance < 1e-4

    @pytest.mark.parametrize(
        "omega_op",
        [f * 2 * math.pi for f in [1000, 5000, 10000, 20000, 50000, 70000, 100000]],  # Low to high frequencies [rad/s]
    )
    def test_permeance_parametric_omega(self, omega_op):
        """Parametric test for various frequency levels."""
        model = CorePermeanceModel()
        permeance = model.calculate_core_permeance(omega=omega_op)
        
        assert permeance > 0

    def test_geometry_consistency_default_vs_direct(self):
        """Test that default geometry is consistent."""
        model1 = CorePermeanceModel()
        model2 = CorePermeanceModel(geometry=DEFAULT_SENSOR_GEOMETRY)
        
        permeance1 = model1.calculate_core_permeance()
        permeance2 = model2.calculate_core_permeance()
        
        assert math.isclose(permeance1, permeance2, rel_tol=1e-10)


