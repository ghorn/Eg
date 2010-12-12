#!/usr/bin/env python

## 
 # ###################################################################
 #  FiPy - Python-based finite volume PDE solver
 # 
 #  FILE: "input.py"
 #                                    created: 11/17/03 {10:29:10 AM} 
 #                                last update: 5/15/06 {2:44:02 PM} { 1:23:41 PM}
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

Here we solve the level set equation in two dimensions for a circle. The 2D
level set equation can be written,

.. raw:: latex

    $$ | \nabla \phi | = 1$$

and the boundary condition for a circle is given by,

.. raw:: latex

    $ \phi = 0 $ at $(x - L / 2)^2 + (y - L / 2)^2 = (L / 4)^2 $.

The solution to this problem will be demonstrated in the following
script. Firstly, setup the parameters.

   >>> dx = 1.
   >>> dy = 1.
   >>> nx = 11
   >>> ny = 11
   >>> Lx = nx * dx
   >>> Ly = ny * dy

Construct the mesh.

.. raw:: latex

   \IndexClass{Grid2D}

..

   >>> from fipy.meshes.grid2D import Grid2D
   >>> mesh = Grid2D(dx=dx, dy=dy, nx=nx, ny=ny)

Construct a `distanceVariable` object.

.. raw:: latex

   \IndexClass{DistanceVariable}

..

   >>> from fipy.models.levelSet.distanceFunction.distanceVariable \
   ...     import DistanceVariable
   >>> var = DistanceVariable(name='level set variable',
   ...                        mesh=mesh,
   ...                        value=-1,
   ...                        hasOld=1)

   >>> x, y = mesh.getCellCenters()[...,0], mesh.getCellCenters()[...,1]
   >>> var.setValue(1, where=(x - Lx / 2.)**2 + (y - Ly / 2.)**2 < (Lx / 4.)**2)

   >>> var.calcDistanceFunction()
   
.. raw:: latex

   \IndexModule{viewers}

..

   >>> if __name__ == '__main__':
   ...     from fipy import viewers
   ...     viewer = viewers.make(vars = var, 
   ...                           limits = {'datamin': -5., 'datamax': 5.})
   ...     viewer.plot()

The result can be tested with the following commands.

.. raw:: latex

   \IndexModule{numerix}

..

   >>> dY = dy / 2.
   >>> dX = dx / 2.
   >>> mm = min (dX, dY)
   >>> from fipy.tools import numerix
   >>> m1 = dY * dX / numerix.sqrt(dY**2 + dX**2)
   >>> def evalCell(phix, phiy, dx, dy):
   ...     aa = dy**2 + dx**2
   ...     bb = -2 * ( phix * dy**2 + phiy * dx**2)
   ...     cc = dy**2 * phix**2 + dx**2 * phiy**2 - dx**2 * dy**2
   ...     sqr = numerix.sqrt(bb**2 - 4. * aa * cc)
   ...     return ((-bb - sqr) / 2. / aa,  (-bb + sqr) / 2. / aa)
   >>> v1 = evalCell(-dY, -m1, dx, dy)[0] 
   >>> v2 = evalCell(-m1, -dX, dx, dy)[0]
   >>> v3 = evalCell(m1,  m1,  dx, dy)[1]
   >>> v4 = evalCell(v3, dY, dx, dy)[1]
   >>> v5 = evalCell(dX, v3, dx, dy)[1]
   >>> MASK = -1000
   >>> trialValues = numerix.MA.masked_values((
   ...     MASK,  MASK, MASK, MASK, MASK, MASK, MASK, MASK, MASK, MASK, MASK,
   ...     MASK,  MASK, MASK, MASK,-3*dY,-3*dY,-3*dY, MASK, MASK, MASK, MASK,
   ...     MASK,  MASK, MASK,   v1,  -dY,  -dY,  -dY,   v1, MASK, MASK, MASK,
   ...     MASK,  MASK,   v2,  -m1,   m1,   dY,   m1,  -m1,   v2, MASK, MASK,
   ...     MASK, -dX*3,  -dX,   m1,   v3,   v4,   v3,   m1,  -dX,-dX*3, MASK,
   ...     MASK, -dX*3,  -dX,   dX,   v5, MASK,   v5,   dX,  -dX,-dX*3, MASK,
   ...     MASK, -dX*3,  -dX,   m1,   v3,   v4,   v3,   m1,  -dX,-dX*3, MASK,
   ...     MASK,  MASK,   v2,  -m1,   m1,   dY,   m1,  -m1,   v2, MASK, MASK,
   ...     MASK,  MASK, MASK,   v1,  -dY,  -dY,  -dY,   v1, MASK, MASK, MASK,
   ...     MASK,  MASK, MASK, MASK,-3*dY,-3*dY,-3*dY, MASK, MASK, MASK, MASK,
   ...     MASK,  MASK, MASK, MASK, MASK, MASK, MASK, MASK, MASK, MASK, MASK), 
   ...     MASK)
   >>> print var.allclose(trialValues)
   1
   
"""
__docformat__ = 'restructuredtext'

if __name__ == '__main__':
    import fipy.tests.doctestPlus
    exec(fipy.tests.doctestPlus._getScript())
    raw_input("finished")
