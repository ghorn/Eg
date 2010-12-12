#!/usr/bin/env python

## 
 # ###################################################################
 #  FiPy - Python-based finite volume PDE solver
 # 
 #  FILE: "input.py"
 #                                    created: 11/17/03 {10:29:10 AM} 
 #                                last update: 1/12/06 {7:49:01 PM} 
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
 #  2003-11-17 JEG 1.0 original
 # ###################################################################
 ##

r"""
This example combines a phase field problem, as given in
``examples/elphf/phase/input1D.py``,
with a binary diffusion problem, such as described in the ternary example
``examples/elphf/diffusion/input1D.py``,
on a 1D mesh

    >>> nx = 400
    >>> dx = 0.01
    >>> L = nx * dx
    >>> from fipy.meshes.grid1D import Grid1D
    >>> mesh = Grid1D(dx = dx, nx = nx)

We create the phase field

    >>> from fipy.variables.cellVariable import CellVariable
    >>> phase = CellVariable(mesh = mesh, name = 'xi', value = 1, hasOld = 1)
    >>> phase.mobility = 1.
    >>> phase.gradientEnergy = 0.025

    >>> def pPrime(xi):
    ...     return 30. * (xi * (1 - xi))**2
        
    >>> def gPrime(xi):
    ...     return 4 * xi * (1 - xi) * (0.5 - xi)

and a dummy electrostatic potential field

    >>> potential = CellVariable(mesh = mesh, name = 'phi', value = 0.)
    >>> permitivityPrime = 0.

We start with a binary substitutional system

    >>> from fipy.variables.cellVariable import CellVariable
    >>> class ComponentVariable(CellVariable):
    ...     def __init__(self, mesh, value = 0., name = '', 
    ...                  standardPotential = 0., barrier = 0., 
    ...                  diffusivity = None, valence = 0, equation = None, 
    ...                  hasOld = 1):
    ...         self.standardPotential = standardPotential
    ...         self.barrier = barrier
    ...         self.diffusivity = diffusivity
    ...         self.valence = valence
    ...         self.equation = equation
    ...         CellVariable.__init__(self, mesh = mesh, value = value, 
    ...                               name = name, hasOld = hasOld)
    ...
    ...     def copy(self):
    ...         return self.__class__(mesh = self.getMesh(), 
    ...                               value = self.getValue(), 
    ...                               name = self.getName(), 
    ...                               standardPotential = 
    ...                                   self.standardPotential, 
    ...                               barrier = self.barrier, 
    ...                               diffusivity = self.diffusivity,
    ...                               valence = self.valence,
    ...                               equation = self.equation,
    ...                               hasOld = 0)

consisting of the solvent

    >>> solvent = ComponentVariable(mesh = mesh, name = 'Cn', value = 1.)

and the solute

    >>> from fipy.tools.numerix import log, take, allclose
    >>> substitutionals = [
    ...     ComponentVariable(mesh = mesh, name = 'C1',
    ...                       diffusivity = 1., barrier = 0.,
    ...                       standardPotential = log(.3/.7) - log(.7/.3))]
    >>> interstitials = []

    >>> for component in substitutionals:
    ...     solvent -= component

The thermodynamic parameters are chosen to give a solid phase rich 
in the solute and a liquid phase rich in the solvent.

.. warning: Addition and subtraction cause `solvent` to lose some crucial 
   information so we only append it after the fact.

..

    >>> solvent.standardPotential = log(.7/.3)
    >>> solvent.barrier = 1.

We create the phase equation as in ``examples.elphf.phase.input1D``
and create the diffustion equations for the different species as in 
``examples.elphf.diffusion.input1D``

    >>> def makeEquations(phase, substitutionals, interstitials):
    ...     from fipy.terms.transientTerm import TransientTerm
    ...     from fipy.terms.implicitDiffusionTerm import ImplicitDiffusionTerm
    ...     from fipy.terms.implicitSourceTerm import ImplicitSourceTerm
    ...     from fipy.terms.powerLawConvectionTerm import PowerLawConvectionTerm
    ...
    ...     from fipy.variables.faceVariable import FaceVariable
    ...
    ...     phase.equation = TransientTerm(coeff = 1/phase.mobility) \
    ...         == ImplicitDiffusionTerm(coeff = phase.gradientEnergy) \
    ...         - (permitivityPrime / 2.) \
    ...             * potential.getGrad().dot(potential.getGrad())
    ...     enthalpy = solvent.standardPotential
    ...     barrier = solvent.barrier
    ...     for component in substitutionals + interstitials:
    ...         enthalpy += component * component.standardPotential
    ...         barrier += component * component.barrier
    ...
    ...     mXi = -(30 * phase * (1 - phase) * enthalpy 
    ...             +  4 * (0.5 - phase) * barrier)
    ...     dmXidXi = (-60 * (0.5 - phase) * enthalpy + 4 * barrier)
    ...     S1 = dmXidXi * phase * (1 - phase) + mXi * (1 - 2 * phase)
    ...     S0 = mXi * phase * (1 - phase) - phase * S1 * (S1 < 0)
    ... 
    ...     phase.equation -= S0 + ImplicitSourceTerm(coeff = S1 * (S1 < 0))
    ... 
    ...     for Cj in substitutionals:
    ...         CkSum = ComponentVariable(mesh = mesh, value = 0.)
    ...         CkFaceSum = FaceVariable(mesh = mesh, value = 0.)
    ...         for Ck in [Ck for Ck in substitutionals if Ck is not Cj]:
    ...             CkSum += Ck
    ...             CkFaceSum += Ck.getHarmonicFaceValue()
    ...            
    ...         counterDiffusion = CkSum.getFaceGrad()
    ...         phaseTransformation = (pPrime(phase.getHarmonicFaceValue()) \
    ...                 * Cj.standardPotential 
    ...                 + gPrime(phase.getHarmonicFaceValue()) \
    ...                     * Cj.barrier) * phase.getFaceGrad()
    ...         electromigration = Cj.valence * potential.getFaceGrad()
    ...         convectionCoeff = counterDiffusion + \
    ...             solvent.getHarmonicFaceValue() \
    ...                 * (phaseTransformation + electromigration)
    ...         convectionCoeff *= \
    ...             (Cj.diffusivity / (1. - CkFaceSum))
    ...    
    ...         diffusionTerm = ImplicitDiffusionTerm(coeff = Cj.diffusivity)
    ...         convectionTerm = PowerLawConvectionTerm(coeff = convectionCoeff, 
    ...                                           diffusionTerm = diffusionTerm)
    ...                                                
    ...         Cj.equation = TransientTerm() == diffusionTerm + convectionTerm
    ...
    ...     for Cj in interstitials:
    ...         phaseTransformation = (pPrime(phase.getHarmonicFaceValue()) \
    ...             * Cj.standardPotential \
    ...             + gPrime(phase.getHarmonicFaceValue()) \
    ...                 * Cj.barrier) * phase.getFaceGrad()
    ...         electromigration = Cj.valence * potential.getFaceGrad()
    ...         convectionCoeff = Cj.diffusivity \
    ...             * (1 + Cj.getHarmonicFaceValue()) \
    ...             * (phaseTransformation + electromigration)
    ...    
    ...         diffusionTerm = ImplicitDiffusionTerm(coeff = Cj.diffusivity)
    ...         convectionTerm = PowerLawConvectionTerm(coeff = convectionCoeff, 
    ...                                           diffusionTerm = diffusionTerm)
    ...                                                
    ...         Cj.equation = TransientTerm() == diffusionTerm + convectionTerm
    
    >>> makeEquations(phase, substitutionals, interstitials)
    
We start with a sharp phase boundary

.. raw:: latex

   $$ \xi =
   \begin{cases}
       1& \text{for $x \le L/2$,} \\
       0& \text{for $x > L/2$,}
   \end{cases} $$

or

    >>> x = mesh.getCellCenters()[...,0]
    >>> phase.setValue(1.)
    >>> phase.setValue(0., where=x > L / 2)

and with a uniform concentration field

.. raw:: latex

   $C_1 = 0.5$.
   
or

    >>> substitutionals[0].setValue(0.5)

If running interactively, we create viewers to display the results

    >>> if __name__ == '__main__':
    ...     from fipy import viewers
    ...
    ...     viewer = viewers.make(vars = [phase, solvent] \
    ...                                  + substitutionals + interstitials,
    ...                           limits = {'datamin': 0, 'datamax': 1})
    ...     viewer.plot()

This problem does not have an analytical solution, so after
iterating to equilibrium

    >>> from fipy.solvers.linearLUSolver import LinearLUSolver
    >>> solver = LinearLUSolver()

    >>> dt = 10000
    >>> for i in range(5):
    ...     for field in [phase] + substitutionals + interstitials:
    ...         field.updateOld()
    ...     phase.equation.solve(var = phase, dt = dt)
    ...     for field in substitutionals + interstitials:
    ...         field.equation.solve(var = field, 
    ...                              dt = dt,
    ...                              solver = solver)
    ...     if __name__ == '__main__':    
    ...         viewer.plot()

.. image:: examples/elphf/phaseDiffusion/binary.pdf
   :scale: 50
   :align: center

we confirm that the far-field phases have remained separated

    >>> ends = take(phase, (0,-1))
    >>> allclose(ends, (1.0, 0.0), rtol = 1e-5, atol = 1e-5)
    1
    
and that the solute concentration field has appropriately segregated into 
solute-rich and solute-poor phases.

    >>> ends = take(substitutionals[0], (0,-1))
    >>> print allclose(ends, (0.7, 0.3), rtol = 2e-3, atol = 2e-3)
    1

The same system of equations can model a quaternary substitutional system as 
easily as a binary.  Because it depends on the number of substitutional solute 
species in question, we recreate the solvent

    >>> solvent = ComponentVariable(mesh = mesh, name = 'Cn', value = 1.)

and make three new solute species

    >>> substitutionals = [
    ...     ComponentVariable(mesh = mesh, name = 'C1',
    ...                       diffusivity = 1., barrier = 0.,
    ...                       standardPotential = log(.3/.4) - log(.1/.2)),
    ...     ComponentVariable(mesh = mesh, name = 'C2',
    ...                       diffusivity = 1., barrier = 0.,
    ...                       standardPotential = log(.4/.3) - log(.1/.2)),
    ...     ComponentVariable(mesh = mesh, name = 'C3',
    ...                       diffusivity = 1., barrier = 0.,
    ...                       standardPotential = log(.2/.1) - log(.1/.2))]
    
    >>> for component in substitutionals:
    ...     solvent -= component
    >>> solvent.standardPotential = log(.1/.2)
    >>> solvent.barrier = 1.

These thermodynamic parameters are chosen to give a solid phase rich in the
solvent and the first substitutional component and a liquid phase rich in
the remaining two substitutional species.

Again, if we're running interactively, we create a viewer
    
    >>> if __name__ == '__main__':
    ...     viewer = viewers.make(vars = [phase, solvent] \
    ...                                  + substitutionals + interstitials,
    ...                           limits = {'datamin': 0, 'datamax': 1})
    ...     viewer.plot()

We reinitialize the sharp phase boundary

    >>> phase.setValue(1.)
    >>> phase.setValue(0., where=x > L / 2)
    
and the uniform concentration fields, with the substitutional concentrations

.. raw:: latex

   $C_1 = C_2 = 0.35$ and $C_3 = 0.15$.
   
..

    >>> substitutionals[0].setValue(0.35)
    >>> substitutionals[1].setValue(0.35)
    >>> substitutionals[2].setValue(0.15)

We make new equations

    >>> makeEquations(phase, substitutionals, interstitials)

and again iterate to equilibrium

    >>> dt = 10000
    >>> for i in range(5):
    ...     for field in [phase] + substitutionals + interstitials:
    ...         field.updateOld()
    ...     phase.equation.solve(var = phase, dt = dt)
    ...     for field in substitutionals + interstitials:
    ...         field.equation.solve(var = field, 
    ...                              dt = dt,
    ...                              solver = solver)
    ...     if __name__ == '__main__':    
    ...         viewer.plot()

.. image:: examples/elphf/phaseDiffusion/quaternary.pdf
   :scale: 50
   :align: center

We confirm that the far-field phases have remained separated

    >>> ends = take(phase, (0,-1))
    >>> allclose(ends, (1.0, 0.0), rtol = 1e-5, atol = 1e-5)
    1
    
and that the concentration fields have appropriately segregated into 
their respective phases

    >>> ends = take(substitutionals[0], (0,-1))
    >>> allclose(ends, (0.4, 0.3), rtol = 3e-3, atol = 3e-3)
    1
    >>> ends = take(substitutionals[1], (0,-1))
    >>> allclose(ends, (0.3, 0.4), rtol = 3e-3, atol = 3e-3)
    1
    >>> ends = take(substitutionals[2], (0,-1))
    >>> allclose(ends, (0.1, 0.2), rtol = 3e-3, atol = 3e-3)
    1

Finally, we can represent a system that contains both substitutional and 
interstitial species. We recreate the solvent

    >>> solvent = ComponentVariable(mesh = mesh, name = 'Cn', value = 1.)

and two new solute species

    >>> substitutionals = [
    ...     ComponentVariable(mesh = mesh, name = 'C2',
    ...                       diffusivity = 1., barrier = 0.,
    ...                       standardPotential = log(.4/.3) - log(.4/.6)),
    ...     ComponentVariable(mesh = mesh, name = 'C3',
    ...                       diffusivity = 1., barrier = 0.,
    ...                       standardPotential = log(.2/.1) - log(.4/.6))]
    
and one interstitial

    >>> interstitials = [
    ...     ComponentVariable(mesh = mesh, name = 'C1',
    ...                       diffusivity = 1., barrier = 0.,
    ...                       standardPotential = log(.3/.4) - log(1.3/1.4))]


    >>> for component in substitutionals:
    ...     solvent -= component
    >>> solvent.standardPotential = log(.4/.6) - log(1.3/1.4)
    >>> solvent.barrier = 1.

These thermodynamic parameters are chosen to give a solid phase rich in interstitials
and the solvent and a liquid phase rich in the two substitutional species.

Once again, if we're running interactively, we create a viewer
    
    >>> if __name__ == '__main__':
    ...     viewer = viewers.make(vars = [phase, solvent] \
    ...                                  + substitutionals + interstitials,
    ...                           limits = {'datamin': 0, 'datamax': 1})
    ...     viewer.plot()

We reinitialize the sharp phase boundary

    >>> phase.setValue(1.)
    >>> phase.setValue(0., where=x > L / 2)
    
and the uniform concentration fields, with the interstitial
concentration

.. raw:: latex

   $C_1 = 0.35$

..

    >>> interstitials[0].setValue(0.35)

and the substitutional concentrations

.. raw:: latex

   $C_2 = 0.35$ and $C_3 = 0.15$.
   
..

    >>> substitutionals[0].setValue(0.35)
    >>> substitutionals[1].setValue(0.15)

We make new equations

    >>> makeEquations(phase, substitutionals, interstitials)

and again iterate to equilibrium

    >>> dt = 10000
    >>> for i in range(5):
    ...     for field in [phase] + substitutionals + interstitials:
    ...         field.updateOld()
    ...     phase.equation.solve(var = phase, dt = dt)
    ...     for field in substitutionals + interstitials:
    ...         field.equation.solve(var = field, 
    ...                              dt = dt,
    ...                              solver = solver)
    ...     if __name__ == '__main__':    
    ...         viewer.plot()

.. image:: examples/elphf/phaseDiffusion/ternaryAndElectrons.pdf
   :scale: 50
   :align: center

We once more confirm that the far-field phases have remained separated

    >>> ends = take(phase, (0,-1))
    >>> allclose(ends, (1.0, 0.0), rtol = 1e-5, atol = 1e-5)
    1
    
and that the concentration fields have appropriately segregated into 
their respective phases

    >>> ends = take(interstitials[0], (0,-1))
    >>> allclose(ends, (0.4, 0.3), rtol = 3e-3, atol = 3e-3)
    1
    >>> ends = take(substitutionals[0], (0,-1))
    >>> allclose(ends, (0.3, 0.4), rtol = 3e-3, atol = 3e-3)
    1
    >>> ends = take(substitutionals[1], (0,-1))
    >>> allclose(ends, (0.1, 0.2), rtol = 3e-3, atol = 3e-3)
    1
"""
__docformat__ = 'restructuredtext'

if __name__ == "__main__": 
    import fipy.tests.doctestPlus
    exec(fipy.tests.doctestPlus._getScript())
    raw_input("finished")

## if __name__ == '__main__':
##     ## from fipy.tools.profiler.profiler import Profiler
##     ## from fipy.tools.profiler.profiler import calibrate_profiler
## 
##     # fudge = calibrate_profiler(10000)
##     # profile = Profiler('profile', fudge=fudge)
## 
##     import fipy.tests.doctestPlus
##     exec(fipy.tests.doctestPlus.getScript())
## 
##     # profile.stop()
## 	    
##     raw_input("finished")
## 
