"""
Sensor geometry and dimensional parameters for magnetoelastic sensor modeling.

All dimensions stored in SI units (meters) with nominal values and tolerances.
Reference architecture: Single-branch magnetoelastic sensor with ferrite core.
"""

from dataclasses import dataclass


@dataclass
class DimensionalParameter:
    """Represents a dimensional parameter with nominal value and tolerance."""
    
    nominal: float  # Nominal dimension [m]
    tolerance: float  # ± tolerance [m]
    
    @property
    def min(self) -> float:
        """Minimum dimension within tolerance."""
        return self.nominal - self.tolerance
    
    @property
    def max(self) -> float:
        """Maximum dimension within tolerance."""
        return self.nominal + self.tolerance
    
    def __repr__(self) -> str:
        return (
            f"{self.nominal*1e3:.2f}mm ± {self.tolerance*1e3:.2f}mm "
            f"({self.nominal*39.37:.2f}in ± {self.tolerance*39.37:.3f}in)"
        )


@dataclass
class SensorGeometry:
    """
    Sensor geometry parameters for magnetoelastic cross-architecture sensor.
    
    Based on Fleming's magnetic circuit design with ferrite core structure.
    The sensor architecture features:
    - Drive pole: Primary magnetic path excitation
    - Sense pole: Secondary signal pickup
    - Bridge (pole arm): Mechanical connection and flux path
    - Target: Stress-sensing element (external rotor/shaft)
    
    References
    ----------
    Fleming equations for magnetic circuit analysis
    See README.md for architecture overview
    """
    
    # Drive pole (primary coil connection)
    dim_dp: DimensionalParameter  # Drive pole diameter
    dim_sph_drive: DimensionalParameter  # Drive pole height
    
    # Sense pole (secondary coil connection)
    dim_sp: DimensionalParameter  # Sense pole diameter
    dim_sph_sense: DimensionalParameter  # Sense pole height
    
    # Bridge / Pole arm (ferrite structure connecting poles)
    dim_spaw: DimensionalParameter  # Bridge width
    dim_spah: DimensionalParameter  # Bridge height
    dim_spac: DimensionalParameter  # Bridge length (distance between pole centers)
    
    # Gap/spacing
    dim_spag: DimensionalParameter  # Distance between poles (air gap)
    
    def __repr__(self) -> str:
        return (
            f"SensorGeometry(\n"
            f"  Drive pole:     ∅ {self.dim_dp.nominal*1e3:.2f}mm × H {self.dim_sph_drive.nominal*1e3:.2f}mm\n"
            f"  Sense pole:     ∅ {self.dim_sp.nominal*1e3:.2f}mm × H {self.dim_sph_sense.nominal*1e3:.2f}mm\n"
            f"  Bridge (arm):   W {self.dim_spaw.nominal*1e3:.2f}mm × H {self.dim_spah.nominal*1e3:.2f}mm × L {self.dim_spac.nominal*1e3:.2f}mm\n"
            f"  Pole gap:       {self.dim_spag.nominal*1e3:.2f}mm\n"
            f")"
        )


# Default sensor geometry - nominal values from specification
# Reference dimensions from engineering documentation
DEFAULT_SENSOR_GEOMETRY = SensorGeometry(
    # Drive pole: diameter 9.50mm ± 0.08mm, height 15.0mm ± 0.08mm
    dim_dp=DimensionalParameter(
        nominal=9.50e-3,
        tolerance=0.08e-3
    ),
    dim_sph_drive=DimensionalParameter(
        nominal=15.0e-3,
        tolerance=0.08e-3
    ),
    
    # Sense pole: diameter 4.50mm ± 0.08mm, height 15.0mm ± 0.08mm
    dim_sp=DimensionalParameter(
        nominal=4.50e-3,
        tolerance=0.08e-3
    ),
    dim_sph_sense=DimensionalParameter(
        nominal=15.0e-3,
        tolerance=0.08e-3
    ),
    
    # Bridge/pole arm: width 4.50mm ± 0.08mm, height 4.25mm ± 0.08mm, length 16.0mm ± 0.08mm
    dim_spaw=DimensionalParameter(
        nominal=4.50e-3,
        tolerance=0.08e-3
    ),
    dim_spah=DimensionalParameter(
        nominal=4.25e-3,
        tolerance=0.08e-3
    ),
    dim_spac=DimensionalParameter(
        nominal=16.0e-3,
        tolerance=0.08e-3
    ),
    
    # Pole gap: distance between poles 9.00mm ± 0.10mm
    dim_spag=DimensionalParameter(
        nominal=9.00e-3,
        tolerance=0.10e-3
    ),
)
