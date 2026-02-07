"""
Magnetic permeance calculations for magnetoelastic sensor modeling.

Reference: Fleming equations for cross-leakage flux permeance.
"""

import math


# Physical constants
MU_0 = 4 * math.pi * 1e-7  # Permeability of free space [H/m]


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


def cross_leakage_permeance(
    dim_spagi: float,
    dim_dp: float,
    dim_spi: float,
    dim_sphi: float,
    dim_spahi: float,
    g2: float
) -> float:
    """
    Calculate cross-leakage flux permeance.
    
    From Fleming:
        𝒫₁₂ = μ₀ * (h - g2) * g_u
    
    Where:
        h = dim_sphi - dim_spahi
        u = geometric parameter from cross_leakage_u_parameter()
        g_u = normalized coefficient from cross_leakage_gu()
    
    Parameters
    ----------
    dim_spagi : float
        Spagi dimension [m] - gap-related geometry.
    dim_dp : float
        Primary coil dimension [m].
    dim_spi : float
        Secondary coil dimension [m].
    dim_sphi : float
        Sphi dimension [m] - height-related geometry.
    dim_spahi : float
        Spahi dimension [m] - additional height offset.
    g2 : float
        Secondary gap parameter [m].
    
    Returns
    -------
    float
        Cross-leakage permeance 𝒫₁₂ [H].
    
    Raises
    ------
    ValueError
        If geometric constraints are violated (see cross_leakage_u_parameter).
    """
    # Calculate normalized geometric parameter
    u = cross_leakage_u_parameter(dim_spagi, dim_dp, dim_spi)
    
    # Calculate normalized permeance coefficient
    gu = cross_leakage_gu(u)
    
    # Calculate height difference
    h = dim_sphi - dim_spahi
    
    # Calculate permeance: 𝒫₁₂ = μ₀ * (h - g2) * g_u
    permeance = MU_0 * (h - g2) * gu
    
    return permeance

