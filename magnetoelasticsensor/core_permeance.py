"""
Core magnetic permeance calculations for magnetoelastic sensor modeling.

The core permeance represents the reluctance of the main magnetic flux path through
the ferrite core structure and target material. This is distinct from leakage permeance.

Reference: Fleming magnetic circuit analysis
B. Howard
7 Feb 2026.
"""

import math
from magnetoelasticsensor.geometry import SensorGeometry, DEFAULT_SENSOR_GEOMETRY


class CorePermeanceModel:
    """
    Model for calculating core magnetic permeance.
    
    The core permeance depends on:
    - Geometric parameters (pole diameters, heights, gap distance)
    - Material properties (permeability of target and core materials)
    - Stress state (inverse magnetostriction effect on target permeability)
    
    This is a template/placeholder for the hybrid Kleinke-Flemming -based formulation.

    - Kleinke, Darrell K. and  H. Mehmet Uras; Modeling of magnetostrictive sensors. Rev. Sci. Instrum. 1 January 1996; 67 (1): 294–301. https://doi.org/10.1063/1.1146584.
    - Fleming, W., "Magnetostrictive Torque Sensors — Derivation of Model," SAE Technical Paper 890482, 1989. https://doi.org/10.4271/890482.

    """
    
    def __init__(self, geometry: SensorGeometry = None):
        """
        Initialize core permeance model with sensor geometry.
        
        Parameters
        ----------
        geometry : SensorGeometry, optional
            Sensor geometry parameters. If None, uses DEFAULT_SENSOR_GEOMETRY.
        """
        if geometry is None:
            geometry = DEFAULT_SENSOR_GEOMETRY
        self.geometry = geometry
    
    def calculate_core_permeance(
        self,
        *,
        muo: float | None = None,
        mur: float | None = None,
        rho: float | None = None,
        omega: float | None = None,
    ) -> float:
        """
        Calculate equivelent core magnetic permeance using Kleinke equations, 
        (15), (16), and (17) for the eddy-current permeance calculations.

        Parameters
        ----------
        muo : float, optional
            Vacuum permeability override. If None, uses geometry.muo.
        mur : float, optional
            Core relative permeability override. If None, uses geometry.mur.
        rho : float, optional
            Core electrical resistivity override. If None, uses geometry.rho.
        omega : float, optional
            Angular frequency override. If None, uses geometry.omega.

        Returns
        -------
        float
            Core permeance 𝒫_core [H].
        """
        # Extract geometry (nominal values)
        dp = self.geometry.dim_dp.nominal
        dimsphi = self.geometry.dim_sph_drive.nominal
        sp = self.geometry.dim_sp.nominal
        dimsphi = self.geometry.dim_sph_sense.nominal
        dimspawi = self.geometry.dim_spaw.nominal
        dimspahi = self.geometry.dim_spah.nominal
        dimspaci = self.geometry.dim_spac.nominal
        spag = self.geometry.dim_spag.nominal

        muo = self.geometry.muo.nominal if muo is None else muo
        mur = self.geometry.mur.nominal if mur is None else mur
        rho = self.geometry.rho.nominal if rho is None else rho
        omega = self.geometry.omega.nominal if omega is None else omega

        # Implement core permeance calculation, starting with branch
        # permeance as a function of geometry and material properties

        # Branch permeance (magnetic path through core)
        Pbr = (dimspahi * dimspawi * muo * mur) / dimspaci
        assert Pbr > 0, "Branch permeance must be greater than zero."
        Pbreddy = (16 * math.pi * rho) / (dimspaci * omega)
        assert Pbreddy > 0, "Branch eddy current permeance must be greater than zero."

        #sense pole permeance (magnetic path through sense pole)
        Ps = ((sp**2)*muo*mur*math.pi)/(4.*dimsphi)
        assert Ps > 0, "Sense pole permeance must be greater than zero."
        Pseddy = (16*math.pi*rho)/(dimsphi*omega)
        assert Pseddy > 0, "Sense pole eddy current permeance must be greater than zero."

        # Drive pole permeance (magnetic path through drive pole)
        Pd = ((dp**2)*muo*mur*math.pi)/(4.*dimsphi)
        assert Pd > 0, "Drive pole permeance must be greater than zero."
        Pdeddy = (16*math.pi*rho)/(dimsphi*omega)
        assert Pdeddy > 0, "Drive pole eddy current permeance must be greater than zero."

        # Sum the effective permeance to estimate the core total permeance
        # (does not include target permeability or stress effects yet)
        permeance = 1.0 / (1 / Pbr + 1 / Pbreddy + 1 / Ps + 1 / Pseddy
                            + 1 / Pd + 1 / Pdeddy)   

        return permeance


