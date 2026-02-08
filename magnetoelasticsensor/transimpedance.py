"""
Transimpedance calculations for magnetoelastic sensor impedance analysis.

Implements the complex impedance model relating drive current (Id) to sense voltage (Vs)
in a four-branch magnetoelastic sensor with target eddy current coupling effects.
"""


def calculate_normalized_impedance(
    p3: float,
    p_sd: float,
    p: float,
    epsilon: float,
) -> complex:
    """
    Calculate the complex normalized impedance factor accounting for eddy current effects.
    
    The normalized impedance represents the frequency-dependent coupling between the drive
    and sense circuits through the ferromagnetic target material. Eddy currents in the
    target dissipate energy and modify the magnetic coupling.
    
    Formula:
        z = (-j*P3*(Psd + 3*P) + 3*P3*P*ε + Psd*(P3 + P)*ε) 
            / (-j*3*P3*P + 3*P*(P3 + P)*ε)
    
    Where:
        j = complex unit (0 + 1j in Python)
        P3 = target eddy-current permeance [H]
        Psd = cross-leakage permeance [H]
        P = effective permeance (series target + air gaps) [H]
        ε = frequency-dependent damping/loss factor [dimensionless]
    
    Parameters
    ----------
    p3 : float
        Target eddy-current permeance [H].
    p_sd : float
        Cross-leakage permeance [H].
    p : float
        Effective permeance [H].
    epsilon : float
        Frequency-dependent damping factor [dimensionless].
        Typically small positive value accounting for target losses.
    
    Returns
    -------
    complex
        Complex normalized impedance factor z (dimensionless).
    
    Raises
    ------
    ValueError
        If any permeance is zero or epsilon is negative.
    """
    if p3 <= 0 or p_sd <= 0 or p <= 0:
        raise ValueError(
            f"All permeances must be positive: p3={p3}, p_sd={p_sd}, p={p}"
        )
    
    if epsilon < 0:
        raise ValueError(f"epsilon must be non-negative: epsilon={epsilon}")
    
    j = complex(0, 1)  # Complex unit
    
    # Numerator: -j*P3*(Psd + 3*P) + 3*P3*P*ε + Psd*(P3 + P)*ε
    numerator = (
        -j * p3 * (p_sd + 3.0 * p)
        + 3.0 * p3 * p * epsilon
        + p_sd * (p3 + p) * epsilon
    )
    
    # Denominator: -j*3*P3*P + 3*P*(P3 + P)*ε
    denominator = (
        -j * 3.0 * p3 * p
        + 3.0 * p * (p3 + p) * epsilon
    )
    
    if denominator == 0:
        raise ValueError("Denominator is zero - invalid parameter combination")
    
    return numerator / denominator


