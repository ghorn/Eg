#!/usr/bin/env python

## 
 # ###################################################################
 #  FiPy - Python-based finite volume PDE solver
 # 
 #  FILE: "input.py"
 #                                    created: 12/29/03 {3:23:47 PM}
 #                                last update: 1/12/06 {9:39:34 PM} 
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

This example is a 1D steady state diffusion test case as in
`./examples/diffusion/variable/mesh2x1/input.py` with then
number of cells set to `nx = 10`.

A simple analytical answer can be used to test the result:
   >>> ImplicitDiffusionTerm(coeff = diffCoeff).solve(var, boundaryConditions = boundaryConditions)
   >>> x = mesh.getCellCenters()[:,0]
   >>> from fipy.tools import numerix
   >>> values = numerix.where(x < 3. * L / 4., 10 * x - 9. * L / 4., x + 18. * L / 4.)
   >>> values = numerix.where(x < L / 4., x, values)
   >>> print var.allclose(values, atol = 1e-8, rtol = 1e-8)
   1

"""

from fipy.boundaryConditions.fixedValue import FixedValue
from fipy.boundaryConditions.fixedFlux import FixedFlux
from fipy.meshes.tri2D import Tri2D
from fipy.variables.cellVariable import CellVariable
import fipy.viewers
from fipy.terms.implicitDiffusionTerm import ImplicitDiffusionTerm

nx = 10
ny = 1

valueLeft = 0.
fluxRight = 1.
timeStepDuration = 1. 

L = 10.

dx = L / nx
dy = 1.

mesh = Tri2D(dx, dy, nx, ny)
    
var = CellVariable(
    name = "solution variable",
    mesh = mesh,
    value = valueLeft)

from fipy.variables.faceVariable import FaceVariable
diffCoeff = FaceVariable(mesh = mesh, value = 1.0)

x = mesh.getFaceCenters()[...,0]
diffCoeff.setValue(0.1, where=(L/4. <= x) & (x < 3. * L / 4.))

boundaryConditions=(FixedValue(mesh.getFacesLeft(),valueLeft),
                    FixedFlux(mesh.getFacesRight(),fluxRight))

if __name__ == '__main__':
    ImplicitDiffusionTerm(coeff = diffCoeff).solve(var, boundaryConditions = boundaryConditions)
    viewer = fipy.viewers.make(vars = var)
    viewer.plot()
    raw_input('finished')
