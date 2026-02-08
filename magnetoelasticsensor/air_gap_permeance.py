"""
Air gap magnetic permeance calculations for magnetoelastic sensor modeling.

The air gap permeance represents the reluctance of the magnetic flux path through
the air gap between the core sense and drive poles and the target material. This is a critical
component in the overall magnetic circuit, as the gap geometry and target proximity
directly affect sensor sensitivity.

The air gap permeance must account for:
- Geometric fringing effects at pole faces
- Target material proximity and alignment
- Pole face area and shape
- Average gap distance between pole and target surface

Reference: Fleming magnetic circuit analysis, Kleinke eddy current formulation
B. Howard
7 Feb 2026.
"""

import math
from magnetoelasticsensor.geometry import SensorGeometry, DEFAULT_SENSOR_GEOMETRY
from magnetoelasticsensor.permeance import calculate_g2_parameter


class AirGapPermeanceModel:
    """
    Model for calculating air gap magnetic permeance.
    
    The air gap permeance depends on:
    - Geometric parameters (pole diameters, average gap distance)
    - Vacuum permeability (μ₀)
    - Average gap distance between pole faces and target surface
    - Fringing field effects at pole boundaries
    
    This model captures the magnetic reluctance of the air path between sensor
    poles and the ferromagnetic target. Changes in target permeability (due to
    stress via inverse magnetostriction) modulate the effective circuit permeance.
    
    References:
    - Kleinke, Darrell K. and H. Mehmet Uras; Modeling of magnetostrictive sensors. 
      Rev. Sci. Instrum. 1 January 1996; 67 (1): 294–301. 
      https://doi.org/10.1063/1.1146584
    - Fleming, W., "Magnetostrictive Torque Sensors — Derivation of Model," 
      SAE Technical Paper 890482, 1989. https://doi.org/10.4271/890482
    """
    
    def __init__(self, geometry: SensorGeometry = None, avg_gap: float | None = None):
        """
        Initialize air gap permeance model with sensor geometry and gap distance.
        
        Parameters
        ----------
        geometry : SensorGeometry, optional
            Sensor geometry parameters. If None, uses DEFAULT_SENSOR_GEOMETRY.
        avg_gap : float, optional
            Average gap distance between pole faces and target surface [m].
            If None, uses geometry.dim_spag.nominal as default gap.
        """
        if geometry is None:
            geometry = DEFAULT_SENSOR_GEOMETRY
        self.geometry = geometry
        
        if avg_gap is None:
            avg_gap = geometry.dim_spag.nominal
        self.avg_gap = avg_gap
    
    def calculate_air_gap_permeance(
        self,
        *,
        avg_gap: float | None = None,
        muo: float | None = None,
        murt: float | None = None,
    ) -> float:
        """
        Calculate air gap magnetic permeance.
        
        The air gap permeance represents the magnetic reluctance of the flux path
        through air between sensor poles and the ferromagnetic target. This calculation
        includes fringing field corrections at pole boundaries.
        
        Physical meaning: Lower gap distance → higher permeance → stronger coupling.
        Stress in target (via inverse magnetostriction) → target permeability change
        → effective gap permeance modulation → measurable voltage signal.
        
        Parameters
        ----------
        avg_gap : float, optional
            Average gap distance override [m]. If None, uses self.avg_gap.
        muo : float, optional
            Vacuum permeability override [H/m]. If None, uses geometry.muo.
        murt : float, optional
            Target relative permeability override (dimensionless).
            If None, uses geometry.murt. This captures stress-induced permeability
            changes in the ferromagnetic target material.
        
        Returns
        -------
        float
            Air gap permeance 𝒫_gap [H].
            
        """
        # Use provided overrides or defaults
        d_gap_avg = self.geometry.avg_gap.nominal if avg_gap is None else avg_gap
        muo = self.geometry.muo.nominal if muo is None else muo
        murt = self.geometry.murt.nominal if murt is None else murt
        
        # Extract pole geometry (nominal values)
        dimsphi = self.geometry.dim_sph_drive.nominal # Drive/sense pole height [m]
        dimdp = self.geometry.dim_dp.nominal # Drive pole diameter [m]
        dimspi = self.geometry.dim_sp.nominal # Sense pole diameter [m]
        dimspagi = self.geometry.dim_spag.nominal # Distance between poles [m]
        
        # Basic sanity checks       
        assert d_gap_avg > 0, "Air gap distance must be greater than zero."
        assert muo > 0, "Vacuum permeability must be greater than zero."
        assert murt > 0, "Target relative permeability must be greater than zero."
        
        # Calculate permeance across the sense pole face, then the drive pole face
        P0s = calculate_pole_face_permeance(
            pole_diameter=dimspi,
            vacuum_permeability=muo,
            gap_distance=d_gap_avg,
        )
        P0d = calculate_pole_face_permeance(
            pole_diameter=dimdp,
            vacuum_permeability=muo,
            gap_distance=d_gap_avg,
        )

        # Calculate fringing field correction for sense pole, using a simplified model
        # suggested by Fleming.
        P1s = calculate_pole_edge_fringing_permeance(
            pole_diameter=dimspi,
            vacuum_permeability=muo,
            gap_distance=d_gap_avg,
        )
        P1d = calculate_pole_edge_fringing_permeance(
            pole_diameter=dimdp,
            vacuum_permeability=muo,
            gap_distance=d_gap_avg,
        )

        # Calculate the permeance at the sides of the pole. First sense, then drive
        P2s = calculate_pole_side_permeance(
            pole_diameter=dimspi,
            vacuum_permeability=muo,
            gap_distance=d_gap_avg,
            pole_spacing=dimspagi,
        )
        P2d = calculate_pole_side_permeance(
            pole_diameter=dimdp,
            vacuum_permeability=muo,
            gap_distance=d_gap_avg,
            pole_spacing=dimspagi,
        )

        # Return the sum
        permeance = [(P0s + P1s + P2s), (P0d + P1d + P2d)]    
        
        return permeance


