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