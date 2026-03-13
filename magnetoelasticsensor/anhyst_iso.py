"""
anhyst_iso.py

Compute the anhysteretic magnetization term used in the Jiles-Atherton
magnetic hysteresis model.

Equation
--------
Man = Ms * (coth((H + alpha*M)/a) - a/(H + alpha*M))

Equivalent form
---------------
Let:
    x = (H + alpha*M) / a

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


def anhysteretic_magnetization(
    h: float | np.ndarray,
    m: float | np.ndarray,
    ms: float,
    a: float,
    alpha: float,
) -> float | np.ndarray:
    """
    Compute anhysteretic magnetization for the Jiles-Atherton model.

    Parameters
    ----------
    h : float or numpy.ndarray
        Applied magnetic field strength.
    m : float or numpy.ndarray
        Magnetization.
    ms : float
        Saturation magnetization.
    a : float
        Shape parameter for the anhysteretic curve. Must be nonzero.
    alpha : float
        Mean-field coupling parameter.

    Returns
    -------
    float or numpy.ndarray
        Anhysteretic magnetization, with the same broadcasted shape as
        the inputs.

    Raises
    ------
    ValueError
        If `a` is zero.
    """
    if a == 0:
        raise ValueError("Parameter 'a' must be nonzero.")

    h_arr = np.asarray(h, dtype=float)
    m_arr = np.asarray(m, dtype=float)

    x = (h_arr + alpha * m_arr) / a
    man = ms * _langevin(x)

    if np.isscalar(h) and np.isscalar(m):
        return float(man)

    return man


def anhysteretic_magnetization_differential(
    h: float | np.ndarray,
    m: float | np.ndarray,
    ms: float,
    a: float,
    alpha: float,
) -> float | np.ndarray:
    """
    Compute the analytical differential of the anhysteretic curve with
    respect to the applied field H, holding M fixed.

    Formula::

        dMan/dH = Ms * (a / (H + alpha*M)^2 - csch((H + alpha*M)/a)^2 / a)

    The direct closed form is numerically unstable near H + alpha*M = 0,
    so the small-field limit is evaluated with the Langevin-series
    expansion, which yields dMan/dH -> Ms / (3a).

    Parameters
    ----------
    h : float or numpy.ndarray
        Applied magnetic field strength, A/m.
    m : float or numpy.ndarray
        Magnetization, A/m.
    ms : float
        Saturation magnetization, A/m.
    a : float
        Shape parameter. Must be nonzero.
    alpha : float
        Mean-field coupling parameter.

    Returns
    -------
    float or numpy.ndarray
        Analytical differential dMan/dH with the same broadcasted shape as
        the inputs.

    Raises
    ------
    ValueError
        If ``a`` is zero.
    """
    if a == 0:
        raise ValueError("Parameter 'a' must be nonzero.")

    h_arr = np.asarray(h, dtype=float)
    m_arr = np.asarray(m, dtype=float)

    x = (h_arr + alpha * m_arr) / a
    dman_dh = (ms / a) * _langevin_deriv(x)

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
    ms: float,
    a: float,
    alpha: float,
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
    ms : float
        Saturation magnetization, A/m.
    a : float
        Shape parameter. Must be nonzero.
    alpha : float
        Mean-field coupling parameter.

    Returns
    -------
    float or numpy.ndarray
        dMan/dH_eff with the same broadcasted shape as the inputs.

    Raises
    ------
    ValueError
        If ``a`` is zero.
    """
    return anhysteretic_magnetization_differential(
        h=h,
        m=m,
        ms=ms,
        a=a,
        alpha=alpha,
    )


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