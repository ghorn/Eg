#!/usr/bin/env python

## 
 # ###################################################################
 #  FiPy - Python-based finite volume PDE solver
 # 
 #  FILE: "input.py"
 #                                    created: 12/29/03 {3:23:47 PM}
 #                                last update: 4/7/05 {4:34:20 PM} 
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

To run this example from the base fipy directory type::
    
    $ examples/diffusion/steadyState/mesh1D/tri2Dinput.py
    
at the command line. A contour plot should appear and the word `finished`
in the terminal.

This example is similar to the example found in::
    
    $ examples/diffusion/steadyState/mesh1D/input.py
    
However, the `mesh` is a `Tri2D` object rather than a `Grid2D` object.

Here, one time step is execcuted to implicitly find the steady state
solution.

    >>> ImplicitDiffusionTerm().solve(var, boundaryConditions = boundaryConditions)

To test the solution, the analytical result is required. The `x`
coordinates from the mesh are gathered and the length of the domain,
`Lx`, is calculated.  An array, `analyticalArray`, is calculated to
compare with the numerical result,

    >>> x = mesh.getCellCenters()[:,0]
    >>> Lx = nx * dx
    >>> analyticalArray = valueLeft + (valueRight - valueLeft) * x / Lx

Finally the analytical and numerical results are compared with a
tolerance of `1e-10`. 

    >>> print var.allclose(analyticalArray)
    1

"""

__docformat__ = 'restructuredtext'

from fipy.variables.cellVariable import CellVariable
from fipy.boundaryConditions.fixedValue import FixedValue
import fipy.viewers
from fipy.meshes.tri2D import Tri2D
from fipy.terms.implicitDiffusionTerm import ImplicitDiffusionTerm

nx = 50
dx = 1.

mesh = Tri2D(dx = dx, nx = nx)

valueLeft = 0
valueRight = 1
var = CellVariable(name = "solution-variable", mesh = mesh, value = valueLeft)

boundaryConditions = (FixedValue(mesh.getFacesLeft(),valueLeft), FixedValue(mesh.getFacesRight(),valueRight))

if __name__ == '__main__':
    from fipy.terms.implicitDiffusionTerm import ImplicitDiffusionTerm
    ImplicitDiffusionTerm().solve(var, boundaryConditions = boundaryConditions)
    viewer = fipy.viewers.make(vars = var)
    viewer.plot()
    raw_input("finished")
