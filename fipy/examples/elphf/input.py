#!/usr/bin/env python

## 
 # ###################################################################
 #  FiPy - Python-based finite volume PDE solver
 # 
 #  FILE: "input.py"
 #                                    created: 11/17/03 {10:29:10 AM} 
 #                                last update: 1/12/06 {9:20:39 PM} 
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
This example adds two more components to
``examples/elphf/input1DphaseBinary.py``
one of which is another substitutional species and the other represents 
electrons and diffuses interterstitially.

Parameters from `2004/January/21/elphf0214`

We start by defining a 1D mesh

    >>> from fipy.tools.dimensions.physicalField import PhysicalField as PF
    
    >>> RT = (PF("1 Nav*kB") * PF("298 K"))
    >>> molarVolume = PF("1.80000006366754e-05 m**3/mol")
    >>> Faraday = PF("1 Nav*e")

    >>> from fipy.tools import numerix
    >>> L = PF("3 nm")
    >>> nx = 1200
    >>> dx = L / nx
    >>> # nx = 200
    >>> # dx = PF("0.01 nm")
    >>> ## dx = PF("0.001 nm") * (1.001 - 1/numerix.cosh(numerix.arange(-10, 10, .01)))
    >>> # L = nx * dx
    >>> from fipy.meshes.grid1D import Grid1D
    >>> mesh = Grid1D(dx = dx, nx = nx)
    >>> # mesh = Grid1D(dx = dx)
    >>> # L = mesh.getFacesRight()[0].getCenter()[0] - mesh.getFacesLeft()[0].getCenter()[0]
    >>> # L = mesh.getCellCenters()[-1] - mesh.getCellCenters()[0]


We create the phase field

    >>> timeStep = PF("1e-12 s")
    
    >>> from fipy.variables.cellVariable import CellVariable
    >>> phase = CellVariable(mesh = mesh, name = 'xi', value = 1, hasOld = 1)
    >>> phase.mobility = PF("1 m**3/J/s") / (molarVolume / (RT * timeStep))
    >>> phase.gradientEnergy = PF("3.6e-11 J/m") / (mesh.getScale()**2 * RT / molarVolume)

    >>> def p(xi):
    ...     return xi**3 * (6 * xi**2 - 15 * xi + 10.)
        
    >>> def g(xi):
    ...     return (xi * (1 - xi))**2

    >>> def pPrime(xi):
    ...     return 30. * (xi * (1 - xi))**2
        
    >>> def gPrime(xi):
    ...     return 4 * xi * (1 - xi) * (0.5 - xi)

We create four components

    >>> from fipy.variables.cellVariable import CellVariable
    >>> class ComponentVariable(CellVariable):
    ...     def __init__(self, mesh, value = 0., name = '', standardPotential = 0., barrier = 0., diffusivity = None, valence = 0, equation = None, hasOld = 1):
    ...         self.standardPotential = standardPotential
    ...         self.barrier = barrier
    ...         self.diffusivity = diffusivity
    ...         self.valence = valence
    ...         self.equation = equation
    ...         CellVariable.__init__(self, mesh = mesh, value = value, name = name, hasOld = hasOld)
    ...
    ...     def copy(self):
    ...         return self.__class__(mesh = self.getMesh(), value = self.getValue(), 
    ...                               name = self.getName(), 
    ...                               standardPotential = self.standardPotential, 
    ...                               barrier = self.barrier, 
    ...                               diffusivity = self.diffusivity,
    ...                               valence = self.valence,
    ...                               equation = self.equation,
    ...                               hasOld = 0)

the solvent

    >>> from fipy.tools import numerix
    >>> solvent = ComponentVariable(mesh = mesh, name = 'H2O', value = 1.)
    >>> CnStandardPotential = PF("34139.7265625 J/mol") / RT
    >>> CnBarrier = PF("3.6e5 J/mol") / RT
    >>> CnValence = 0
    
and two solute species

    >>> substitutionals = [
    ...     ComponentVariable(mesh = mesh, name = 'SO4',
    ...                       diffusivity = PF("1e-9 m**2/s") / (mesh.getScale()**2/timeStep),
    ...                       standardPotential = PF("24276.6640625 J/mol") / RT,
    ...                       barrier = CnBarrier,
    ...                       valence = -2,
    ...                       value = PF("0.000010414586295976 mol/l") * molarVolume),
    ...     ComponentVariable(mesh = mesh, name = 'Cu',
    ...                       diffusivity = PF("1e-9 m**2/s") / (mesh.getScale()**2/timeStep),
    ...                       standardPotential = PF("-7231.81396484375 J/mol") / RT,
    ...                       barrier = CnBarrier,
    ...                       valence = +2,
    ...                       value = PF("55.5553718417909 mol/l") * molarVolume)]
    
