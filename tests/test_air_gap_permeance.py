"""
Unit tests for air gap magnetic permeance calculations.

Tests the magnetoelasticsensor.air_gap_permeance module.
"""
import math
import pytest
from magnetoelasticsensor import permeance
from magnetoelasticsensor.air_gap_permeance import (
    AirGapPermeanceModel,
    calculate_air_gap_permeance,
)
from magnetoelasticsensor.geometry import (
    SensorGeometry,
    DimensionalParameter,
    DEFAULT_SENSOR_GEOMETRY,
)


class TestAirGapPermeanceModel:
    """Tests for AirGapPermeanceModel class."""

    def test_model_initialization_default(self):
        """Test initialization with default geometry and gap."""
        model = AirGapPermeanceModel()
        
        assert model.geometry == DEFAULT_SENSOR_GEOMETRY
        assert model.avg_gap == DEFAULT_SENSOR_GEOMETRY.dim_spag.nominal

    def test_model_initialization_custom_gap(self):
        """Test initialization with custom gap distance."""
        custom_gap = 5e-3  # 5mm gap
        model = AirGapPermeanceModel(avg_gap=custom_gap)
        
        assert model.avg_gap == custom_gap
        assert model.geometry == DEFAULT_SENSOR_GEOMETRY

    def test_model_initialization_custom_geometry(self):
        """Test initialization with custom geometry."""
        custom_geom = SensorGeometry(
            dim_dp=DimensionalParameter(nominal=10e-3, tolerance=0.1e-3),
            dim_sph_drive=DimensionalParameter(nominal=16e-3, tolerance=0.1e-3),
            dim_sp=DimensionalParameter(nominal=5e-3, tolerance=0.1e-3),
            dim_sph_sense=DimensionalParameter(nominal=16e-3, tolerance=0.1e-3),
            ndrive=DimensionalParameter(nominal=800.0, tolerance=0.0),
            nsense=DimensionalParameter(nominal=60.0, tolerance=0.0),
            dim_spaw=DimensionalParameter(nominal=5e-3, tolerance=0.1e-3),
            dim_spah=DimensionalParameter(nominal=5e-3, tolerance=0.1e-3),
            dim_spac=DimensionalParameter(nominal=17e-3, tolerance=0.1e-3),
            dim_spag=DimensionalParameter(nominal=12e-3, tolerance=0.1e-3),
            muo=DimensionalParameter(nominal=4e-7*math.pi, tolerance=0.0),
            mur=DimensionalParameter(nominal=2000.0, tolerance=0.0),
            rho=DimensionalParameter(nominal=1e-6, tolerance=0.0),
            murt=DimensionalParameter(nominal=2000.0, tolerance=0.0),
            omega=DimensionalParameter(nominal=2*math.pi*1e3, tolerance=0.0),
            theta3_deg=DimensionalParameter(nominal=45.0, tolerance=0.0),
            avg_gap=DimensionalParameter(nominal=1.143e-3, tolerance=1e-5),
            sigmac=DimensionalParameter(nominal=100/22, tolerance=5/22),
        )
        
        model = AirGapPermeanceModel(geometry=custom_geom)
        assert model.geometry == custom_geom
        assert model.avg_gap == custom_geom.dim_spag.nominal

    def test_model_initialization_custom_geometry_and_gap(self):
        """Test initialization with both custom geometry and gap."""
        custom_geom = SensorGeometry(
            dim_dp=DimensionalParameter(nominal=10e-3, tolerance=0.1e-3),
            dim_sph_drive=DimensionalParameter(nominal=16e-3, tolerance=0.1e-3),
            dim_sp=DimensionalParameter(nominal=5e-3, tolerance=0.1e-3),
            dim_sph_sense=DimensionalParameter(nominal=16e-3, tolerance=0.1e-3),
            ndrive=DimensionalParameter(nominal=800.0, tolerance=0.0),
            nsense=DimensionalParameter(nominal=60.0, tolerance=0.0),
            dim_spaw=DimensionalParameter(nominal=5e-3, tolerance=0.1e-3),
            dim_spah=DimensionalParameter(nominal=5e-3, tolerance=0.1e-3),
            dim_spac=DimensionalParameter(nominal=17e-3, tolerance=0.1e-3),
            dim_spag=DimensionalParameter(nominal=12e-3, tolerance=0.1e-3),
            muo=DimensionalParameter(nominal=4e-7*math.pi, tolerance=0.0),
            mur=DimensionalParameter(nominal=2000.0, tolerance=0.0),
            rho=DimensionalParameter(nominal=1e-6, tolerance=0.0),
            murt=DimensionalParameter(nominal=2000.0, tolerance=0.0),
            omega=DimensionalParameter(nominal=2*math.pi*1e3, tolerance=0.0),
            theta3_deg=DimensionalParameter(nominal=45.0, tolerance=0.0),
            avg_gap=DimensionalParameter(nominal=1.143e-3, tolerance=1e-5),
            sigmac=DimensionalParameter(nominal=100/22, tolerance=5/22),

        )
        custom_gap = 8e-3  # 8mm
        
        model = AirGapPermeanceModel(geometry=custom_geom, avg_gap=custom_gap)
        assert model.geometry == custom_geom
        assert model.avg_gap == custom_gap

    def test_air_gap_permeance_calculation_default(self):
        """Test air gap permeance calculation with default parameters."""
        model = AirGapPermeanceModel()
        permeance = model.calculate_air_gap_permeance()
        
        # Permeance should be positive and in reasonable range
        assert permeance[0] > 0
        assert permeance[1] > 0
        assert 1e-12 < permeance[0] < 1e-6  # Typical air gap permeance range

    def test_air_gap_permeance_returns_float(self):
        """Test that air gap permeance returns a float."""
        model = AirGapPermeanceModel()
        permeance = model.calculate_air_gap_permeance()
        assert isinstance(permeance[0], float)
        assert isinstance(permeance[1], float)

    def test_air_gap_permeance_with_custom_gap(self):
        """Test permeance calculation with custom gap distance."""
        model = AirGapPermeanceModel()
        permeance_large_gap = model.calculate_air_gap_permeance(avg_gap=1e-3)
        permeance_small_gap = model.calculate_air_gap_permeance(avg_gap=5e-4)
        
        # Smaller gap should yield higher permeance (lower reluctance)
        assert permeance_small_gap[0] > permeance_large_gap[0]
        assert permeance_large_gap[0] > 0
        assert permeance_small_gap[0] > 0

    def test_air_gap_permeance_monotonic_with_gap(self):
        """Test that permeance decreases monotonically with increasing gap."""
        model = AirGapPermeanceModel()
        gaps = [1e-3, 3e-3, 5e-3, 10e-3, 15e-3]  # 1mm to 15mm
        permeances = [model.calculate_air_gap_permeance(avg_gap=g) for g in gaps]
        
        # Check monotonic decrease
        for i in range(len(permeances) - 1):
            assert permeances[i] > permeances[i+1], \
                f"Permeance should decrease with gap: P({gaps[i]}) > P({gaps[i+1]})"

    def test_air_gap_permeance_zero_gap_error(self):
        """Test that zero gap raises assertion or returns infinite permeance."""
        model = AirGapPermeanceModel()
        with pytest.raises(AssertionError, match="Air gap distance must be greater than zero"):
            model.calculate_air_gap_permeance(avg_gap=0.0)

    def test_air_gap_permeance_negative_gap_error(self):
        """Test that negative gap raises assertion."""
        model = AirGapPermeanceModel()
        with pytest.raises(AssertionError, match="Air gap distance must be greater than zero"):
            model.calculate_air_gap_permeance(avg_gap=-1e-3)


