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
        murt: float | None = None,
        stress: float | None = None,
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
        murt : float, optional
            Target relative permeability. If None, uses geometry.murt.
        stress : float, optional
            Applied stress [Pa]. Placeholder for inverse magnetostriction effects.
        muo : float, optional
            Vacuum permeability override. If None, uses geometry.muo.
        mur : float, optional
            Core relative permeability override. If None, uses geometry.mur.
        rho : float, optional
            Electrical resistivity override. If None, uses geometry.rho.
        omega : float, optional
            Angular frequency override. If None, uses geometry.omega.

        Returns
        -------
        float
            Core permeance 𝒫_core [H].
        """
        # Extract geometry (nominal values)
        dp = self.geometry.dim_dp.nominal
        sph_drive = self.geometry.dim_sph_drive.nominal
        sp = self.geometry.dim_sp.nominal
        sph_sense = self.geometry.dim_sph_sense.nominal
        spaw = self.geometry.dim_spaw.nominal
        spah = self.geometry.dim_spah.nominal
        spac = self.geometry.dim_spac.nominal
        spag = self.geometry.dim_spag.nominal

        muo = self.geometry.muo.nominal if muo is None else muo
        mur = self.geometry.mur.nominal if mur is None else mur
        murt = self.geometry.murt.nominal if murt is None else murt
        rho = self.geometry.rho.nominal if rho is None else rho
        omega = self.geometry.omega.nominal if omega is None else omega

        # TODO: incorporate stress -> permeability transformation (inverse magnetostriction)
        _ = stress  # placeholder to accept discrete stress input

        # Implement core permeance calculation, starting with branch
        # permeance as a function of geometry and material properties
        Pbr = (spah * spaw * muo * mur) / spac
        Pbreddy = (16 * math.pi * rho) / (spac * omega)

        # Sum the series permeance to estimate the core total permeance
        # (does not include target permeability or stress effects yet)
        permeance = 1.0 / (1 / Pbr + 1 / Pbreddy)

        return permeance


