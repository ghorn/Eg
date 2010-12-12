#!/usr/bin/env python

## 
 # ###################################################################
 #  FiPy - Python-based finite volume PDE solver
 # 
 #  FILE: "input.py"
 #                                    created: 12/16/03 {3:23:47 PM}
 #                                last update: 5/15/06 {2:22:18 PM} 
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

"""

This example solves the steady-state convection-diffusion equation as described in
`./examples/diffusion/convection/exponential1D/input.py` but uses the
`PowerLawConvectionTerm` rather than the `ExponentialConvectionTerm` instatiator.

    >>> L = 10.
    >>> nx = 1000
    >>> from fipy.meshes.grid2D import Grid2D
    >>> mesh = Grid2D(dx = L / nx, nx = nx)

    >>> valueLeft = 0.
    >>> valueRight = 1.

    >>> from fipy.variables.cellVariable import CellVariable
    >>> var = CellVariable(name = "concentration",
    ...                    mesh = mesh,
    ...                    value = valueLeft)

    >>> from fipy.boundaryConditions.fixedValue import FixedValue
    >>> boundaryConditions = (
    ...     FixedValue(mesh.getFacesLeft(), valueLeft),
    ...     FixedValue(mesh.getFacesRight(), valueRight),
    ... )

    >>> diffCoeff = 1.
    >>> convCoeff = (10.,0.)

    >>> from fipy.terms.implicitDiffusionTerm import ImplicitDiffusionTerm
    >>> diffTerm = ImplicitDiffusionTerm(coeff = diffCoeff)

    >>> from fipy.terms.powerLawConvectionTerm import PowerLawConvectionTerm
    >>> eq = diffTerm + PowerLawConvectionTerm(coeff = convCoeff, diffusionTerm = diffTerm)

    >>> from fipy.solvers.linearCGSSolver import LinearCGSSolver
    >>> eq.solve(var = var,
    ...          boundaryConditions = boundaryConditions,
    ...          solver = LinearCGSSolver(tolerance = 1.e-15, iterations = 2000))

The analytical solution test for this problem is given by:

    >>> axis = 0
    >>> x = mesh.getCellCenters()[:,axis]
    >>> from fipy.tools.numerix import exp
    >>> CC = 1. - exp(-convCoeff[axis] * x / diffCoeff)
    >>> DD = 1. - exp(-convCoeff[axis] * L / diffCoeff)
    >>> analyticalArray = CC / DD
    >>> print var.allclose(analyticalArray, rtol = 1e-2, atol = 1e-2) 
    1
   
    >>> if __name__ == '__main__':
    ...     import fipy.viewers
    ...     viewer = fipy.viewers.make(vars = var)
    ...     viewer.plot()
"""
__docformat__ = 'restructuredtext'

if __name__ == '__main__':
    import fipy.tests.doctestPlus
    exec(fipy.tests.doctestPlus._getScript())
    
    raw_input('finished')
  
