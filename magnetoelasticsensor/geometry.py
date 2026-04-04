"""
Sensor geometry and dimensional parameters for magnetoelastic sensor modeling.

All dimensions stored in SI units (meters) with nominal values and tolerances.
Reference architecture: Single-branch magnetoelastic sensor with ferrite core.

B. Howard
7 Feb 2026.
"""

import math
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
    dim_sph_drive: DimensionalParameter  # Drive pole height [m]
    
    # Sense pole (secondary coil connection)
    dim_sp: DimensionalParameter  # Sense pole diameter [m]
    dim_sph_sense: DimensionalParameter  # Sense pole height [m]

    # Coil turns
    ndrive: DimensionalParameter  # Number of turns on drive coil [dimensionless]
    nsense: DimensionalParameter  # Number of turns on sense coil [dimensionless]
    
    # Bridge / Pole arm (ferrite structure connecting poles)
    awi: DimensionalParameter  # Rectangular Bridge width [m]
    dim_spah: DimensionalParameter  # Rectangular Bridge height [m]
    drspi: DimensionalParameter  # Bridge length (distance between pole centers)

    # Core magnetic properties (not geometric but included for completeness)
    muo: DimensionalParameter  # Permeability of free space [H/m]
    mur: DimensionalParameter  # Relative permeability of core material (dimensionless)
    rho: DimensionalParameter  # Electrical resistivity of core material [Ω·m]
    
    # Target magnetic and electrical properties
    murt: DimensionalParameter  # Relative permeability of target material (dimensionless)
    
    # Gap/spacing
    dim_spag: DimensionalParameter  # Distance between poles 
    avg_gap: DimensionalParameter  # Average gap distance between poles and target surface [mm]  

    # Operating frequency (for eddy current calculations)
    omega: DimensionalParameter  # Angular frequency [rad/s]

    # Target geometric parameter
    theta3_deg: DimensionalParameter  # Angle parameter for target geometry [degrees]

    # Target conductivity
    sigmac: DimensionalParameter  # Electrical conductivity of target material [S/m]
    
    def __repr__(self) -> str:
        return (
            f"SensorGeometry(\n"
            f"  Drive pole:     ∅ {self.dim_dp.nominal*1e3:.2f}mm × H {self.dim_sph_drive.nominal*1e3:.2f}mm\n"
            f"  Sense pole:     ∅ {self.dim_sp.nominal*1e3:.2f}mm × H {self.dim_sph_sense.nominal*1e3:.2f}mm\n"
            f"  Bridge (arm):   W {self.awi.nominal*1e3:.2f}mm × H {self.dim_spah.nominal*1e3:.2f}mm × L {self.drspi.nominal*1e3:.2f}mm\n"
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

    # Coil turns
    ndrive=DimensionalParameter(
        nominal=60.0,  # Number of turns on drive coil [dimensionless]
        tolerance=1.0  # We sometimes take a turn or two off to impedance match
    ),
    nsense=DimensionalParameter(
        nominal=100.0,  # Number of turns on sense coil [dimensionless]
        tolerance=1.0  # We sometimes take a turn or two off to impedance match
    ),
    
    # Bridge/pole arm: width 4.50mm ± 0.08mm, height 4.25mm ± 0.08mm, length 16.0mm ± 0.08mm
    awi=DimensionalParameter(
        nominal=4.50e-3,
        tolerance=0.08e-3
    ),
    dim_spah=DimensionalParameter(
        nominal=4.25e-3,
        tolerance=0.08e-3
    ),
    drspi=DimensionalParameter(
        nominal=16.0e-3,
        tolerance=0.08e-3
    ),
    
    # Pole gap: distance between poles 9.00mm ± 0.10mm
    dim_spag=DimensionalParameter(
        nominal=9.00e-3,
        tolerance=0.10e-3
    ),

    # Permeability of free space
    muo=DimensionalParameter(
        nominal=4 * math.pi * 1e-7,
        tolerance=0.0  # Physical constant, no tolerance
    ),

    # Permeability of core material (ferrite) - nominal value from datasheet, tolerance estimated
    # “97 Material Data Sheet - Fair-Rite.” Fair-Rite 97 
    # Material Data Sheet, Fair-rite, 26 Apr. 2023, 
    # fair-rite.com/97-material-data-sheet/.
    mur=DimensionalParameter(
        nominal=2000.0,  # Room temp, @ B < 10 gauss
        tolerance=20.0  # Estimated
    ),

    # Electrical resistivity of core material (ferrite) - nominal value from datasheet, tolerance estimated
        # “97 Material Data Sheet - Fair-Rite.” Fair-Rite 97 
    # Material Data Sheet, Fair-rite, 26 Apr. 2023, 
    # fair-rite.com/97-material-data-sheet/.
    rho=DimensionalParameter(
        nominal=2.0,  # Electrical resistivity of ferrite [Ω·m], estimated
        tolerance=0.02  # Estimated, used in dissertation
    ),

    # Permeability of target material (ferromagnetic)  
    # - Jiles, David. Introduction to Magnetism and Magnetic 
    #   Materials. 3rd ed., Springer Boston, MA, 2016.
    # - Rose, J.H., Uzal, E., Moulder, J.C. (1995). Magnetic Permeability 
    #   and Eddy-Current Measurements. In: Thompson, D.O., Chimenti, D.E. 
    #   (eds) Review of Progress in Quantitative Nondestructive Evaluation. 
    #   Springer, Boston, MA. https://doi.org/10.1007/978-1-4615-1987-4_36.
    # - Jiles, D.C. (1988), Variation of the magnetic properties of AISI 
    #   4140 steels with plastic strain. phys. stat. sol. (a), 108: 
    #   417-429. https://doi.org/10.1002/pssa.2211080144.
    # - Hristoforou, E., A. Ktena, P. Vourna, and K. Argiris. “Dependence 
    #   of Magnetic Permeability on Residual Stresses in Alloyed Steels.” 
    #   *AIP Advances*, vol. 8, no. 4, 2018, article 047201,
    #    https://doi.org/10.1063/1.4994202.
    # Findings:
    #  Most probably 4140 and 4340 steel have a relative permeability in
    #  the range of 55 to 65 at zero stress and room temperatures.
    #  Using Figure 4 in Hristoforou et. al., likely a 10% change
    #  in permeability with 100 MPa of applied stress. 
    murt=DimensionalParameter(
        nominal=60.0,  # Room temp, zero stress
        tolerance= 1.0 # Estimated, actual value will depend on target material and stress state  
    ),

    # Operating frequency (for eddy current calculations)
    # Matches assumptions in dissertation. 
    omega=DimensionalParameter(
        nominal=2 * math.pi * 50000.0,  # 50 kHz operating frequency
        tolerance=0.0  # No tolerance, user-defined parameter
    ),

    # Target geometric parameter - angle for target geometry. Fleming says this ranges from
    # 45 degrees at low saturation to 26.6 degrees at high saturation.
    theta3_deg=DimensionalParameter(
        nominal=45.0,  # 45 degrees [degrees]
        tolerance=0.0  # Fixed design parameter, no tolerance
    ),

    # Average gap distance between poles and target surface - research definition
    avg_gap=DimensionalParameter(
        nominal=1.143/1000,  # Average gap distance [m]
        tolerance=1.0/100000  # What you get with plastic feeler gauges
    ),  

    # Target conductivity
    # Reference:
    # - Material Data Sheet for AISI 4140 Steel." Knovel, 
    #   www.knovel.com/web/portal/knovel_content?p_p_id=EXT_KNOVEL_CONTENT. 
    #   Accessed 12 Oct. 2011.
    sigmac=DimensionalParameter(
        nominal=100000000/22,  # Electrical conductivity of target material [S/m]
        tolerance=5000000/22  # Estimated 
    )

)
