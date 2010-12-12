#!/usr/bin/env python

## -*-Pyth-*-
 # ########################################################################
 # FiPy - a finite volume PDE solver in Python
 # 
 # FILE: "binary.py"
 #                                     created: 4/10/06 {2:20:36 PM}
 #                                 last update: 5/16/06 {1:31:28 PM}
 #  Author: Jonathan Guyer <guyer@nist.gov>
 #  Author: Daniel Wheeler <daniel.wheeler@nist.gov>
 #  Author: James Warren   <jwarren@nist.gov>
 #   mail: NIST
 #    www: <http://www.ctcms.nist.gov/fipy/>
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
 # History
 # 
 # modified   by  rev reason
 # ---------- --- --- -----------
 # 2006-04-10 JEG 1.0 original
 # 
 # ########################################################################
 ##

r"""
It is straightforward to extend a phase field model to include binary alloys.
As in `examples.phase.simple.input`, we will examine a 1D problem

.. raw:: latex

   \IndexClass{Grid1D}

..

    >>> nx = 400
    >>> dx = 5e-6 # cm
    >>> L = nx * dx
    >>> from fipy.meshes.grid1D import Grid1D
    >>> mesh = Grid1D(dx=dx, nx=nx)

.. raw:: latex

   The Helmholtz free energy functional can be written as the integral
   \cite{BoettingerReview:2002,McFaddenReview:2002,Wheeler:1992}
   \[
       \mathcal{F}\left(\phi, C, T\right)
       = \int_\mathcal{V} \left\{
           f(\phi, C, T)
           + \frac{\kappa_\phi}{2}\abs{\nabla\phi}^2
           + \frac{\kappa_C}{2}\abs{\nabla C}^2
       \right\} dV
   \]
   over the volume \( \mathcal{V} \) as a function of phase%
   \footnote{We will find that we need to ``sweep'' this non-linear problem
   (see \emph{e.g.} the composition-dependent diffusivity example in
   \texttt{examples.diffusion.mesh1D}), so we declare \( \phi \) and \( C
   \) to retain an ``old'' value.} \( \phi \)
   \IndexClass{CellVariable}
   
..

    >>> from fipy.variables.cellVariable import CellVariable
    >>> phase = CellVariable(name="phase", mesh=mesh, hasOld=1)

.. raw:: latex

   composition \( C \)
   
..

   >>> C = CellVariable(name="composition", mesh=mesh, hasOld=1)

.. raw:: latex

   and temperature\footnote{we are going to want to
   examine different temperatures in this example, so we declare \( T
   \) as a \texttt{Variable}} \( T \) 
   \IndexClass{Variable}
   
..

    >>> from fipy.variables.variable import Variable
    >>> T = Variable(name="temperature")

.. raw:: latex

   Frequently, the gradient energy term in concentration is ignored and we
   can derive governing equations
   \begin{equation}
       \frac{\partial\phi}{\partial t}
       = M_\phi \left( \kappa_\phi \nabla^2 \phi 
                      - \frac{\partial f}{\partial \phi} \right)
       \label{eq:phase:binary:phase}
   \end{equation}
   for phase and
   \begin{equation}
       \frac{\partial C}{\partial t}
       = \nabla\cdot\left( M_C \nabla \frac{\partial f}{\partial C} \right)
       \label{eq:phase:binary:diffusion}
   \end{equation}
   for solute.
   
   The free energy density \( f(\phi, C, T) \) can be constructed in many
   different ways. One approach is to construct free energy densities for
   each of the pure compoonents, as functions of phase, \emph{e.g.}
   \[
       f_A(\phi, T) = p(\phi) f_A^S(T)
       + \left(1 - p(\phi)\right) f_A^L(T) + \frac{W_A}{2} g(\phi)
   \]
   where \( f_A^L(T) \), \( f_B^L(T) \), \( f_A^S(T) \), and \( f_B^S(T) \)
   are the free energy densities of the pure components. There are a
   variety of choices for the interpolation function \( p(\phi) \) and the
   barrier function \( g(\phi) \), 
   
such as those shown in `examples.phase.simple.input`

    >>> def p(phi):
    ...     return phi**3 * (6 * phi**2 - 15 * phi + 10)

    >>> def g(phi):
    ...     return (phi * (1 - phi))**2
   
.. raw:: latex

   The desired thermodynamic model can then be applied to obtain \( f(\phi,
   C, T) \), such as for a regular solution,
   \begin{align*}
       f(\phi, C, T) &= (1 - C) f_A(\phi, T) + C f_B(\phi, T) \\
       &\qquad + R T \left[
           (1 - C) \ln (1 - C) + C \ln C
       \right]
       + C (1 - C) \left[ 
           \Omega_S p(\phi)
           + \Omega_L \left( 1 - p(\phi) \right)
       \right]
   \end{align*}
   where
   
..

    >>> R = 8.314 # J / (mol K)

.. raw:: latex
   
   is the gas constant and \( \Omega_S \) and \( \Omega_L \) are the
   regular solution interaction parameters for solid and liquid.

   Another approach is useful when the free energy densities \( f^L(C, T)
   \) and \( f^S(C,T) \) of the alloy in the solid and liquid phases are
   known. This might be the case when the two different phases have
   different thermodynamic models or when one or both is obtained from a
   Calphad code. In this case, we can construct
   \[
       f(\phi, C, T) = p(\phi) f^S(C,T) 
       + \left(1 - p(\phi)\right) f^L(C, T)
       + \left[
           (1-C) \frac{W_A}{2} + C \frac{W_B}{2}
       \right] g(\phi).
   \]
   When the thermodynamic models are the same in both phases, both
   approaches should yield the same result.
   
   We choose the first approach and make the simplifying assumptions of an
   ideal solution and that
   \begin{align*}
       f_A^L(T) & = 0 \\
       f_A^S(T) - f_A^L(T) &= \frac{L_A\left(T - T_M^A\right)}{T_M^A}
   \end{align*}
   and likewise for component \( B \). 
   
..

    >>> LA = 2350. # J / cm**3
    >>> LB = 1728. # J / cm**3
    >>> TmA = 1728. # K
    >>> TmB = 1358. # K

    >>> enthalpyA = LA * (T - TmA) / TmA
    >>> enthalpyB = LB * (T - TmB) / TmB

.. raw:: latex
    
   This relates the difference between the free energy densities of the
   pure solid and pure liquid phases to the latent heat \( L_A \) and the
   pure component melting point \( T_M^A \), such that
   \[
       f_A(\phi, T) = \frac{L_A\left(T - T_M^A\right)}{T_M^A} p(\phi) 
       + \frac{W_A}{2} g(\phi).
   \]
   With these assumptions
   \begin{align}
       \frac{\partial f}{\partial \phi}
       &= (1-C) \frac{\partial f_A}{\partial \phi} 
       + C \frac{\partial f_A}{\partial \phi} \nonumber \\
       &= \left\{
           (1-C) \frac{L_A\left(T - T_M^A\right)}{T_M^A}
           + C \frac{L_B\left(T - T_M^B\right)}{T_M^B} 
       \right\} p'(\phi)
       + \left\{
         (1-C) \frac{W_A}{2} + C \frac{W_B}{2}  
       \right\} g'(\phi)
       \label{eq:phase:binary:phaseTransformation}
       \\
     \intertext{and}
       \frac{\partial f}{\partial C}
       &= \left[f_B(\phi, T) + \frac{R T}{V_m} \ln C\right] 
       - \left[f_A(\phi, T) + \frac{R T}{V_m} \ln (1-C) \right] \nonumber \\
       &= \left[\mu_B(\phi, C, T) - \mu_A(\phi, C, T) \right] / V_m
       \label{eq:phase:binary:chemicalPotential}
   \end{align}
   where \( \mu_A \) and \( \mu_B \) are the classical chemical potentials
   for the binary species. \( p'(\phi) \) and \( g'(\phi) \) are the
   partial derivatives of of \( p \) and \( g \) with respect to \( \phi \)
   
..

   >>> def pPrime(phi):
   ...     return 30. * g(phi)

   >>> def gPrime(phi):
   ...     return 2. * phi * (1 - phi) * (1 - 2 * phi)

.. raw:: latex
   
   \( V_m \) is the molar volume, which we take to be independent of
   concentration and phase
   
..

    >>> Vm = 7.42 # cm**3 / mol
   
On comparison with `examples.phase.simple.input`, we can see that the
present form of the phase field equation is identical to the one found
earlier, with the source now composed of the concentration-weighted average
of the source for either pure component. We let the pure component barriers
equal the previous value

    >>> deltaA = deltaB = 1.5 * dx
    >>> sigmaA = 3.7e-5 # J / cm**2
    >>> sigmaB = 2.9e-5 # J / cm**2
    >>> betaA = 0.33 # cm / (K s)
    >>> betaB = 0.39 # cm / (K s)
    >>> kappaA = 6 * sigmaA * deltaA # J / cm
    >>> kappaB = 6 * sigmaB * deltaB # J / cm
    >>> WA = 6 * sigmaA / deltaA # J / cm**3
    >>> WB = 6 * sigmaB / deltaB # J / cm**3
    
and define the averages

    >>> W = (1 - C) * WA / 2. + C * WB / 2.
    >>> enthalpy = (1 - C) * enthalpyA + C * enthalpyB

We can now linearize the source exactly as before

    >>> mPhi = -((1 - 2 * phase) * W + 30 * phase * (1 - phase) * enthalpy)
    >>> dmPhidPhi = 2 * W - 30 * (1 - 2 * phase) * enthalpy
    >>> S1 = dmPhidPhi * phase * (1 - phase) + mPhi * (1 - 2 * phase)
    >>> S0 = mPhi * phase * (1 - phase) - S1 * phase * (S1 < 0)

Using the same gradient energy coefficient and phase field mobility

    >>> kappa = (1 - C) * kappaA + C * kappaB
    >>> Mphi = TmA * betaA / (6 * LA * deltaA)

we define the phase field equation

.. raw:: latex

   \IndexClass{TransientTerm}
   \IndexClass{ImplicitDiffusionTerm}
   \IndexClass{ImplicitSourceTerm}

..

    >>> from fipy.terms.transientTerm import TransientTerm
    >>> from fipy.terms.implicitDiffusionTerm import ImplicitDiffusionTerm
    >>> from fipy.terms.implicitSourceTerm import ImplicitSourceTerm

    >>> phaseEq = TransientTerm(1/Mphi) == ImplicitDiffusionTerm(coeff=kappa) \
    ...   + S0 + ImplicitSourceTerm(coeff=S1 * (S1 < 0))

-----

.. raw:: latex

   When coding explicitly, it is typical to simply write a function to
   evaluate the chemical potentials \( \mu_A \) and \( \mu_B \) and then
   perform the finite differences necessary to calculate their gradient and
   divergence, e.g., 

..

::
    
    def deltaChemPot(phase, C, T):
        return ((Vm * (enthalpyB * p(phase) + WA * g(phase)) + R * T * log(1 - C)) -
                (Vm * (enthalpyA * p(phase) + WA * g(phase)) + R * T * log(C)))
    
    for j in range(faces):
        flux[j] = ((Mc[j+.5] + Mc[j-.5]) / 2) \
          * (deltaChemPot(phase[j+.5], C[j+.5], T) \
            - deltaChemPot(phase[j-.5], C[j-.5], T)) / dx
        
    for j in range(cells):
        diffusion = (flux[j+.5] - flux[j-.5]) / dx
        
where we neglect the details of the outer boundaries (``j = 0`` and ``j =
N``) or exactly how to translate ``j+.5`` or ``j-.5`` into an array index,
much less the complexities of higher dimensions. FiPy can handle all of
these issues automatically, so we could just write::

    chemPotA = Vm * (enthalpyA * p(phase) + WA * g(phase)) + R * T * log(C)
    chemPotB = Vm * (enthalpyB * p(phase) + WB * g(phase)) + R * T * log(1-C)
    flux = Mc * (chemPotB - chemPotA).getFaceGrad()
    eq = TransientTerm() == flux.getDivergence()

.. raw:: latex

   Although the second syntax would essentially work as written, such an
   explicit implementation would be very slow. In order to take advantage
   of \FiPy{}'s implicit solvers, it is necessary to reduce
   Eq.~\eqref{eq:phase:binary:diffusion} to the canonical form of
   Eq.~\eqref{eqn:num:gen}, hence we must expand
   Eq.~\eqref{eq:phase:binary:chemicalPotential} as
   \[
       \frac{\partial f}{\partial C} 
       = \left[
           \frac{L_B\left(T - T_M^B\right)}{T_M^B} 
           - \frac{L_A\left(T - T_M^A\right)}{T_M^A}
       \right] p(\phi)
       + \frac{R T}{V_m} \left[\ln C - \ln (1-C)\right]
       + \frac{W_B - W_A}{2} g(\phi)
   \]
   In either bulk phase, \( \nabla p(\phi) = \nabla g(\phi) = 0 \), so
   we can then reduce Eq.~\eqref{eq:phase:binary:diffusion} to
   \begin{align}
       \frac{\partial C}{\partial t}
       &= \nabla\cdot\left( M_C \nabla \left\{
           \frac{R T}{V_m} \left[\ln C - \ln (1-C)\right]
       \right\}
       \right) \nonumber \\
       &= \nabla\cdot\left[ 
           \frac{M_C R T}{C (1-C) V_m} \nabla C
       \right]
       \label{eq:phase:binary:diffusion:bulk}
   \end{align}
   and, by comparison with Fick's second law
   \[
       \frac{\partial C}{\partial t}
       = \nabla\cdot\left[D \nabla C\right],
   \]
   we can associate the mobility \( M_C \) with the intrinsic diffusivity \( D \) by 
   \( M_C \equiv D C (1-C) V_m / R T \) and write Eq.~\eqref{eq:phase:binary:diffusion} as
   \begin{align}
       \frac{\partial C}{\partial t}
       &= \nabla\cdot\left( D \nabla C \right) \nonumber \\
       &\qquad + \nabla\cdot\left(
       \frac{D C (1 - C) V_m}{R T}
       \left\{
           \left[
               \frac{L_B\left(T - T_M^B\right)}{T_M^B} 
               - \frac{L_A\left(T - T_M^A\right)}{T_M^A}
           \right] \nabla p(\phi)
           + \frac{W_B - W_A}{2} \nabla g(\phi)  
       \right\}
       \right).
       \label{eq:phase:binary:diffusion:canonical}
   \end{align}
   The first term is clearly a \texttt{DiffusionTerm}. The second is less
   obvious, but by factoring out \( C \), we can see that this is a
   \texttt{ConvectionTerm} with a velocity
   \[
       \vec{u}_\phi = 
       \frac{D (1 - C) V_m}{R T}
       \left\{
           \left[
               \frac{L_B\left(T - T_M^B\right)}{T_M^B} 
               - \frac{L_A\left(T - T_M^A\right)}{T_M^A}
           \right] \nabla p(\phi)
           + \frac{W_B - W_A}{2} \nabla g(\phi)  
       \right\}
   \]
   due to phase transformation, such that
   \[
       \frac{\partial C}{\partial t}
       = \nabla\cdot\left( D \nabla C \right) + \nabla\cdot\left(C \vec{u}_\phi\right)
   \]
   
or

    >>> Dl = Variable(value=1e-5) # cm**2 / s
    >>> Ds = Variable(value=1e-9) # cm**2 / s
    >>> D = (Dl - Ds) * phase.getArithmeticFaceValue() + Dl
    >>> diffusion = ImplicitDiffusionTerm(coeff=D)

    >>> phaseTransformationVelocity = \
    ...  ((enthalpyB - enthalpyA) * p(phase).getFaceGrad()
    ...   + 0.5 * (WB - WA) * g(phase).getFaceGrad()) \
    ...   * D * (1. - C).getHarmonicFaceValue() * Vm / (R * T)

.. raw:: latex

   \IndexClass{PowerLawConvectionTerm}

..
    
    >>> from fipy.terms.powerLawConvectionTerm import PowerLawConvectionTerm
    >>> diffusionEq = TransientTerm() == diffusion \
    ...   + PowerLawConvectionTerm(coeff=phaseTransformationVelocity,
    ...                            diffusionTerm=diffusion)

-----

We initialize the phase field to a step function in the middle of the domain

    >>> phase.setValue(1.)
    >>> phase.setValue(0., where=mesh.getCellCenters()[...,0] > L/2.)

.. raw:: latex

   and start with a uniform composition field \( C = 1/2 \)
   
..

    >>> C.setValue(0.5)


.. raw:: latex

   In equilibrium, \( \mu_A(0, C_L, T) = \mu_A(1, C_S, T) \) and \(
   \mu_B(0, C_L, T) = \mu_B(1, C_S, T) \) and, for ideal solutions, we can
   deduce the liquidus and solidus compositions as
   \begin{align*}
       C_L &= \frac{1 - \exp\left(-\frac{L_A\left(T - T_M^A\right)}{T_M^A}\frac{V_m}{R T}\right)}
       {\exp\left(-\frac{L_B\left(T - T_M^B\right)}{T_M^B}\frac{V_m}{R T}\right) 
       - \exp\left(-\frac{L_A\left(T - T_M^A\right)}{T_M^A}\frac{V_m}{R T}\right)} \\
       C_S &= \exp\left(-\frac{L_B\left(T - T_M^B\right)}{T_M^B}\frac{V_m}{R T}\right) C_L
   \end{align*}
   \IndexModule{numerix}
   \IndexFunction{exp}
   
..

    >>> from fipy.tools.numerix import exp
    >>> Cl = (1. - exp(-enthalpyA * Vm / (R * T))) \
    ...   / (exp(-enthalpyB * Vm / (R * T)) - exp(-enthalpyA * Vm / (R * T)))
    >>> Cs = exp(-enthalpyB * Vm / (R * T)) * Cl

The phase fraction is predicted by the lever rule

    >>> Cavg = C.getCellVolumeAverage()
    >>> fraction = (Cl - Cavg) / (Cl - Cs)

For the special case of ``fraction = Cavg = 0.5``, a little bit of algebra
reveals that the temperature that leaves the phase fraction unchanged is
given by
    
    >>> T.setValue((LA + LB) * TmA * TmB / (LA * TmB + LB * TmA))

In this simple, binary, ideal solution case, we can derive explicit
expressions for the solidus and liquidus compositions. In general, this may
not be possible or practical. In that event, the root-finding facilities in
SciPy can be used.

   
.. raw:: latex

   We'll need a function to return the two conditions for equilibrium
   \begin{align*}
       0 = \mu_A(1, C_S, T) - \mu_A(0, C_L, T) &= 
       \frac{L_A\left(T - T_M^A\right)}{T_M^A} V_m 
       + R T \ln (1 - C_S) - R T \ln (1 - C_L) \\
       0 = \mu_B(1, C_S, T) - \mu_B(0, C_L, T) &= 
       \frac{L_B\left(T - T_M^B\right)}{T_M^B} V_m
       + R T \ln C_S - R T \ln C_L
   \end{align*}
   \IndexModule{numerix}
   \IndexFunction{log}
   \IndexFunction{array}

..

    >>> from fipy.tools.numerix import log
    >>> from fipy.tools.numerix import array
    >>> def equilibrium(C):
    ...     return [array(enthalpyA * Vm + R * T * log(1 - C[0]) - R * T * log(1 - C[1])),
    ...             array(enthalpyB * Vm + R * T * log(C[0]) - R * T * log(C[1]))]
               
.. raw:: latex

   and we'll have much better luck if we also supply the Jacobian
   \[\left[\begin{matrix} 
       \frac{\partial(\mu_A^S - \mu_A^L)}{\partial C_S}
       & \frac{\partial(\mu_A^S - \mu_A^L)}{\partial C_L} \\
       \frac{\partial(\mu_B^S - \mu_B^L)}{\partial C_S}
       & \frac{\partial(\mu_B^S - \mu_B^L)}{\partial C_L}
   \end{matrix}\right]
   = 
   R T\left[\begin{matrix} 
       -\frac{1}{1-C_S} & \frac{1}{1-C_L} \\
       \frac{1}{C_S} & -\frac{1}{C_L}
   \end{matrix}\right]\]
   
..

    >>> def equilibriumJacobian(C):
    ...     return R * T * array([[-1. / (1 - C[0]), 1. / (1 - C[1])],
    ...                           [ 1. / C[0],      -1. / C[1]]])

.. raw:: latex

   \IndexSoftware{SciPy}

..

    >>> try:
    ...     from scipy.optimize import fsolve
    ...     CsRoot, ClRoot = fsolve(func=equilibrium, x0=[0.5, 0.5], 
    ...                             fprime=equilibriumJacobian)
    ... except ImportError:
    ...     ClRoot = CsRoot = 0
    ...     print "The SciPy library is not available to calculate the solidus and \
    ... liquidus concentrations"

    >>> print Cl.allclose(ClRoot)
    1
    >>> print Cs.allclose(CsRoot)
    1

We plot the result against the sharp interface solution

    >>> sharp = CellVariable(name="sharp", mesh=mesh)
    >>> x = mesh.getCellCenters()[...,0]
    >>> sharp.setValue(Cs, where=x < L * fraction)
    >>> sharp.setValue(Cl, where=x >= L * fraction)

.. raw:: latex

   \IndexModule{viewers}

..

    >>> if __name__ == '__main__':
    ...     from fipy import viewers
    ...     viewer = viewers.make(vars=(phase, C, sharp), 
    ...                           limits={'datamin': 0., 'datamax': 1.})
    ...     viewer.plot()

Because the phase field interface will not move, and because we've seen in
earlier examples that the diffusion problem is unconditionally stable, we
need take only one very large timestep to reach equilibrium

    >>> dt = 1.e2

Because the phase field equation is coupled to the composition through
``enthalpy`` and ``W`` and the diffusion equation is coupled to the phase
field through ``phaseTransformationVelocity``, it is necessary sweep this
non-linear problem to convergence. We use the "residual" of the equations
(a measure of how well they think they have solved the given set of linear
equations) as a test for how long to sweep. Because of the
``ConvectionTerm``, the solution matrix for ``diffusionEq`` is asymmetric
and cannot be solved by the default ``LinearPCGSolver``. Therefore, we use a
``LinearLUSolver`` for this equation.

.. raw:: latex

   \IndexClass{LinearLUSolver}
   \IndexFunction{solve}
   \IndexFunction{sweep}

..

We now use the "`sweep()`" method instead of "`solve()`" because we
require the residual.

    >>> from fipy.solvers.linearLUSolver import LinearLUSolver
    >>> solver = LinearLUSolver(tolerance=1e-10)

    >>> phase.updateOld()
    >>> C.updateOld()
    >>> phaseRes = 1e+10
    >>> diffRes = 1e+10
    >>> while phaseRes > 1e-3 or diffRes > 1e-3:
    ...     phaseRes = phaseEq.sweep(var=phase, dt=dt)
    ...     diffRes = diffusionEq.sweep(var=C, dt=dt, solver=solver)
    >>> if __name__ == '__main__':
    ...     viewer.plot()
    ...     raw_input("stationary phase field")

.. image:: examples/phase/binary/stationary.pdf
   :scale: 50
   :align: center

We verify that the bulk phases have shifted to the predicted solidus and
liquidus compositions

    >>> print Cs.allclose(C[0], atol=2e-4)
    1
    >>> print Cl.allclose(C[nx-1], atol=2e-4)
    1

and that the phase fraction remains unchanged

    >>> print fraction.allclose(phase.getCellVolumeAverage(), atol=2e-4)
    1

while conserving mass overall

    >>> print Cavg.allclose(0.5, atol=1e-8)
    1

-----

We now quench by ten degrees

    >>> T.setValue(T() - 10.) # K

    >>> sharp.setValue(Cs, where=x < L * fraction)
    >>> sharp.setValue(Cl, where=x >= L * fraction)

Because this lower temperature will induce the phase interface to move
(solidify), we will need to take much smaller timesteps (the time scales of
diffusion and of phase transformation compete with each other).

    >>> dt = 1.e-6

    >>> for i in range(100):
    ...     phase.updateOld()
    ...     C.updateOld()
    ...     phaseRes = 1e+10
    ...     diffRes = 1e+10
    ...     while phaseRes > 1e-3 or diffRes > 1e-3:
    ...         phaseRes = phaseEq.sweep(var=phase, dt=dt)
    ...         diffRes = diffusionEq.sweep(var=C, dt=dt, solver=solver)
    ...     if __name__ == '__main__':
    ...         viewer.plot()

    >>> if __name__ == '__main__': 
    ...     raw_input("moving phase field")

.. image:: examples/phase/binary/moving.pdf
   :scale: 50
   :align: center

We see that the composition on either side of the interface approach the
sharp-interface solidus and liquidus, but it will take a great many more
timesteps to reach equilibrium. If we waited sufficiently long, we
could again verify the final concentrations and phase fraction against the
expected values. 
"""

__docformat__ = 'restructuredtext'

if __name__ == '__main__':
    import fipy.tests.doctestPlus
    exec(fipy.tests.doctestPlus._getScript())