def calculate_pole_face_permeance(
    pole_diameter: float,
    vacuum_permeability: float,
    gap_distance: float,
) -> float:
    """
    Calculate the permeance across the face of a pole.
    
    Parameters
    ----------
    pole_diameter : float
        Diameter of the pole [mm].
    vacuum_permeability : float
        Vacuum permeability [H/m].
    gap_distance : float
        Distance between pole and target surface [m].
    
    Returns
    -------
    float
        Permeance across the pole face [H].
    """
    return ((pole_diameter**2)*vacuum_permeability*math.pi)/(4.*gap_distance)


def calculate_pole_side_permeance(
    pole_diameter: float,
    vacuum_permeability: float,
    gap_distance: float,
    pole_spacing: float,
) -> float:
    """
    Calculate the permeance at the sides of the pole.

    This term captures a simplified fringing-field contribution along the
    pole sides, based on the pole spacing and average gap distance.

    Parameters
    ----------
    pole_diameter : float
        Pole diameter [m].
    vacuum_permeability : float
        Vacuum permeability μ₀ [H/m].
    gap_distance : float
        Average gap distance between pole face and target surface [m].
    pole_spacing : float
        Distance between poles [m].

    Returns
    -------
    float
        Pole side permeance contribution [H].
    """
    g2 = calculate_g2_parameter(gap_distance, pole_spacing)
    term = pole_diameter / 2.0 + math.sqrt(gap_distance * (gap_distance + g2))
    return 4.0 * term * vacuum_permeability * math.log(1.0 + g2 / gap_distance)


def calculate_pole_edge_fringing_permeance(
    pole_diameter: float,
    vacuum_permeability: float,
    gap_distance: float,
) -> float:
    """
    Calculate the fringing-field permeance correction at the pole face edge.

    This simplified correction follows Fleming's model and accounts for fringe
    flux at the pole edge as a function of pole diameter and average gap distance.

    Parameters
    ----------
    pole_diameter : float
        Pole diameter [m].
    vacuum_permeability : float
        Vacuum permeability μ₀ [H/m].
    gap_distance : float
        Average gap distance between pole face and target surface [m].

    Returns
    -------
    float
        Fringing-field permeance correction [H].
    """
    return 0.528 * vacuum_permeability * 2.0 * math.pi * (
        pole_diameter / 2.0 + gap_distance / 2.0
    )


def calculate_air_gap_permeance(
    geometry: SensorGeometry = None,
    avg_gap: float | None = None,
    **kwargs
) -> float:
    """
    Convenience function to calculate air gap permeance.
    
    Parameters
    ----------
    geometry : SensorGeometry, optional
        Sensor geometry. If None, uses DEFAULT_SENSOR_GEOMETRY.
    avg_gap : float, optional
        Average gap distance [m]. If None, uses geometry.dim_spag.nominal.
    **kwargs
        Additional keyword arguments passed to AirGapPermeanceModel.calculate_air_gap_permeance()
        (e.g., muo, murt overrides).
    
    Returns
    -------
    float
        Air gap permeance [H].
    """
    model = AirGapPermeanceModel(geometry=geometry, avg_gap=avg_gap)
    return model.calculate_air_gap_permeance(**kwargs)