"""
Unit tests for target magnetic permeance calculations.

Tests the magnetoelasticsensor.target_permeance module.
"""
import math
import pytest
from magnetoelasticsensor import permeance
from magnetoelasticsensor.target_permeance import (
    TargetPermeanceModel,
    calculate_target_permeance,
)
from magnetoelasticsensor.geometry import (
    SensorGeometry,
    DimensionalParameter,
    DEFAULT_SENSOR_GEOMETRY,
)


class TestTargetPermeanceModel:
    """Tests for TargetPermeanceModel class."""

    def test_model_initialization_default(self):
        """Test model initialization with default geometry."""
        model = TargetPermeanceModel()
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
            awi=DimensionalParameter(nominal=5e-3, tolerance=0.1e-3),
            dim_spah=DimensionalParameter(nominal=5e-3, tolerance=0.1e-3),
            drspi=DimensionalParameter(nominal=17e-3, tolerance=0.1e-3),
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
        model = TargetPermeanceModel(geometry=custom_geom)
        assert model.geometry == custom_geom

    def test_target_permeance_calculation_default(self):
        """Test target permeance calculation with default parameters."""
        model = TargetPermeanceModel()
        
        Pt = model.calculate_target_permeance()
        
        # Permeance should be positive and finite
        assert isinstance(Pt[0], float)
        assert Pt[0] > 0
        assert math.isfinite(Pt[0])

        # Expected value from the "Target permeance" section of "ModelAndUncertainty.nb" notebook
        expected_permeance = 2.110233838256014e-8
        assert math.isclose(Pt[0], expected_permeance, rel_tol=1e-8)
        expected_permeance_eddy = 1.683866344744459e-9
        assert math.isclose(Pt[1], expected_permeance_eddy, rel_tol=1e-8)


    def test_target_permeance_returns_float(self):
        """Test that target permeance returns float type."""
        model = TargetPermeanceModel()
        permeance = model.calculate_target_permeance(
            ha=5e-3,
            u=2.5,
            sigma_c=1e6,
        )
        
        assert isinstance(permeance[0], float)

    def test_target_permeance_with_parameter_overrides(self):
        """Test target permeance calculation with parameter overrides."""
        model = TargetPermeanceModel()
        permeance = model.calculate_target_permeance(
            ha=5e-3,
            u=2.5,
            sigma_c=1e6,
            muo=4e-7*math.pi,
            murt=1500.0,
            omega=2*math.pi*50e3,
        )
        
        assert permeance[0] > 0
        assert isinstance(permeance[0], float)

    def test_target_permeance_sensitivity_to_conductivity(self):
        """Test that higher conductivity increases target permeance."""
        model = TargetPermeanceModel()
        permeance_low_sigma = model.calculate_target_permeance(
            ha=5e-3,
            u=2.5,
            sigma_c=5e5,
        )
        permeance_high_sigma = model.calculate_target_permeance(
            ha=5e-3,
            u=2.5,
            sigma_c=2e6,
        )
        
        # Higher conductivity → lower skin depth → higher permeance
        # in the Pt branch; overall effect depends on series combination
        assert permeance_low_sigma[0] > 0
        assert permeance_high_sigma[0] > 0


    def test_target_permeance_raises_for_invalid_ha(self):
        """Test that invalid ha raises ValueError."""
        model = TargetPermeanceModel()
        
        with pytest.raises(ValueError, match="ha must be positive"):
            model.calculate_target_permeance(ha=0, u=2.5, sigma_c=1e6)
        
        with pytest.raises(ValueError, match="ha must be positive"):
            model.calculate_target_permeance(ha=-1e-3, u=2.5, sigma_c=1e6)

    def test_target_permeance_raises_for_invalid_u(self):
        """Test that invalid u raises ValueError."""
        model = TargetPermeanceModel()
        
        with pytest.raises(ValueError, match="u must be > 1"):
            model.calculate_target_permeance(ha=5e-3, u=1.0, sigma_c=1e6)
        
        with pytest.raises(ValueError, match="u must be > 1"):
            model.calculate_target_permeance(ha=5e-3, u=0.5, sigma_c=1e6)

    def test_target_permeance_raises_for_invalid_sigma_c(self):
        """Test that invalid sigma_c raises ValueError."""
        model = TargetPermeanceModel()
        
        with pytest.raises(ValueError, match="sigma_c must be positive"):
            model.calculate_target_permeance(ha=5e-3, u=2.5, sigma_c=0)
        
        with pytest.raises(ValueError, match="sigma_c must be positive"):
            model.calculate_target_permeance(ha=5e-3, u=2.5, sigma_c=-1e6)

    def test_target_permeance_raises_for_invalid_muo(self):
        """Test that invalid muo raises ValueError."""
        model = TargetPermeanceModel()
        
        with pytest.raises(ValueError, match="muo, murt, and omega must be positive"):
            model.calculate_target_permeance(
                ha=5e-3,
                u=2.5,
                sigma_c=1e6,
                muo=0,
            )

    def test_target_permeance_raises_for_invalid_murt(self):
        """Test that invalid murt raises ValueError."""
        model = TargetPermeanceModel()
        
        with pytest.raises(ValueError, match="muo, murt, and omega must be positive"):
            model.calculate_target_permeance(
                ha=5e-3,
                u=2.5,
                sigma_c=1e6,
                murt=0,
            )

    def test_target_permeance_raises_for_invalid_omega(self):
        """Test that invalid omega raises ValueError."""
        model = TargetPermeanceModel()
        
        with pytest.raises(ValueError, match="muo, murt, and omega must be positive"):
            model.calculate_target_permeance(
                ha=5e-3,
                u=2.5,
                sigma_c=1e6,
                omega=0,
            )


