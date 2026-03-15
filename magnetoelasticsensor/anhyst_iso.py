"""
anhyst_iso.py

Compute the anhysteretic magnetization term used in the Jiles-Atherton
magnetic hysteresis model.

Equation
--------
Man = Ms * (coth(H_eff/a) - a/H_eff)

with:

H_eff = H + alpha*M + H_sigma

Equivalent form
---------------
Let:
    x = H_eff / a

Then:
    Man = Ms * (coth(x) - 1/x)

Notes
-----
The expression coth(x) - 1/x is the Langevin function. Near x = 0, the
direct formula is numerically unstable, so a series expansion is used.

References
----------
[1] 	D. Jiles and D. Atherton, "Ferromagnetic hysteresis," in IEEE Transactions 
        on Magnetics, vol. 19, no. 5, pp. 2183-2185, September 1983, 
        doi: 10.1109/TMAG.1983.1062594.
[2]  	Jiles, D. C., and D. L. Atherton. "Theory of Ferromagnetic Hysteresis." 
        Journal of Magnetism and Magnetic Materials, vol. 61, nos. 1\[Dash]2, 
        1986, pp. 48\[Dash]60.
"""

from __future__ import annotations

import numpy as np

from magnetoelasticsensor.ja_props import JAProps


MU0 = 4.0e-7 * np.pi


def anhysteretic_magnetization(
    h: float | np.ndarray,
    m: float | np.ndarray,
    props: JAProps,
) -> float | np.ndarray:
    """
    Compute anhysteretic magnetization for the Jiles-Atherton model.

    Parameters
    ----------
    h : float or numpy.ndarray
        Applied magnetic field strength.
    m : float or numpy.ndarray
        Magnetization.
    props : JAProps
        Jiles-Atherton model parameters.  Only ``ms``, ``a``, and
        ``alpha`` are used by this function.

    Returns
    -------
    float or numpy.ndarray
        Anhysteretic magnetization, with the same broadcasted shape as
        the inputs.

    Raises
    ------
    ValueError
        If ``props.a`` is zero.
    """
    if props.a == 0:
        raise ValueError("Parameter 'a' must be nonzero.")

    h_arr = np.asarray(h, dtype=float)
    m_arr = np.asarray(m, dtype=float)

    h_sigma = _stress_field(m_arr, props)
    x = (h_arr + props.alpha * m_arr + h_sigma) / props.a
    man = props.ms * _langevin(x)

    if np.isscalar(h) and np.isscalar(m):
        return float(man)

    return man


def anhysteretic_magnetization_differential(
    h: float | np.ndarray,
    m: float | np.ndarray,
    props: JAProps,
) -> float | np.ndarray:
    """
    Compute the analytical differential of the anhysteretic curve with
    respect to the applied field H, holding M fixed.

    Formula::

        dMan/dH = Ms * (a / H_eff^2 - csch(H_eff/a)^2 / a)

    The direct closed form is numerically unstable near H_eff = 0,
    so the small-field limit is evaluated with the Langevin-series
    expansion, which yields dMan/dH -> Ms / (3a).

    Parameters
    ----------
    h : float or numpy.ndarray
        Applied magnetic field strength, A/m.
    m : float or numpy.ndarray
        Magnetization, A/m.
    props : JAProps
        Jiles-Atherton model parameters.  Only ``ms``, ``a``, and
        ``alpha`` are used by this function.

    Returns
    -------
    float or numpy.ndarray
        Analytical differential dMan/dH with the same broadcasted shape as
        the inputs.

    Raises
    ------
    ValueError
        If ``props.a`` is zero.
    """
    if props.a == 0:
        raise ValueError("Parameter 'a' must be nonzero.")

    h_arr = np.asarray(h, dtype=float)
    m_arr = np.asarray(m, dtype=float)

    h_sigma = _stress_field(m_arr, props)
    x = (h_arr + props.alpha * m_arr + h_sigma) / props.a
    dman_dh = (props.ms / props.a) * _langevin_deriv(x)

    if np.isscalar(h) and np.isscalar(m):
        return float(dman_dh)

    return dman_dh