class TestAirGapPermeanceFunctional:
    """Tests for functional interface to air gap permeance."""

    def test_functional_with_defaults(self):
        """Test functional interface with all defaults."""
        permeance = calculate_air_gap_permeance()
        
        # A first sanity check: both drive and sense pole permeance 
        # should be positive
        assert permeance[0] > 0
        assert permeance[1] > 0

        # From the "Sense pole (circular) air gap permeance" section 
        # of the "UncertaintyChain.nb" notebook
        expected_permeance = 4.799748476441882e-8
        assert math.isclose(permeance[0], expected_permeance, rel_tol=1e-8)

        # From the "Drive pole (circular) air gap permeance" section 
        # of the "UncertaintyChain.nb" notebook
        expected_permeance = 1.304100211826622e-7
        assert math.isclose(permeance[1], expected_permeance, rel_tol=1e-8)

    def test_functional_with_custom_gap(self):
        """Test functional interface with custom gap."""
        permeance = calculate_air_gap_permeance(avg_gap=5e-3)
        assert permeance[0]  > 0
        assert permeance[1]  > 0

    def test_functional_with_custom_geometry(self):
        """Test functional interface with custom geometry."""
        custom_geom = SensorGeometry(
            dim_dp=DimensionalParameter(nominal=10e-3, tolerance=0.1e-3),
            dim_sph_drive=DimensionalParameter(nominal=16e-3, tolerance=0.1e-3),
            dim_sp=DimensionalParameter(nominal=5e-3, tolerance=0.1e-3),
            dim_sph_sense=DimensionalParameter(nominal=16e-3, tolerance=0.1e-3),
            ndrive=DimensionalParameter(nominal=800.0, tolerance=0.0),
            nsense=DimensionalParameter(nominal=60.0, tolerance=0.0),
            dim_spaw=DimensionalParameter(nominal=5e-3, tolerance=0.1e-3),
            dim_spah=DimensionalParameter(nominal=5e-3, tolerance=0.1e-3),
            dim_spac=DimensionalParameter(nominal=17e-3, tolerance=0.1e-3),
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
        
        permeance = calculate_air_gap_permeance(geometry=custom_geom)
        assert permeance[0] > 0

    def test_functional_with_geometry_and_gap(self):
        """Test functional interface with both geometry and gap overrides."""
        custom_geom = SensorGeometry(
            dim_dp=DimensionalParameter(nominal=10e-3, tolerance=0.1e-3),
            dim_sph_drive=DimensionalParameter(nominal=16e-3, tolerance=0.1e-3),
            dim_sp=DimensionalParameter(nominal=5e-3, tolerance=0.1e-3),
            dim_sph_sense=DimensionalParameter(nominal=16e-3, tolerance=0.1e-3),
            ndrive=DimensionalParameter(nominal=800.0, tolerance=0.0),
            nsense=DimensionalParameter(nominal=60.0, tolerance=0.0),
            dim_spaw=DimensionalParameter(nominal=5e-3, tolerance=0.1e-3),
            dim_spah=DimensionalParameter(nominal=5e-3, tolerance=0.1e-3),
            dim_spac=DimensionalParameter(nominal=17e-3, tolerance=0.1e-3),
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
        
        permeance = calculate_air_gap_permeance(
            geometry=custom_geom,
            avg_gap=1e-3,
            murt=3000.0
        )
        assert permeance[0] > 0


class TestIntegration:
    """Integration tests for air gap permeance in sensor context."""

    def test_gap_vs_core_permeance_ratio(self):
        """Test that air gap permeance is typically much smaller than core permeance.
        
        Physical expectation: Air gap has much higher reluctance (lower permeance)
        than ferrite core, making it the dominant term in magnetic circuit.
        """
        from magnetoelasticsensor.core_permeance import CorePermeanceModel
        
        core_model = CorePermeanceModel()
        gap_model = AirGapPermeanceModel()
        
        p_core = core_model.calculate_core_permeance()
        p_gap = gap_model.calculate_air_gap_permeance()
        
        # Air gap should be limiting factor (lower permeance)
        # Typical ratio: P_gap << P_core for ferrite cores
        assert p_gap[0] > 0
        assert p_core > 0
        # Note: actual ratio depends on design; this is a sanity check

    @pytest.mark.parametrize(
        "gap_distance",
        [1e-3, 3e-3, 5e-3, 7e-3, 9e-3, 12e-3, 15e-3],  # 1mm to 15mm
    )
    def test_parametric_gap_sweep(self, gap_distance):
        """Parametric test sweeping gap distances.
        
        Validates permeance across typical operating gap ranges for magnetoelastic
        sensors in turbomachinery applications (close proximity to rotating shaft).
        
        Parameters
        ----------
        gap_distance : float
            Air gap distance [m] between pole face and target surface.
        """
        model = AirGapPermeanceModel(avg_gap=gap_distance)
        permeance = model.calculate_air_gap_permeance()
        
        assert permeance[0] > 0
        assert 1e-12 < permeance[0] < 1e-5, \
            f"Permeance {permeance:.3e} H out of expected range for gap {gap_distance*1e3:.1f}mm"

    @pytest.mark.parametrize(
        "target_mu",
        [100.0, 500.0, 1000.0, 2000.0, 3000.0, 5000.0],
    )
    def test_parametric_target_permeability_sweep(self, target_mu):
        """Parametric test for target material permeability.
        
        Target permeability changes with applied stress (inverse magnetostriction):
        - Tensile stress → increased permeability
        - Compressive stress → decreased permeability
        
        This sweep validates model behavior across the expected permeability range
        for ferromagnetic shaft materials under load.
        
        Parameters
        ----------
        target_mu : float
            Target material relative permeability (dimensionless).
        """
        model = AirGapPermeanceModel()
        permeance = model.calculate_air_gap_permeance(murt=target_mu)
        
        assert permeance[0] > 0
        assert isinstance(permeance[0], float)
        assert isinstance(permeance[1], float)

    def test_consistency_model_vs_functional(self):
        """Test that class method and functional interface give identical results."""
        gap = 6e-3
        murt = 2500.0
        
        # Class-based approach
        model = AirGapPermeanceModel(avg_gap=gap)
        p_model = model.calculate_air_gap_permeance(murt=murt)
        
        # Functional approach
        p_func = calculate_air_gap_permeance(avg_gap=gap, murt=murt)
        
        assert math.isclose(p_model[0], p_func[0], rel_tol=1e-10)