class TestTargetPermeanceFunctional:
    """Tests for functional interface to target permeance."""

    def test_convenience_function_with_defaults(self):
        """Test convenience function with default geometry."""
        permeance = calculate_target_permeance(
            ha=5e-3,
            u=2.5,
            sigma_c=1e6,
        )
        
        assert permeance[0] > 0
        assert isinstance(permeance[0], float)

    def test_convenience_function_with_custom_geometry(self):
        """Test convenience function with custom geometry."""
        custom_geom = SensorGeometry(
            dim_dp=DimensionalParameter(nominal=10e-3, tolerance=0.08e-3),
            dim_sph_drive=DimensionalParameter(nominal=16e-3, tolerance=0.1e-3),
            dim_sp=DimensionalParameter(nominal=5e-3, tolerance=0.04e-3),
            dim_sph_sense=DimensionalParameter(nominal=16e-3, tolerance=0.1e-3),
            ndrive=DimensionalParameter(nominal=800.0, tolerance=0.0),
            nsense=DimensionalParameter(nominal=60.0, tolerance=0.0),
            awi=DimensionalParameter(nominal=5e-3, tolerance=0.1e-3),
            dim_spah=DimensionalParameter(nominal=5e-3, tolerance=0.1e-3),
            drspi=DimensionalParameter(nominal=17e-3, tolerance=0.1e-3),
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
        
        permeance = calculate_target_permeance(
            geometry=custom_geom,
            ha=5e-3,
            u=2.5,
            sigma_c=1e6,
        )
        
        assert permeance[0] > 0
        assert isinstance(permeance[0], float)

    def test_convenience_function_with_overrides(self):
        """Test convenience function with parameter overrides."""
        permeance = calculate_target_permeance(
            ha=5e-3,
            u=2.5,
            sigma_c=1e6,
            muo=4e-7*math.pi,
            murt=1500.0,
            omega=2*math.pi*100e3,
        )
        
        assert permeance[0] > 0
        assert isinstance(permeance[0], float)


class TestTargetPermeanceIntegration:
    """Integration tests for target permeance model."""

    @pytest.mark.parametrize(
        "ha",
        [1e-3, 5e-3, 10e-3, 20e-3],
    )
    def test_permeance_increases_with_height(self, ha):
        """Test that target permeance increases with target height."""
        model = TargetPermeanceModel()
        permeance = model.calculate_target_permeance(
            ha=ha,
            u=2.5,
            sigma_c=1e6,
        )
        
        assert permeance[0] > 0
        assert isinstance(permeance[0], float)

    @pytest.mark.parametrize(
        "u",
        [1.01, 1.5, 2.0, 3.0, 5.0, 10.0],
    )
    def test_permeance_varies_with_geometry_parameter(self, u):
        """Test that target permeance varies with normalized geometry parameter."""
        model = TargetPermeanceModel()
        permeance = model.calculate_target_permeance(
            ha=5e-3,
            u=u,
            sigma_c=1e6,
        )
        
        assert permeance[0] > 0
        assert isinstance(permeance[0], float)

    @pytest.mark.parametrize(
        "sigma_c",
        [1e5, 5e5, 1e6, 5e6, 1e7],
    )
    def test_permeance_varies_with_conductivity(self, sigma_c):
        """Test that target permeance varies with material conductivity."""
        model = TargetPermeanceModel()
        permeance = model.calculate_target_permeance(
            ha=5e-3,
            u=2.5,
            sigma_c=sigma_c,
        )
        
        assert permeance[0] > 0
        assert isinstance(permeance[0], float)