and one interstitial

    >>> interstitials = [
    ...     ComponentVariable(mesh = mesh, name = 'e-',
    ...                       diffusivity = PF("1e-9 m**2/s") / (mesh.getScale()**2/timeStep),
    ...                       standardPotential = PF("-33225.9453125 J/mol") / RT,
    ...                       barrier = 0.,
    ...                       valence = -1,
    ...                       value = PF("111.110723815414 mol/l") * molarVolume)]

    >>> for component in substitutionals:
    ...     solvent -= component
    ...     component.standardPotential -= CnStandardPotential
    ...     component.barrier -= CnBarrier
    ...     component.valence -= CnValence

Finally, we create the electrostatic potential field

    >>> potential = CellVariable(mesh = mesh, name = 'phi', value = 0.)
    
    >>> permittivity = PF("78.49 eps0") / (Faraday**2 * mesh.getScale()**2 / (RT * molarVolume))

    >>> permittivity = 1.
    >>> permitivityPrime = 0.

The thermodynamic parameters are chosen to give a solid phase rich in electrons 
and the solvent and a liquid phase rich in the two substitutional species

.. warning: Addition and subtraction cause `solvent` to lose some crucial information
   so we only append it after the fact.

..

    >>> solvent.standardPotential = CnStandardPotential
    >>> solvent.barrier = CnBarrier
    >>> solvent.valence = CnValence

Once again, we start with a sharp phase boundary

    >>> x = mesh.getCellCenters()[...,0]
    >>> phase.setValue(x < L / 2)
    >>> interstitials[0].setValue("0.000111111503177394 mol/l" * molarVolume, where=x > L / 2)
    >>> substitutionals[0].setValue("0.249944439430068 mol/l" * molarVolume, where=x > L / 2)
    >>> substitutionals[1].setValue("0.249999982581341 mol/l" * molarVolume, where=x > L / 2)
    
We again create the phase equation as in ``examples.elphf.phase.input1D``

    >>> mesh.setScale(1)

    >>> from fipy.terms.transientTerm import TransientTerm
    >>> from fipy.terms.implicitDiffusionTerm import ImplicitDiffusionTerm
    >>> from fipy.terms.implicitSourceTerm import ImplicitSourceTerm

    >>> phase.equation = TransientTerm(coeff = 1/phase.mobility) \
    ...     == ImplicitDiffusionTerm(coeff = phase.gradientEnergy) \
    ...     - (permitivityPrime / 2.) * potential.getGrad().dot(potential.getGrad())

We linearize the source term in the same way as in `example.phase.simple.input1D`.

    >>> enthalpy = solvent.standardPotential
    >>> barrier = solvent.barrier
    >>> for component in substitutionals + interstitials:
    ...     enthalpy += component * component.standardPotential
    ...     barrier += component * component.barrier
          
    >>> mXi = -(30 * phase * (1 - phase) * enthalpy +  4 * (0.5 - phase) * barrier)
    >>> dmXidXi = (-60 * (0.5 - phase) * enthalpy + 4 * barrier)
    >>> S1 = dmXidXi * phase * (1 - phase) + mXi * (1 - 2 * phase)
    >>> S0 = mXi * phase * (1 - phase) - phase * S1 * (S1 < 0)
    
    >>> phase.equation -= S0 + ImplicitSourceTerm(coeff = S1 * (S1 < 0))
    
