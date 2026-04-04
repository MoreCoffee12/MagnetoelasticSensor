"""
Cross-leakage magnetic permeance calculations for magnetoelastic sensor modeling.

The cross-leakage permeance represents the reluctance of magnetic flux paths that
leak between the drive and sense poles through non-ideal coupling routes. This leakage
flux does not contribute to useful signal transduction and represents loss in the
magnetic circuit efficiency.

The cross-leakage permeance accounts for:
- Flux paths between poles that bypass the target material
- Ferrite core geometry and magnetic properties
- Pole-to-pole spacing and orientation

References: 

19.	Fleming, W., "Magnetostrictive Torque Sensors — Derivation of Model," SAE 
Technical Paper 890482, 1989.

30.	Kleinke, Darrell K. and H. Mehmet Uras; Modeling of magnetostrictive 
sensors. Rev. Sci. Instrum. 1 January 1996; 67 (1): 294–301.
https://doi.org/10.1063/1.1146584.

B. Howard
8 Feb 2026.
"""

import math
from magnetoelasticsensor.geometry import SensorGeometry, DEFAULT_SENSOR_GEOMETRY
from magnetoelasticsensor.permeance import (
    calculate_g2_parameter,
    cross_leakage_u_parameter,
)


class CrossLeakagePermeanceModel:
    """
    Model for calculating cross-leakage magnetic permeance.
    
    The cross-leakage permeance represents parasitic flux coupling between drive
    and sense poles that does not pass through the target material. This leakage
    reduces sensor efficiency and signal-to-noise ratio.
    
    The cross-leakage permeance depends on:
    - Ferrite core geometry (pole spacing, bridge dimensions)
    - Core cross-sectional area available for leakage
    
    Physical interpretation:
    - Larger pole spacing → lower leakage (longer flux path)
    - Larger core cross-section → higher leakage (more flux capacity)
    
    References:
    - Kleinke, Darrell K. and H. Mehmet Uras; Modeling of magnetostrictive sensors. 
      Rev. Sci. Instrum. 1 January 1996; 67 (1): 294–301. 
      https://doi.org/10.1063/1.1146584
    - Fleming, W., "Magnetostrictive Torque Sensors — Derivation of Model," 
      SAE Technical Paper 890482, 1989. https://doi.org/10.4271/890482
    """
    
    def __init__(self, geometry: SensorGeometry = None):
        """
        Initialize cross-leakage permeance model with sensor geometry.
        
        Parameters
        ----------
        geometry : SensorGeometry, optional
            Sensor geometry parameters. If None, uses DEFAULT_SENSOR_GEOMETRY.
        """
        if geometry is None:
            geometry = DEFAULT_SENSOR_GEOMETRY
        self.geometry = geometry
    
    def calculate_cross_leakage_permeance(
        self,
        *,
        muo: float | None = None,
    ) -> float:
        """
        Calculate cross-leakage magnetic permeance.
        
        The cross-leakage permeance represents parasitic flux coupling between drive
        and sense poles through the ferrite core material. This flux path does not
        interact with the target and represents loss in the magnetic circuit.
        
        Physical meaning: 
        - Higher cross-leakage → reduced effective coupling to target
        - Lower cross-leakage → higher sensor efficiency and sensitivity
        
        Parameters
        ----------
        muo : float, optional
            Vacuum permeability override [H/m]. If None, uses geometry.muo.
        Returns
        -------
        float
            Cross-leakage permeance 𝒫_leakage [H].
        """
        # Use provided overrides or defaults
        muo = self.geometry.muo.nominal if muo is None else muo
        
        # Extract core geometry (nominal values)
        awi = self.geometry.awi.nominal  # Sense pole are width [m]
        sphi = self.geometry.dim_spah.nominal  # Pole overall height [m]
        dim_spac = self.geometry.dim_spac.nominal  # Pole-to-pole spacing [m]
        dimdp = self.geometry.dim_dp.nominal  # Drive pole diameter [m]
        dimspagi = self.geometry.dim_spag.nominal  # Pole gap [m] 
        dimspi = self.geometry.dim_sp.nominal  # Sense pole diameter [m]
        dimsphi = self.geometry.dim_sph_sense.nominal  # Sense/drive pole height [m]
        avg_gap = self.geometry.avg_gap.nominal  # Average gap distance [m]
        
        # Basic sanity checks
        assert muo > 0, "Vacuum permeability must be greater than zero."
        assert awi > 0, "Bridge width must be greater than zero."
        assert sphi > 0, "Bridge height must be greater than zero."
        assert dim_spac > 0, "Pole spacing must be greater than zero."
        
        # Calculate g2 parameter for fringing field calculations
        # Note: For cross-leakage, we use the pole spacing (dim_spag) and 
        # we need a gap distance. Using dimspagi as the effective gap.
        u = cross_leakage_u_parameter(dim_spagi=dimspagi, dim_dp=dimdp,
                                       dim_spi=dimspi)
        g2 = calculate_g2_parameter(gap_distance=avg_gap, pole_spacing=dimspagi)
        
        # Calculate cross-leaking permeance following Fleming's method
        # using the utility function from permeance module
        permeance = (2*(-sphi + dimsphi - g2)*muo*math.pi)/math.log(u + math.sqrt(-1 + math.pow(u,2)))
        
        return permeance







