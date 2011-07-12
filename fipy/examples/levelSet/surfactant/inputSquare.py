#!/usr/bin/env python

## 
 # ###################################################################
 #  FiPy - Python-based finite volume PDE solver
 # 
 #  FILE: "input.py"
 #                                    created: 11/17/03 {10:29:10 AM} 
 #                                last update: 1/12/06 {8:30:35 PM} { 1:23:41 PM}
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

"""

This example advects a 2 by 2 initially square region outwards.
The example checks for global conservation of surfactant.

Advect the interface and check the position.

   >>> distanceVariable.calcDistanceFunction()
   >>> initialSurfactant = numerix.sum(surfactantVariable)
   >>> for step in range(steps):
   ...     surfactantVariable.updateOld()
   ...     distanceVariable.updateOld()
   ...     surfactantEquation.solve(surfactantVariable)
   ...     advectionEquation.solve(distanceVariable, dt = timeStepDuration)
   >>> print numerix.allclose(initialSurfactant, numerix.sum(surfactantVariable))
   1
 

   
"""
__docformat__ = 'restructuredtext'

import fipy.tools.numerix as numerix

from fipy.meshes.grid2D import Grid2D
from fipy.models.levelSet.distanceFunction.distanceVariable import DistanceVariable
from fipy.models.levelSet.advection.higherOrderAdvectionEquation import buildHigherOrderAdvectionEquation
from fipy.models.levelSet.surfactant.surfactantEquation import SurfactantEquation
from fipy.models.levelSet.surfactant.surfactantVariable import SurfactantVariable

L = 1.
dx = 0.1
velocity = 1.
cfl = 0.1
distanceToTravel = L / 5.
boxSize = .2

nx = int(L / dx)
ny = int(L / dx)

steps = int(distanceToTravel / dx / cfl)

timeStepDuration = cfl * dx / velocity

mesh = Grid2D(dx = dx, dy = dx, nx = nx, ny = ny)

x0 = (L - boxSize) / 2
x1 = (L + boxSize) / 2

distanceVariable = DistanceVariable(
    mesh = mesh,
    value = 1,
    hasOld = 1
    )

x, y = mesh.getCellCenters()[...,0], mesh.getCellCenters()[...,1]
distanceVariable.setValue(-1, where=((x0 < x) & (x < x1)) & ((x0 < y) & (y < x1)))


surfactantVariable = SurfactantVariable(
    distanceVar = distanceVariable,
    value = 1.
    )

surfactantEquation = SurfactantEquation(
    distanceVar = distanceVariable)


advectionEquation = buildHigherOrderAdvectionEquation(
    advectionCoeff = velocity)

if __name__ == '__main__':
    import fipy.viewers
    distanceViewer = fipy.viewers.make(vars = distanceVariable, limits = {'datamin': -.001, 'datamax': .001})
    surfactantViewer = fipy.viewers.make(vars = surfactantVariable, limits = {'datamin': 0., 'datamax': 2.})


    distanceVariable.calcDistanceFunction()

    for step in range(steps):
        print numerix.sum(surfactantVariable)
        surfactantVariable.updateOld()
        distanceVariable.updateOld()
        surfactantEquation.solve(surfactantVariable)
        advectionEquation.solve(distanceVariable, dt = timeStepDuration)
        distanceViewer.plot()
        surfactantViewer.plot()

    surfactantEquation.solve(surfactantVariable)

    distanceViewer.plot()
    surfactantViewer.plot()
    print surfactantVariable
    raw_input('finished')