and we create the diffustion equation for the solute as in 
``examples.elphf.diffusion.input1D``

    >>> from fipy.terms.implicitSourceTerm import ImplicitSourceTerm
    >>> from fipy.terms.powerLawConvectionTerm import PowerLawConvectionTerm
    
    >>> from fipy.variables.faceVariable import FaceVariable
    >>> for Cj in substitutionals:
    ...     CkSum = ComponentVariable(mesh = mesh, value = 0.)
    ...     CkFaceSum = FaceVariable(mesh = mesh, value = 0.)
    ...     for Ck in [Ck for Ck in substitutionals if Ck is not Cj]:
    ...         CkSum += Ck
    ...         CkFaceSum += Ck.getHarmonicFaceValue()
    ...        
    ...     counterDiffusion = CkSum.getFaceGrad()
    ...     # phaseTransformation = (pPrime(phase.getHarmonicFaceValue()) * Cj.standardPotential 
    ...     #         + gPrime(phase.getHarmonicFaceValue()) * Cj.barrier) * phase.getFaceGrad()
    ...     phaseTransformation = (pPrime(phase).getHarmonicFaceValue() * Cj.standardPotential 
    ...             + gPrime(phase).getHarmonicFaceValue() * Cj.barrier) * phase.getFaceGrad()
    ...     # phaseTransformation = (p(phase).getFaceGrad() * Cj.standardPotential 
    ...     #         + g(phase).getFaceGrad() * Cj.barrier)
    ...     electromigration = Cj.valence * potential.getFaceGrad()
    ...     convectionCoeff = counterDiffusion + \
    ...         solvent.getHarmonicFaceValue() * (phaseTransformation + electromigration)
    ...     convectionCoeff *= (Cj.diffusivity / (1. - CkFaceSum))
    ...
    ...     diffusionTerm = ImplicitDiffusionTerm(coeff = Cj.diffusivity)
    ...     convectionTerm = PowerLawConvectionTerm(coeff = convectionCoeff, 
    ...                                             diffusionTerm = diffusionTerm)
    ...                                            
    ...     Cj.equation = TransientTerm() == diffusionTerm + convectionTerm
    
    >>> for Cj in interstitials:
    ...     # phaseTransformation = (pPrime(phase.getHarmonicFaceValue()) * Cj.standardPotential 
    ...     #         + gPrime(phase.getHarmonicFaceValue()) * Cj.barrier) * phase.getFaceGrad()
    ...     phaseTransformation = (pPrime(phase).getHarmonicFaceValue() * Cj.standardPotential 
    ...             + gPrime(phase).getHarmonicFaceValue() * Cj.barrier) * phase.getFaceGrad()
    ...     # phaseTransformation = (p(phase).getFaceGrad() * Cj.standardPotential 
    ...     #         + g(phase).getFaceGrad() * Cj.barrier)
    ...     electromigration = Cj.valence * potential.getFaceGrad()
    ...     convectionCoeff = Cj.diffusivity * (1 + Cj.getHarmonicFaceValue()) * \
    ...         (phaseTransformation + electromigration)
    ...
    ...     diffusionTerm = ImplicitDiffusionTerm(coeff = Cj.diffusivity)
    ...     convectionTerm = PowerLawConvectionTerm(coeff = convectionCoeff, 
    ...                                             diffusionTerm = diffusionTerm)
    ...                                            
    ...     Cj.equation = TransientTerm() == diffusionTerm + convectionTerm

And Poisson's equation

    >>> charge = 0.
    >>> for Cj in interstitials + substitutionals:
    ...     charge += Cj * Cj.valence

    >>> potential.equation = ImplicitDiffusionTerm(coeff = permittivity) + charge == 0

If running interactively, we create viewers to display the results

    >>> if __name__ == '__main__':
    ...     import fipy.viewers
    ...     from fipy.viewers.gistViewer.gist1DViewer import Gist1DViewer
    ...
    ...     phaseViewer = fipy.viewers.make(vars = phase,
    ...                                     limits = {'datamin': 0, 'datamax': 1})
    ...     concViewer = Gist1DViewer(vars = [solvent] + substitutionals + interstitials, ylog = 1)
    ...     potentialViewer = fipy.viewers.make(vars = potential)
    ...     phaseViewer.plot()
    ...     concViewer.plot()
    ...     potentialViewer.plot()
    ...     raw_input("Press a key to continue")

