#!/usr/bin/env python

## 
 # ###################################################################
 #  FiPy - Python-based finite volume PDE solver
 # 
 #  FILE: "input.py"
 #                                    created: 12/29/03 {3:23:47 PM}
 #                                last update: 4/5/05 {5:55:56 PM} 
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
This example is a 1D steady state diffusion test case with a diffusion
coefficient that spatially varies such that

.. raw:: latex

    $$ \frac{\partial }{\partial x} D \frac{\partial \phi}{\partial x} = 0, $$

with boundary conditions

.. raw:: latex

    $\phi = 0$ at $x = 0$ and $D \frac{\partial \phi}{\partial x} = 1$ at $x = L$.

The diffusion coefficient varies with the profile

.. raw:: latex

   $$ D = \begin{cases}
   1& \text{for $0 < x < L / 2$,} \\
   0.1& \text{for $L / 2 \ge x < 3 L / 4$,} \\
   1& \text{for $3 L / 4 \ge x < L$,}
   \end{cases} $$

   where $L$ is the length of the bar.  
   
In this example the diffusion
coefficient is a numerical array that is passed to the diffusion equation.
The diffusion coefficient exists on the faces of the cells and thus has to
be the length of the faces.  It is created in the following way:

   >>> x = mesh.getFaceCenters()[:,0]
   >>> middleFaces = numerix.logical_or(x < L / 4., x >= 3. * L / 4.)
   >>> diffCoeff = numerix.where(middleFaces, 1., 0.1)

The number of cells is only `nx = 2` here. Accurate answers to this
problem are given for any number of cells where `nCells = 4 * i + 2`
where `i` is an integer and of course for large `nCells`. In this example
`nx = 2`.

A simple analytical answer can be used to test the result:
   >>> ImplicitDiffusionTerm(coeff = diffCoeff).solve(var, boundaryConditions = boundaryConditions)
   >>> x = mesh.getCellCenters()[:,0]
   >>> values = x + 18. * L / 4.
   >>> values = numerix.where(x < 3. * L / 4., 10 * x - 9. * L / 4., values)
   >>> values = numerix.where(x < L / 4., x, values)
   >>> print var.allclose(values, atol = 1e-8, rtol = 1e-8)
   1

"""
__docformat__ = 'restructuredtext'

from fipy.tools import numerix

from fipy.boundaryConditions.fixedValue import FixedValue
from fipy.boundaryConditions.fixedFlux import FixedFlux
from fipy.meshes.grid2D import Grid2D
from fipy.solvers.linearPCGSolver import LinearPCGSolver
from fipy.variables.cellVariable import CellVariable
from fipy.terms.implicitDiffusionTerm import ImplicitDiffusionTerm

nx = 2

valueLeft = 0.
fluxRight = 1.
timeStepDuration = 1. 

L = 1.

dx = L / nx

mesh = Grid2D(dx = dx, nx = nx)
    
var = CellVariable(
    name = "solution variable",
    mesh = mesh,
    value = valueLeft)

x = mesh.getFaceCenters()[:,0]
middleFaces = numerix.logical_or(x < L / 4.,x >= 3. * L / 4.)
diffCoeff = numerix.where(middleFaces, 1., 0.1)

boundaryConditions=(FixedValue(mesh.getFacesLeft(),valueLeft),
                    FixedFlux(mesh.getFacesRight(),fluxRight))

if __name__ == '__main__':
    ImplicitDiffusionTerm(coeff = diffCoeff).solve(var, boundaryConditions = boundaryConditions)
    
    import fipy.viewers
    viewer = fipy.viewers.make(vars = var, limits = {'datamax': L + 18. * L / 4.})
    viewer.plot()
    raw_input('finished')
