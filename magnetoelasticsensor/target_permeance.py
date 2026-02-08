"""
Target magnetic permeance calculations for magnetoelastic sensor modeling.

Implements Fleming-style equations for target permeance and eddy current
skin-depth effects.

References:
- Fleming, W., "Magnetostrictive Torque Sensors — Derivation 
  of Model," SAE Technical Paper 890482, 1989.  

"""

import math
from magnetoelasticsensor.geometry import SensorGeometry, DEFAULT_SENSOR_GEOMETRY
from magnetoelasticsensor.permeance import calculate_skin_depth, cross_leakage_gu, cross_leakage_u_parameter


class TargetPermeanceModel:
    """
    Model for calculating target magnetic permeance.

    The target permeance captures flux coupling into the target material with
    eddy current effects approximated by an average skin depth.
    """

    def __init__(self, geometry: SensorGeometry = None):
        """
        Initialize target permeance model with sensor geometry.

        Parameters
        ----------
        geometry : SensorGeometry, optional
            Sensor geometry parameters. If None, uses DEFAULT_SENSOR_GEOMETRY.
        """
        if geometry is None:
            geometry = DEFAULT_SENSOR_GEOMETRY
        self.geometry = geometry

    def calculate_target_permeance(
        self,
        *,
        ha: float | None = None,
        u: float | None = None,
        sigma_c: float | None = None,
        muo: float | None = None,
        murt: float | None = None,
        omega: float | None = None,
    ) -> float:
        """
        Calculate target magnetic permeance.

        Implements:
            Pt = (2 * pi * delta * muo * mur) / ln(u + sqrt(u^2 - 1))
            P3 = 1 / (1 / Pt + 1 / (ha * muo * u))

        Parameters
        ----------
        ha : float, optional
            Eddy current flux height above the target [m]. Defaults to skin depth if not provided.
        u : float, optional
            Normalized geometric parameter (dimensionless). Default to Fleming's cross-leakage geometric factor.
        sigma_c : float, optional  
            Target electrical conductivity [S/m].
        muo : float, optional
            Vacuum permeability override [H/m]. If None, uses geometry.muo.
        murt : float, optional
            Target relative permeability override (dimensionless).
            If None, uses geometry.murt.
        omega : float, optional
            Angular frequency override [rad/s]. If None, uses geometry.omega.

        Returns
        -------
        float
            Target permeance P3 [H].
        """
        sigma_c = self.geometry.sigmac.nominal if sigma_c is None else sigma_c
        muo = self.geometry.muo.nominal if muo is None else muo
        murt = self.geometry.murt.nominal if murt is None else murt
        omega = self.geometry.omega.nominal if omega is None else omega

        # Default to the skin depth calcuation as default for the eddy current flux height
        # (See Fleming, Fig. C.4)
        ha = calculate_skin_depth(muo=muo, mur=murt, omega=omega, sigma_c=sigma_c) if ha is None else ha

        # Default to Fleming's cross-leakage geometric factor (Equation C.8)
        u = cross_leakage_u_parameter(dim_spagi=self.geometry.dim_spag.nominal, dim_dp=self.geometry.dim_dp.nominal,
                                       dim_spi=self.geometry.dim_sp.nominal) if u is None else u

        if ha <= 0:
            raise ValueError("ha must be positive")
        if u <= 1:
            raise ValueError("u must be > 1 for real-valued target permeance")
        if sigma_c <= 0:
            raise ValueError("sigma_c must be positive")
        if muo <= 0 or murt <= 0 or omega <= 0:
            raise ValueError("muo, murt, and omega must be positive")

        # Permeance associated with main mutual flux passing through the target.
        delta = calculate_skin_depth(muo=muo, mur=murt, omega=omega, sigma_c=sigma_c)

        pt = (2*math.pi*delta*muo*murt)/math.log(u + math.sqrt(-1 + u**2))
        if pt <= 0 :
            raise ValueError("Computed permeance terms must be positive")

        return pt


def calculate_target_permeance(
    *,
    geometry: SensorGeometry = None,
    ha: float,
    u: float,
    sigma_c: float,
    muo: float | None = None,
    murt: float | None = None,
    omega: float | None = None,
) -> float:
    """
    Convenience function to calculate target permeance.

    Parameters
    ----------
    geometry : SensorGeometry, optional
        Sensor geometry. If None, uses DEFAULT_SENSOR_GEOMETRY.
    ha : float
        Effective target height [m].
    u : float
        Normalized geometric parameter (dimensionless).
    sigma_c : float
        Target electrical conductivity [S/m].
    muo : float, optional
        Vacuum permeability override [H/m]. If None, uses geometry.muo.
    murt : float, optional
        Target relative permeability override (dimensionless).
        If None, uses geometry.murt.
    omega : float, optional
        Angular frequency override [rad/s]. If None, uses geometry.omega.

    Returns
    -------
    float
        Target permeance P3 [H].
    """
    model = TargetPermeanceModel(geometry=geometry)
    return model.calculate_target_permeance(
        ha=ha,
        u=u,
        sigma_c=sigma_c,
        muo=muo,
        murt=murt,
        omega=omega,
    )