Again, this problem does not have an analytical solution, so after
iterating to equilibrium

    >>> from fipy.solvers.linearLUSolver import LinearLUSolver
    >>> solver = LinearLUSolver()

    >>> from fipy.solvers.linearCGSSolver import LinearCGSSolver
    >>> solver = LinearCGSSolver(tolerance = 1e-3)

    >>> from fipy.boundaryConditions.fixedValue import FixedValue
    >>> bcs = (FixedValue(faces = mesh.getFacesLeft(), value = 0),)

    >>> phase.residual = CellVariable(mesh = mesh)
    >>> potential.residual = CellVariable(mesh = mesh)
    >>> for Cj in substitutionals + interstitials:
    ...     Cj.residual = CellVariable(mesh = mesh)
    >>> residualViewer = fipy.viewers.make(vars = [phase.residual, potential.residual] + [Cj.residual for Cj in substitutionals + interstitials])
    
    >>> from fipy.viewers.tsvViewer import TSVViewer
    >>> tsv = TSVViewer(vars = [phase, potential] + substitutionals + interstitials)
    
    >>> dt = substitutionals[0].diffusivity * 100
    >>> # dt = 1.
    >>> elapsed = 0.
    >>> maxError = 1e-1
    >>> SAFETY = 0.9
    >>> ERRCON = 1.89e-4
    >>> desiredTimestep = 1.
    >>> thisTimeStep = 0.
    >>> print "%3s: %20s | %20s | %20s | %20s" % ("i", "elapsed", "this", "next dt", "residual")
    >>> residual = 0.
    >>> for i in range(500): # iterate
    ...     if thisTimeStep == 0.:
    ...         tsv.plot(filename = "%s.tsv" % str(elapsed * timeStep))
    ...
    ...     for field in [phase, potential] + substitutionals + interstitials:
    ...         field.updateOld()
    ...
    ...     while 1:
    ...         for j in range(10): # sweep
    ...             print i, j, dt * timeStep, residual
    ...             # raw_input()
    ...             residual = 0.
    ...                 
    ...             phase.equation.solve(var = phase, dt = dt)
    ...             # print phase.name, numerix.max(phase.equation.residual)
    ...             residual = max(numerix.max(phase.equation.residual), residual)
    ...             phase.residual[:] = phase.equation.residual
    ...    
    ...             potential.equation.solve(var = potential, dt = dt, boundaryConditions = bcs)
    ...             # print potential.name, numerix.max(potential.equation.residual)
    ...             residual = max(numerix.max(potential.equation.residual), residual)
    ...             potential.residual[:] = potential.equation.residual
    ...    
    ...             for Cj in substitutionals + interstitials:
    ...                 Cj.equation.solve(var = Cj, 
    ...                                   dt = dt,
    ...                                   solver = solver)
    ...                 # print Cj.name, numerix.max(Cj.equation.residual)
    ...                 residual = max(numerix.max(Cj.equation.residual), residual)
    ...                 Cj.residual[:] = Cj.equation.residual
    ...    
    ...             # print
    ...             # phaseViewer.plot()
    ...             # concViewer.plot()
    ...             # potentialViewer.plot()
    ...             # residualViewer.plot()
    ...    
    ...         residual /= maxError
    ...         if residual <= 1.:
    ...             break	# step succeeded
    ...
    ...         dt = max(SAFETY * dt * residual**-0.2, 0.1 * dt)
    ...         if thisTimeStep + dt == thisTimeStep:
    ...             raise "step size underflow"
    ...
    ...     thisTimeStep += dt
    ...
    ...     if residual > ERRCON:
    ...         dt *= SAFETY * residual**-0.2
    ...     else:
    ...         dt *= 5.
    ...    
    ...     # dt *= (maxError / residual)**0.5
    ...
    ...     if thisTimeStep >= desiredTimestep:
    ...         elapsed += thisTimeStep
    ...         thisTimeStep = 0.
    ...     else:
    ...         dt = min(dt, desiredTimestep - thisTimeStep)
    ...         
    ...     if __name__ == '__main__':    
    ...         phaseViewer.plot()
    ...         concViewer.plot()
    ...         potentialViewer.plot()
    ...         print "%3d: %20s | %20s | %20s | %g" % (i, str(elapsed * timeStep), str(thisTimeStep * timeStep), str(dt * timeStep), residual)


we confirm that the far-field phases have remained separated

    >>> ends = numerix.take(phase, (0,-1))
    >>> numerix.allclose(ends, (1.0, 0.0), rtol = 1e-5, atol = 1e-5)
    1
    
and that the concentration fields has appropriately segregated into into
their respective phases

    >>> ends = numerix.take(interstitials[0], (0,-1))
    >>> numerix.allclose(ends, (0.4, 0.3), rtol = 3e-3, atol = 3e-3)
    1
    >>> ends = numerix.take(substitutionals[0], (0,-1))
    >>> numerix.allclose(ends, (0.3, 0.4), rtol = 3e-3, atol = 3e-3)
    1
    >>> ends = numerix.take(substitutionals[1], (0,-1))
    >>> numerix.allclose(ends, (0.1, 0.2), rtol = 3e-3, atol = 3e-3)
    1
"""
__docformat__ = 'restructuredtext'

## def _test(): 
##     import doctest
##     return doctest.testmod()
##     
## if __name__ == "__main__": 
##     _test() 
##     raw_input("finished")

if __name__ == '__main__':
    ## from fipy.tools.profiler.profiler import Profiler
    ## from fipy.tools.profiler.profiler import calibrate_profiler

    # fudge = calibrate_profiler(10000)
    # profile = Profiler('profile', fudge=fudge)

    import fipy.tests.doctestPlus
    exec(fipy.tests.doctestPlus._getScript())

    # profile.stop()
            
    raw_input("finished")

