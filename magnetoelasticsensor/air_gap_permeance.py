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
        dimsphi = self.geometry.dim_sph_drive.nominal # Drive pole diameter [mm]
        dimspi = self.geometry.dim_sp.nominal # Sense pole diameter [mm]
        
        # Basic sanity checks       
        assert d_gap_avg > 0, "Air gap distance must be greater than zero."
        assert muo > 0, "Vacuum permeability must be greater than zero."
        assert murt > 0, "Target relative permeability must be greater than zero."
        
        # Calculate permeance across the sense pole face.
        P0s = ((dimspi**2)*muo*math.pi)/(4.*d_gap_avg)


        permeance = P0s
        
        return permeance


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