#!/usr/bin/env python

## 
 # ###################################################################
 #  FiPy - Python-based finite volume PDE solver
 # 
 #  FILE: "input.py"
 #                                    created: 12/29/03 {3:23:47 PM}
 #                                last update: 1/4/07 {10:17:35 AM} 
 #  Author: Jonathan Guyer <guyer@nist.gov>
 #  Author: Daniel Wheeler <daniel.wheeler@nist.gov>
 #  Author: James Warren   <jwarren@nist.gov>
 #    mail: NIST
 #     www: http://www.ctcms.nist.gov/fipy/
 #  
 # ========================================================================
 # This software was developed at the National Institute of Standards
 # and Technology by employees of the Federal Government in the course
 # of their official duties.  Pursuant to title 17 Section 105 of the
 # United States Code this software is not subject to copyright
 # protection and is in the public domain.  FiPy is an experimental
 # system.  NIST assumes no responsibility whatsoever for its use by
 # other parties, and makes no guarantees, expressed or implied, about
 # its quality, reliability, or any other characteristic.  We would
 # appreciate acknowledgement if the software is used.
 # 
 # This software can be redistributed and/or modified freely
 # provided that any derivative works bear some notice that they are
 # derived from it, and any modified versions bear some notice that
 # they have been modified.
 # ========================================================================
 #  
 #  Description: 
 # 
 #  History
 # 
 #  modified   by  rev reason
 #  ---------- --- --- -----------
 #  2003-11-10 JEG 1.0 original
 # ###################################################################
 ##

