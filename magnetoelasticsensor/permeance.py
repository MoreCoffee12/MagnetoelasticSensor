"""
Magnetic permeance calculations for magnetoelastic sensor modeling.

Reference: Fleming equations for cross-leakage flux permeance.
"""

import math


# Physical constants
MU_0 = 4 * math.pi * 1e-7  # Permeability of free space [H/m]


def calculate_skin_depth(
    muo: float,
    mur: float,
    omega: float,
    sigma_c: float,
) -> float:
    """
    Calculate the average eddy current skin depth for the target material.

    From Jiles:
        delta = sqrt(2) * sqrt(1 / (muo * mur * omega * sigma_c))

    References:
    - Jiles, David. Introduction to Magnetism and Magnetic Materials. 
      3rd ed., Springer Boston, MA, 2016.

    Parameters
    ----------
    muo : float
        Vacuum permeability [H/m].
    mur : float
        Relative permeability of the material (dimensionless).
    omega : float
        Angular frequency [rad/s].
    sigma_c : float
        Electrical conductivity [S/m].

    Returns
    -------
    float
        Skin depth delta [m].
    """
    if muo <= 0 or mur <= 0 or omega <= 0 or sigma_c <= 0:
        raise ValueError(
            "muo, mur, omega, and sigma_c must all be positive to compute skin depth"
        )

    return math.sqrt(2.0) * math.sqrt(1.0 / (muo * mur * omega * sigma_c))


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


def calculate_series_permeance(
    pt: float,
    p_gapd: float,
    p_gaps: float
) -> float:
    """
    Calculate the combined permeance of three magnetic circuit elements in series.
    
    For permeances (or reluctances) in series, the reciprocals add:
        1/P_total = 1/Pt + 1/P_gapd + 1/P_gaps
    
    Therefore:
        P_total = 1 / (1/Pt + 1/P_gapd + 1/P_gaps)
    
    This represents the effective permeance of a magnetic circuit where flux
    must pass sequentially through the target (Pt), drive gap (P_gapd), and
    sense gap (P_gaps) elements.
    
    Parameters
    ----------
    pt : float
        Target permeance [H].
    p_gapd : float
        Drive gap permeance [H].
    p_gaps : float
        Sense gap permeance [H].
    
    Returns
    -------
    float
        Combined series permeance [H].
    
    Raises
    ------
    ValueError
        If any permeance is zero or negative.
    
    Notes
    -----
    This equation is analogous to resistors in series (R_total = R1 + R2 + R3)
    but applied to magnetic reluctance. Since permeance P = 1/R (reluctance),
    the reciprocals add in the same way.
    """
    if pt <= 0 or p_gapd <= 0 or p_gaps <= 0:
        raise ValueError(
            f"All permeances must be positive: pt={pt}, p_gapd={p_gapd}, p_gaps={p_gaps}"
        )
    
    reciprocal_sum = (1.0 / pt) + (1.0 / p_gapd) + (1.0 / p_gaps)
    return 1.0 / reciprocal_sum




