#!/usr/bin/env python

## 
 # ###################################################################
 #  FiPy - Python-based finite volume PDE solver
 # 
 #  FILE: "input.py"
 #                                    created: 12/29/03 {3:23:47 PM}
 #                                last update: 4/5/05 {5:55:02 PM} 
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

This input file again solves a 1D diffusion problem as in
``examples/diffusion/steadyState/mesh1D/input.py``,     
the difference being that this transient example is solved explicitly.

We create a 1D mesh:
    
    >>> nx = 100
    >>> dx = 1.
    >>> from fipy.meshes.grid1D import Grid1D
    >>> mesh = Grid1D(dx = dx, nx = nx)

and we initialize a `CellVariable` to `initialValue`:
    
    >>> valueLeft = 0.
    >>> initialValue = 1.
    >>> from fipy.variables.cellVariable import CellVariable
    >>> var = CellVariable(
    ...     name = "concentration",
    ...     mesh = mesh,
    ...     value = initialValue)

The transient diffusion equation 

.. raw:: latex

   $$ \frac{\partial \phi}{\partial t} = \nabla \cdot (D \nabla \phi) $$

is represented by a `TransientTerm` and an `ExplicitDiffusionTerm`.

We take the diffusion coefficient 

.. raw:: latex

   $D = 1$
   
..

   >>> diffusionCoeff = 1.
    
We build the equation:

    >>> from fipy.terms.explicitDiffusionTerm import ExplicitDiffusionTerm
    >>> from fipy.terms.transientTerm import TransientTerm
    >>> eq = TransientTerm() == ExplicitDiffusionTerm(coeff = diffusionCoeff)
    
and the boundary conditions:
    
    >>> from fipy.boundaryConditions.fixedValue import FixedValue
    >>> boundaryConditions=(FixedValue(mesh.getFacesLeft(),valueLeft),)

In this case, many steps have to be taken to reach equilibrium.  A loop is
required to execute the necessary time steps:
    
    >>> timeStepDuration = 0.1
    >>> steps = 100
    >>> for step in range(steps):
    ...     var.updateOld()     
    ...     eq.solve(var = var, boundaryConditions = boundaryConditions,
    ...                         dt = timeStepDuration)

The analytical solution for this transient diffusion problem is given
by

.. raw:: latex

   $\phi = \erf(x/2\sqrt{D t})$.
   
The result is tested against the expected profile:
    
    >>> Lx = nx * dx
    >>> x = mesh.getCellCenters()[:,0]
    >>> t = timeStepDuration * steps
    >>> from fipy.tools import numerix
    >>> epsi = x / numerix.sqrt(t * diffusionCoeff)
    >>> from scipy.special import erf
    >>> analyticalArray = erf(epsi/2)
    >>> print var.allclose(analyticalArray, atol = 2e-3)
    1
    
If the problem is run interactively, we can view the result:
    
    >>> if __name__ == '__main__':
    ...     import fipy.viewers
    ...     viewer = fipy.viewers.make(vars = (var,))
    ...     viewer.plot()
"""
 
__docformat__ = 'restructuredtext'

if __name__ == '__main__':
    import fipy.tests.doctestPlus
    exec(fipy.tests.doctestPlus._getScript())
    raw_input('finished')