def calculate_transimpedance(
    nd: int,
    ns: int,
    p_eq: float,
    omega: float,
    p3: float,
    p_sd: float,
    p: float,
    epsilon: float,
) -> complex:
    """
    Calculate the complex transimpedance (Vs/Id) of the magnetoelastic sensor.
    
    The transimpedance relates the sense voltage (Vs) to the drive current (Id),
    accounting for:
    - Magnetic coupling through the core (Nd * Ns * P_eq * ω)
    - Frequency-dependent effects (ω = 2πf)
    - Target eddy current losses and coupling modification (z factor)
    
    Formula:
        Vs/Id = j * Nd * Ns * P_eq * ω * z
    
    Where:
        j = complex unit
        Nd = number of drive coil turns
        Ns = number of sense coil turns
        P_eq = equivalent permeance [H]
        ω = angular frequency [rad/s]
        z = complex normalized impedance factor (calculated separately)
    
    Parameters
    ----------
    nd : int
        Number of drive coil turns (dimensionless).
        Must be a positive integer.
    ns : int
        Number of sense coil turns (dimensionless).
        Must be a positive integer.
    p_eq : float
        Equivalent permeance of the four-branch circuit [H].
    omega : float
        Angular frequency [rad/s].
        Must be positive.
    p3 : float
        Target eddy-current permeance [H].
    p_sd : float
        Cross-leakage permeance [H].
    p : float
        Effective permeance [H].
    epsilon : float
        Frequency-dependent damping factor [dimensionless].
    
    Returns
    -------
    complex
        Complex transimpedance Vs/Id [Ω].
    
    Raises
    ------
    ValueError
        If any input parameters are invalid.
    
    Notes
    -----
    The transimpedance has units of impedance (Ohms) and represents the sensitivity
    of the sense voltage to the drive current. The magnitude indicates coupling strength,
    while the phase indicates frequency-dependent behavior.
    
    At low frequencies (ω→0): Z approaches 0 (capacitive behavior)
    At high frequencies: Z approaches frequency-dependent value (resistive behavior)
    """
    if nd <= 0 or not isinstance(nd, int):
        raise ValueError(f"nd must be a positive integer: nd={nd}")
    
    if ns <= 0 or not isinstance(ns, int):
        raise ValueError(f"ns must be a positive integer: ns={ns}")
    
    if p_eq <= 0:
        raise ValueError(f"p_eq must be positive: p_eq={p_eq}")
    
    if omega <= 0:
        raise ValueError(f"omega must be positive: omega={omega}")
    
    j = complex(0, 1)  # Complex unit
    
    # Calculate normalized impedance factor
    z = calculate_normalized_impedance(
        p3=p3,
        p_sd=p_sd,
        p=p,
        epsilon=epsilon,
    )
    
    # Calculate transimpedance: Vs/Id = j * Nd * Ns * P_eq * ω * z
    transimpedance = j * nd * ns * p_eq * omega * z
    
    return transimpedance


def calculate_transimpedance_magnitude(
    nd: int,
    ns: int,
    p_eq: float,
    omega: float,
    p3: float,
    p_sd: float,
    p: float,
    epsilon: float,
) -> float:
    """
    Calculate the magnitude of the complex transimpedance.
    
    The magnitude represents the coupling strength between drive and sense circuits,
    independent of phase information.
    
    Parameters
    ----------
    nd : int
        Number of drive coil turns.
    ns : int
        Number of sense coil turns.
    p_eq : float
        Equivalent permeance [H].
    omega : float
        Angular frequency [rad/s].
    p3 : float
        Target eddy-current permeance [H].
    p_sd : float
        Cross-leakage permeance [H].
    p : float
        Effective permeance [H].
    epsilon : float
        Frequency-dependent damping factor [dimensionless].
    
    Returns
    -------
    float
        Magnitude of transimpedance |Vs/Id| [Ω].
    """
    impedance = calculate_transimpedance(
        nd=nd,
        ns=ns,
        p_eq=p_eq,
        omega=omega,
        p3=p3,
        p_sd=p_sd,
        p=p,
        epsilon=epsilon,
    )
    
    return abs(impedance)


def calculate_transimpedance_phase(
    nd: int,
    ns: int,
    p_eq: float,
    omega: float,
    p3: float,
    p_sd: float,
    p: float,
    epsilon: float,
) -> float:
    """
    Calculate the phase angle of the complex transimpedance.
    
    The phase angle indicates the phase relationship between sense voltage
    and drive current, reflecting frequency-dependent capacity and resistance.
    
    Parameters
    ----------
    nd : int
        Number of drive coil turns.
    ns : int
        Number of sense coil turns.
    p_eq : float
        Equivalent permeance [H].
    omega : float
        Angular frequency [rad/s].
    p3 : float
        Target eddy-current permeance [H].
    p_sd : float
        Cross-leakage permeance [H].
    p : float
        Effective permeance [H].
    epsilon : float
        Frequency-dependent damping factor [dimensionless].
    
    Returns
    -------
    float
        Phase angle in radians [-π, π].
    """
    import cmath
    
    impedance = calculate_transimpedance(
        nd=nd,
        ns=ns,
        p_eq=p_eq,
        omega=omega,
        p3=p3,
        p_sd=p_sd,
        p=p,
        epsilon=epsilon,
    )
    
    return cmath.phase(impedance)
