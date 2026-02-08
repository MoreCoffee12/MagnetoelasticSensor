"""
Magnetic permeance calculations for magnetoelastic sensor modeling.

Reference: Fleming equations for cross-leakage flux permeance.
"""

import math


# Physical constants
MU_0 = 4 * math.pi * 1e-7  # Permeability of free space [H/m]


def calculate_g2_parameter(gap_distance: float, pole_spacing: float) -> float:
    """
    Calculate the g2 geometric parameter for fringing field calculations.
    
    This parameter is used in both air gap permeance (for pole side fringing)
    and cross-leakage permeance calculations. It represents a normalized
    geometric characteristic of the pole spacing and gap configuration.
    
    From Fleming's derivation:
        g2 = -gap_distance + pole_spacing / π
    
    Parameters
    ----------
    gap_distance : float
        Average gap distance between pole face and target surface [m].
    pole_spacing : float
        Distance between poles [m].
    
    Returns
    -------
    float
        The g2 geometric parameter [m].
    
    Notes
    -----
    This parameter appears in:
    - Air gap pole side permeance calculations
    - Cross-leakage permeance height corrections
    
    References
    ----------
    Fleming, W., "Magnetostrictive Torque Sensors — Derivation of Model," 
    SAE Technical Paper 890482, 1989.
    """
    return -gap_distance + pole_spacing / math.pi


def cross_leakage_gu(u: float) -> float:
    """
    Calculate normalized permeance coefficient for cross-leakage flux.
    
    Equation from Fleming, Eq. C.7ff:
        g_u = 2π / ln(u + √(u² - 1))
    
    Parameters
    ----------
    u : float
        Normalized geometric parameter (dimensionless).
        Must satisfy u > 1 for real result.
    
    Returns
    -------
    float
        Normalized permeance coefficient g_u.
    
    Raises
    ------
    ValueError
        If u <= 1, since sqrt(u² - 1) would be imaginary.
    """
    if u <= 1:
        raise ValueError(f"u must be > 1 for real g_u, got u = {u}")
    
    denominator = math.log(u + math.sqrt(u**2 - 1))
    return 2 * math.pi / denominator


def cross_leakage_u_parameter(
    dim_spagi: float,
    dim_dp: float,
    dim_spi: float
) -> float:
    """
    Calculate normalized geometric parameter for cross-leakage flux path.
    
    From Fleming derivation:
        u = (L² - re² - rd²) / (2 * re * rd)
    
    With substitutions:
        L = dim_spagi + (dim_dp / 2) + (dim_spi / 2)
        re = dim_dp / 2
        rd = dim_spi / 2
    
    Simplifies to:
        u = 1 + (2 * dim_spagi * (dim_dp + dim_spi + dim_spagi)) 
            / (dim_dp * dim_spi)
    
    Parameters
    ----------
    dim_spagi : float
        Spagi dimension [m] - related to gap geometry.
    dim_dp : float
        Primary coil dimension [m].
    dim_spi : float
        Secondary coil dimension [m].
    
    Returns
    -------
    float
        Normalized geometric parameter u (dimensionless).
    
    Raises
    ------
    ValueError
        If dim_dp or dim_spi are zero or negative.
    """
    if dim_dp <= 0 or dim_spi <= 0:
        raise ValueError(
            f"Dimensions must be positive: dim_dp={dim_dp}, dim_spi={dim_spi}"
        )
    
    u = 1 + (2 * dim_spagi * (dim_dp + dim_spi + dim_spagi)) / (dim_dp * dim_spi)
    return u