r"""

To run this example from the base FiPy directory, type
`examples/phase/simple/input.py` at the command line.  A viewer
object should appear and, after being prompted to step through the different
examples, the word `finished` in the terminal.

This example takes the user through assembling a simple problem with
FiPy.  It describes a steady 1D phase field problem with no-flux
boundary conditions such that,

.. raw:: latex

   \begin{equation}
   \frac{1}{M_\phi}\frac{\partial \phi}{\partial t} =
   \kappa_\phi \nabla^2\phi
   - \frac{\partial f}{\partial \phi}
   \label{eq-phase:simple}
   \end{equation}
    
For solidification problems, the Helmholtz free energy is frequently
given by

.. raw:: latex

   $$ f(\phi,T) = \frac{W}{2}g(\phi) + L_v\frac{T-T_M}{T_M}p(\phi). $$
   where $W$ is the double-well barrier height between phases, $L_v$ is the latent
   heat, $T$ is the temperature, and $T_M$ is the melting point.
   
One possible choice for the double-well function is

.. raw:: latex

   $$g(\phi) = \phi^2(1 - \phi)^2$$
   
and for the interpolation function is

.. raw:: latex

   $$ p(\phi) = \phi^3(6\phi^2 - 15\phi + 10). $$

We create a 1D solution mesh

    >>> L = 1.
    >>> nx = 400
    >>> dx = L / nx

.. raw:: latex

   \IndexClass{Grid1D}

..
    
    >>> from fipy.meshes.grid1D import Grid1D
    >>> mesh = Grid1D(dx = dx, nx = nx)

We create the phase field variable

.. raw:: latex

   \IndexClass{CellVariable}

..

    >>> from fipy.variables.cellVariable import CellVariable
    >>> phase = CellVariable(name = "phase",
    ...                      mesh = mesh)

and set a step-function initial condition

.. raw:: latex

   $$\phi = 
   \begin{cases}
       1 & \text{for $x \le L/2$} \\
       0 & \text{for $x > L/2$}
   \end{cases}
   \quad\text{at $t = 0$}$$

..

    >>> x = mesh.getCellCenters()[...,0]
    >>> phase.setValue(1.)
    >>> phase.setValue(0., where=x > L/2)
    
If we are running interactively, we'll want a viewer to see the results

.. raw:: latex

   \IndexModule{viewers}

..

    >>> if __name__ == '__main__':
    ...     import fipy.viewers
    ...     viewer = fipy.viewers.make(vars = (phase,))
    ...     viewer.plot()
    ...     raw_input("Initial condition. Press <return> to proceed...")

.. image:: examples/phase/simple/step.pdf
   :scale: 50
   :align: center

We choose the parameter values,

    >>> kappa = 0.0025
    >>> W = 1.
    >>> Lv = 1.
    >>> Tm = 1.
    >>> T = Tm
    >>> enthalpy = Lv * (T - Tm) / Tm

We build the equation by assembling the appropriate terms.  Since, with

.. raw:: latex

   $ T = T_M $
   
we are interested in a steady-state solution, we omit the transient term

.. raw:: latex

   $ (1/M_\phi)\frac{\partial \phi}{\partial t}$.
    
The analytical solution for this steady-state phase field problem, in an infinite domain, is

.. raw:: latex

   \begin{equation}
   \phi = \frac{1}{2}\left[1 - \tanh\frac{x-L/2}{2\sqrt{\kappa/W}}\right]
   \label{eq-phase:simple:analytical}
   \end{equation}
   or
   \IndexModule{numerix}
   \IndexFunction{tanh}
   \IndexFunction{sqrt}

..

    >>> x = mesh.getCellCenters()[:,0]
    >>> from fipy.tools.numerix import tanh, sqrt
    >>> analyticalArray = 0.5*(1 - tanh((x - L/2)/(2*sqrt(kappa/W))))

We treat the diffusion term

.. raw:: latex

   $ \kappa_\phi \nabla^2\phi $
  implicitly, 
  \IndexClass{ImplicitDiffusionTerm}

..

    >>> from fipy.terms.implicitDiffusionTerm import ImplicitDiffusionTerm
    >>> diffusionTerm = ImplicitDiffusionTerm(coeff = kappa)

.. note::
    
   "Diffusion" in |FiPy| is not limited to the movement of atoms, but
   rather refers to the spontaneous spreading of any quantity (e.g.,
   solute, temperature, or in this case "phase") by flow "down" the
   gradient of that quantity.
   
The source term is

.. raw:: latex

   \begin{align*}
   S =
   -\frac{\partial f}{\partial \phi} &= -\frac{W}{2}g'(\phi) - L\frac{T-T_M}{T_M}p'(\phi) \\
   &= -\left[W\phi(1-\phi)(1-2\phi) + L\frac{T-T_M}{T_M}30\phi^2(1-\phi)^2\right] \\
   &= m_\phi\phi(1-\phi)
   \end{align*}
   %
   where
   %
   $ m_\phi \equiv -[W(1-2\phi) + 30\phi(1-\phi)L\frac{T-T_M}{T_M}] $.
  
The simplest approach is to add this source explicitly

    >>> mPhi = -((1 - 2 * phase) * W + 30 * phase * (1 - phase) * enthalpy)
    >>> S0 = mPhi * phase * (1 - phase)
    >>> eq = S0 + diffusionTerm
    
After solving this equation

    >>> eq.solve(var = phase)
    
we obtain the surprising result that |phase| is zero everywhere.

    >>> if __name__ == '__main__':
    ...     viewer.plot()
    ...     raw_input("Fully explicit source. Press <return> to proceed...")
    >>> print phase.allclose(analyticalArray, rtol = 1e-4, atol = 1e-4)
    0

.. image:: examples/phase/simple/explicit.pdf
   :scale: 50
   :align: center

On inspection, we can see that this occurs because, for our step-function initial condition, 

.. raw:: latex

   $m_\phi = 0$ everwhere,
   
hence we are actually only solving the simple implicit diffusion equation

.. raw:: latex

   $ \kappa_\phi \nabla^2\phi = 0 $,
   
which has exactly the uninteresting solution we obtained.

The resolution to this problem is to apply relaxation to obtain the desired
answer, i.e., the solution is allowed to relax in time from the initial
condition to the desired equilibrium solution.  To do so, we reintroduce the
transient term from

.. raw:: latex
  
   Equation~\eqref{eq-phase:simple}
   \IndexClass{TransientTerm}

..
    
    >>> from fipy.terms.transientTerm import TransientTerm
    >>> eq = TransientTerm() == diffusionTerm + S0
    
    >>> phase.setValue(1.)
    >>> phase.setValue(0., where=x > L/2)
    
    >>> for i in range(13):
    ...     eq.solve(var = phase)
    ...     if __name__ == '__main__':
    ...         viewer.plot()
    >>> if __name__ == '__main__':
    ...     raw_input("Relaxation, explicit. Press <return> to proceed...")

.. image:: examples/phase/simple/relaxation.pdf
   :scale: 50
   :align: center

After 13 time steps, the solution has converged to the analytical solution

    >>> print phase.allclose(analyticalArray, rtol = 1e-4, atol = 1e-4)
    1

.. note:: The solution is only found accurate to

   .. raw:: latex

      $\approx 4.3\times 10^{-5}$

   because the infinite-domain analytical solution 
   
   .. raw:: latex
   
      \eqref{eq-phase:simple:analytical}
      
   is not an exact representation for the solution in a finite domain of
   length
   
   .. raw:: latex
   
      $L$.

Setting fixed-value boundary conditions of 1 and 0 would still require the
relaxation method with the fully explicit source.

Solution performance can be improved if we exploit the dependence of the
source on |phase|.  By doing so, we can make the source semi-implicit,
improving the rate of convergence over the fully explicit approach.  The
source can only be semi-implicit because we employ sparse linear algebra
routines to solve the PDEs, i.e., there is no fully implicit way to
represent a term like

.. raw:: latex

   $\phi^4$ in the linear set of equations 
   $ \mathsf{M} \vec{\phi} - \vec{b} = 0 $.

By linearizing a source as

.. raw:: latex

   $ S = S_0 - S_1 \phi $,
   
we make it more implicit by adding the coefficient 

.. raw:: latex

   $S_1$
   
to the matrix diagonal.  For numerical stability, this linear coefficient
must never be negative.

There are an infinite number of choices for this linearization, but
many do not converge very well. One choice is that used by Ryo
Kobayashi:

.. raw:: latex

   \IndexClass{ImplicitSourceTerm}

..

    >>> from fipy.terms.implicitSourceTerm import ImplicitSourceTerm
    >>> S0 = mPhi * phase * (mPhi > 0)
    >>> S1 = mPhi * ((mPhi < 0) - phase)
    >>> implicitSource = ImplicitSourceTerm(coeff = S1)
    >>> eq = diffusionTerm + S0 + implicitSource
    
.. note:: Because `mPhi` is a variable field, the quantities `(mPhi > 0)`
   and `(mPhi < 0)` evaluate to variable *fields* of ones and zeroes, instead of 
   simple boolean values.

This expression converges to the same value given by the explicit
relaxation approach, but in only 8 sweeps (note that because there is no
transient term, these sweeps are not time steps, but rather repeated
iterations at the same time step to reach a converged solution).

.. note:: We use `solve()` instead of `sweep()` because we don't care about
   the residual. Either function would work, but `solve()` is a bit faster.
   
..
    
    >>> phase.setValue(1.)
    >>> phase.setValue(0., where=x > L/2)
    
    >>> for i in range(8):
    ...     eq.solve(var = phase)
    >>> if __name__ == '__main__':
    ...     viewer.plot()
    ...     raw_input("Kobayashi, semi-implicit. Press <return> to proceed...")
    >>> print phase.allclose(analyticalArray, rtol = 1e-4, atol = 1e-4)
    1

In general, the best convergence is obtained when the linearization gives a
good representation of the relationship between the source and the
dependent variable.  The best practical advice is to perform a Taylor
expansion of the source about the previous value of the dependent variable
such that 

.. raw:: latex

   $ S = S_\text{old} + \left.\frac{\partial S}{\partial
   \phi}\right\rvert_\text{old} (\phi - \phi_\text{old}) = (S -
   \frac{\partial S}{\partial\phi} \phi)_\text{old} +
   \left.\frac{\partial S}{\partial \phi}\right|_\text{old} \phi $.
   Now, if our source term is represented by $S = S_0 + S_1 \phi$,
   then $ S_1 = \left.\frac{\partial S}{\partial
   \phi}\right|_\text{old} $ and $ S_0 = (S - \frac{\partial
   S}{\partial\phi} \phi)_\text{old} = S_\text{old} - S_1
   \phi_\text{old} $.
   
In this way, the linearized source will be tangent to the curve of the
actual source as a function of the dependendent variable.
    
For our source,

.. raw:: latex

   $ S = m_\phi \phi (1 - \phi)$, 

   $$ \frac{\partial S}{\partial \phi} 
   = \frac{\partial m_\phi}{\partial \phi} \phi (1 - \phi) + m_\phi (1 - 2\phi) $$
   
   and
   
   $$ \frac{\partial m_\phi}{\partial \phi} = 2 W - 30 (1 - 2\phi) L\frac{T-T_M}{T_M}, $$
   
or

    >>> dmPhidPhi = 2 * W - 30 * (1 - 2 * phase) * enthalpy
    >>> S1 = dmPhidPhi * phase * (1 - phase) + mPhi * (1 - 2 * phase)
    >>> S0 = mPhi * phase * (1 - phase) - S1 * phase * (S1 < 0)
    >>> implicitSource = ImplicitSourceTerm(coeff = S1 * (S1 < 0))
    >>> eq = diffusionTerm + S0 + implicitSource
    
Using this scheme, where the coefficient of the implicit source term is
tangent to the source, we reach convergence in only 5 sweeps

    >>> phase.setValue(1.)
    >>> phase.setValue(0., where=x > L/2)
    
    >>> for i in range(5):
    ...     eq.solve(var = phase)
    >>> if __name__ == '__main__':
    ...     viewer.plot()
    ...     raw_input("Tangent, semi-implicit. Press <return> to proceed...")
    >>> print phase.allclose(analyticalArray, rtol = 1e-4, atol = 1e-4)
    1

Although, for this simple problem, there is no appreciable difference in
run-time between the fully explicit source and the optimized semi-implicit
source, the benefit of 60% fewer sweeps should be obvious for larger
systems and longer iterations.
    
-----

This example has focused on just the region of the phase field interface in
equilibrium. Problems of interest, though, usually involve the dynamics of one phase
transforming to another. To that end, let us recast the problem using
physical parameters and dimensions. We'll need a new mesh

    >>> nx = 400
    >>> dx = 5e-6 # cm
    >>> L = nx * dx

    >>> mesh = Grid1D(dx = dx, nx = nx)

and thus must redeclare |phase| on the new mesh

    >>> phase = CellVariable(name="phase",
    ...                      mesh=mesh,
    ...                      hasOld=1)
    >>> x = mesh.getCellCenters()[...,0]
    >>> phase.setValue(1.)
    >>> phase.setValue(0., where=x > L/2)

.. raw:: latex

   We choose the parameter values appropriate for nickel, given in
   \cite{Warren:1995}
   \IndexClass{Variable}

..

    >>> Lv = 2350 # J / cm**3
    >>> Tm = 1728. # K
    >>> from fipy.variables.variable import Variable
    >>> T = Variable(value=Tm)
    >>> enthalpy = Lv * (T - Tm) / Tm # J / cm**3
    
.. raw:: latex

   The parameters of the phase field model can be related to the surface
   energy \( \sigma \) and the interfacial thickness \( \delta  \) by
   \begin{align*} 
       \kappa &= 6\sigma\delta \\
       W &= \frac{6\sigma}{\delta} \\
       M_\phi &= \frac{T_m\beta}{6 L \delta}.
   \end{align*}
   We take \( \delta \approx \Delta x \).

..

    >>> delta = 1.5 * dx
    >>> sigma = 3.7e-5 # J / cm**2
    >>> beta = 0.33 # cm / (K s)
    >>> kappa = 6 * sigma * delta # J / cm
    >>> W = 6 * sigma / delta # J / cm**3
    >>> Mphi = Tm * beta / (6. * Lv * delta) # cm**3 / (J s)

    >>> analyticalArray = CellVariable(name="tanh", mesh=mesh,
    ...                                value=0.5 * (1 - tanh((x - (L / 2. + L / 10.)) 
    ...                                                      / (2 * delta))))

and make a new viewer

    >>> if __name__ == '__main__':
    ...     viewer2 = fipy.viewers.make(vars = (phase, analyticalArray))
    ...     viewer2.plot()

Now we can redefine the transient phase field equation, using the optimal
form of the source term shown above

    >>> mPhi = -((1 - 2 * phase) * W + 30 * phase * (1 - phase) * enthalpy)
    >>> dmPhidPhi = 2 * W - 30 * (1 - 2 * phase) * enthalpy
    >>> S1 = dmPhidPhi * phase * (1 - phase) + mPhi * (1 - 2 * phase)
    >>> S0 = mPhi * phase * (1 - phase) - S1 * phase * (S1 < 0)
    >>> eq = TransientTerm(coeff=1/Mphi) == ImplicitDiffusionTerm(coeff=kappa) \
    ...                         + S0 + ImplicitSourceTerm(coeff = S1 * (S1 < 0))

In order to separate the effect of forming the phase field interface
from the kinetics of moving it, we first equilibrate at the melting
point. We now use the "`sweep()`" method instead of "`solve()`" because we
require the residual.
    
.. raw:: latex

   \IndexFunction{sweep}

..

    >>> timeStep = 1e-6
    >>> for i in range(10):
    ...     phase.updateOld()
    ...     res = 1e+10
    ...     while res > 1e-5:
    ...         res = eq.sweep(var=phase, dt=timeStep)
    >>> if __name__ == '__main__':
    ...     viewer2.plot()

and then quench by 1 K

    >>> T.setValue(T() - 1)

In order to have a stable numerical solution, the interface must not move
more than one grid point per time step, 

.. raw:: latex

   we thus set the timestep according to the grid spacing \( \Delta x \),
   the linear kinetic coefficient \( \beta \), and the undercooling \(
   \abs{T_m - T} \)
   
..

Again we use the "`sweep()`" method as a replacement for "`solve()`".

    >>> velocity = beta * abs(Tm - T()) # cm / s
    >>> timeStep = .1 * dx / velocity # s
    >>> elapsed = 0
    >>> while elapsed < 0.1 * L / velocity:
    ...     phase.updateOld()
    ...     res = 1e+10
    ...     while res > 1e-5:
    ...         res = eq.sweep(var=phase, dt=timeStep)
    ...     elapsed += timeStep
    ...     if __name__ == '__main__':
    ...         viewer2.plot()

A hyperbolic tangent is not an exact steady-state solution given the
quintic polynomial we chose for the ``p()`` function, but it gives a
reasonable approximation.
    
    >>> print phase.allclose(analyticalArray, rtol = 5, atol = 2e-3)
    1
    
.. raw:: latex

   If we had made another common choice of \( p(\phi) = \phi^2(3 - 2\phi)
   \), we would have found much better agreement, as that case does give an
   exact \( \tanh \) solution in steady state.
   
If SciPy is available, another way to compare against the expected result
is to do a least-squared fit to determine the interface velocity and
thickness

.. raw:: latex

   \IndexSoftware{SciPy}

..

    >>> try:
    ...     def tanhResiduals(p, y, x, t):
    ...         V, d = p
    ...         return y - 0.5 * (1 - tanh((x - V * t - L / 2.) / (2*d)))
    ...     from scipy.optimize import leastsq
    ...     x =  mesh.getCellCenters()[...,0]
    ...     (V_fit, d_fit), msg = leastsq(tanhResiduals, [L/2., delta], 
    ...                                   args=(phase(), x, elapsed))
    ... except ImportError:
    ...     V_fit = d_fit = 0
    ...     print "The SciPy library is unavailable to fit the interface \
    ... thickness and velocity"

    >>> print abs(1 - V_fit / velocity) < 3.3e-2
    True
    >>> print abs(1 - d_fit / delta) < 2e-2
    True

    >>> if __name__ == '__main__':
    ...     raw_input("Dimensional, semi-implicit. Press <return> to proceed...")

.. image:: examples/phase/simple/dimensional.pdf
   :scale: 50
   :align: center

.. |phase| raw:: latex

   $ \phi $
   
.. |FiPy| raw:: latex

   \FiPy{}
   
"""
__docformat__ = 'restructuredtext'


if __name__ == '__main__':
    import fipy.tests.doctestPlus
    exec(fipy.tests.doctestPlus._getScript())

    raw_input('finished')