def _langevin(x: np.ndarray | float) -> np.ndarray | float:
    """
    Compute the Langevin function L(x) = coth(x) - 1/x.

    Uses a series expansion near x = 0 for numerical stability:
        L(x) = x/3 - x^3/45 + 2*x^5/945 + O(x^7)
    """
    x_arr = np.asarray(x, dtype=float)
    out = np.empty_like(x_arr)

    small = np.abs(x_arr) < 1.0e-6
    large = ~small

    # Series expansion for small x
    xs = x_arr[small]
    out[small] = xs / 3.0 - xs**3 / 45.0 + 2.0 * xs**5 / 945.0

    # Direct evaluation for larger x
    xl = x_arr[large]
    out[large] = 1.0 / np.tanh(xl) - 1.0 / xl

    if np.isscalar(x):
        return float(out)

    return out


def anhysteretic_magnetization_deriv(
    h: float | np.ndarray,
    m: float | np.ndarray,
    props: JAProps,
) -> float | np.ndarray:
    """
    Backward-compatible wrapper for the analytical differential of the
    anhysteretic curve.

    For the isotropic Jiles-Atherton formulation used here, dMan/dH and
    dMan/dH_eff are numerically identical when M is treated as fixed inside
    the anhysteretic relation. This wrapper preserves the existing public API
    while delegating to the explicit analytical helper.

    Parameters
    ----------
    h : float or numpy.ndarray
        Applied magnetic field strength, A/m.
    m : float or numpy.ndarray
        Magnetization, A/m.
    props : JAProps
        Jiles-Atherton model parameters.  Only ``ms``, ``a``, and
        ``alpha`` are used by this function.

    Returns
    -------
    float or numpy.ndarray
        dMan/dH_eff with the same broadcasted shape as the inputs.

    Raises
    ------
    ValueError
        If ``props.a`` is zero.
    """
    return anhysteretic_magnetization_differential(h=h, m=m, props=props)


def _langevin_deriv(x: np.ndarray | float) -> np.ndarray | float:
    """
    Compute the derivative of the Langevin function: L'(x) = 1/x^2 - csch^2(x).

    Uses a Taylor series near x = 0 to avoid catastrophic cancellation::

        L'(x) = 1/3 - x^2/15 + 2*x^4/189 + O(x^6)

    The direct formula requires subtracting two O(1/x^2) terms that nearly
    cancel, so the series threshold is set conservatively at |x| < 1e-4.
    """
    x_arr = np.asarray(x, dtype=float)
    out = np.empty_like(x_arr)

    small = np.abs(x_arr) < 1.0e-4
    large = ~small

    # Series expansion for small x
    xs = x_arr[small]
    out[small] = 1.0 / 3.0 - xs**2 / 15.0 + 2.0 * xs**4 / 189.0

    # Direct evaluation for larger x
    xl = x_arr[large]
    out[large] = 1.0 / xl**2 - 1.0 / np.sinh(xl) ** 2

    if np.isscalar(x):
        return float(out)

    return out


def _stress_field(m: np.ndarray, props: JAProps) -> np.ndarray:
    """
    Compute the stress-induced effective field contribution H_sigma.

    H_sigma = [3 (cos(theta)^2 - nu sin(theta)^2)
               (2 M gamma1 + 4 M^3 gamma2) sigma0] / (2 mu0)
    """
    angle_term = np.cos(props.theta) ** 2 - props.nu * np.sin(props.theta) ** 2
    magnetoelastic_term = 2.0 * m * props.gamma1 + 4.0 * (m**3) * props.gamma2
    return (3.0 * angle_term * magnetoelastic_term * props.sigma0) / (2.0 * MU0)