#!/usr/bin/env python

## 
 # ###################################################################
 #  FiPy - Python-based finite volume PDE solver
 # 
 #  FILE: "inputLeveler.py"
 #                                    created: 8/26/04 {10:29:10 AM} 
 #                                last update: 5/15/06 {2:45:49 PM} { 1:23:41 PM}
 #  Author: Jonathan Guyer
 #  E-mail: guyer@nist.gov
 #  Author: Daniel Wheeler
 #  E-mail: daniel.wheeler@nist.gov
 #    mail: NIST
 #     www: http://ctcms.nist.gov
 #  
 # ========================================================================
 # This software was developed at the National Institute of Standards
 # and Technology by employees of the Federal Government in the course
 # of their official duties.  Pursuant to title 17 Section 105 of the
 # United States Code this software is not subject to copyright
 # protection and is in the public domain.  PFM is an experimental
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
This input file

.. raw:: latex

    \label{inputLeveler} is a demonstration of the use of \FiPy{} for
    modeling copper superfill with leveler and accelerator
    additives. The material properties and experimental parameters
    used are roughly those that have been previously
    published~\cite{NIST:leveler:2005}.

To run this example from the base fipy directory type::
    
    $ examples/levelSet/electroChem/inputLeveler.py

at the command line. The results of the simulation will be displayed
and the word `finished` in the terminal at the end of the
simulation. The simulation will only run for 200 time steps. In order
to alter the number of timesteps, the python function that
encapsulates the system of equations must first be imported (at the
python command line),

.. raw:: latex

   \IndexFunction{runLeveler}

..

    >>> from examples.levelSet.electroChem.inputLeveler import runLeveler

and then the function can be executed with a different number of time
steps by changing the `numberOfSteps` argument as follows,

    >>> runLeveler(numberOfSteps=10, displayViewers=False, cellSize=0.25e-7)
    1

Change the `displayViewers` argument to `True` if you wish to see the
results displayed on the screen. This example requires `gmsh` to
construct the mesh.

.. raw:: latex

    \IndexSoftware{gmsh}
    
    This example models the case when suppressor, accelerator and leveler
    additives are present in the electrolyte. The suppressor is
    assumed to absorb quickly compared with the other additives. Any
    unoccupied surface sites are immediately covered with
    suppressor. The accelerator additive has more surface affinity
    than suppressor and is thus preferential adsorbed. The accelerator
    can also remove suppressor when the surface reaches full
    coverage. Similarly, the leveler additive has more surface
    affinity than both the suppressor and accelerator. This forms a
    simple set of assumptions for understanding the behavior of these
    additives.

    The following is a complete description of the equations for the
    model described here. Any equations that have been omitted are the
    same as those given in Example~\ref{inputSimpleTrench}. The
    current density is governed by $$ i = \frac{ c_m }{ c_m^\infty }
    \sum_{ j } \left[ i_j \theta_j \left( \exp{ \frac{-\alpha_j F \eta
    }{ R T }} - \exp{ \frac{ \left( 1 - \alpha_j \right) F \eta}{ R T
    }} \right) \right] $$ where $j$ represents $S$ for suppressor, $A$
    for accelerator, $L$ for leveler and $V$ for vacant. This model
    assumes a linear interpolation between the three cases of complete
    coverage for each additive or vacant substrate. The governing
    equations for the surfactants are given by, $$ \dot{\theta_{L}} =
    \kappa v \theta_L + k_l^+ c_L \left( 1 - \theta_L \right) - k_L^-
    v \theta_L, $$ $$ \dot{\theta_{a}} = \kappa v \theta_A + k_A^+ c_A
    \left( 1 - \theta_A - \theta_L \right) - k_L c_L \theta_A - k_A^-
    \theta_A^{q - 1}, $$ $$ \theta_S = 1 - \theta_A - \theta_L $$ and
    $$ \theta_V = 0. $$ It has been found experimentally that $i_L =
    i_S$.

    If the surface reaches full coverage, the equations do not
    naturally prevent the coverage rising above full coverage due to
    the curvature terms. Thus, when $\theta_L + \theta_A = 1$ then the
    equation for accelerator becomes $\dot{ \theta_A } = -\dot{
    \theta_L }$ and when $\theta_L = 1$, the equation for leveler
    becomes $\dot{\theta_{L}} = - k_L^- v \theta_L.$

    The parameters $k_A^+,$ $k_A^-$ and $q$ are both functions of $\eta$
    given by, $$ k_A^+ = k_{A0}^+ \exp{\frac{-\alpha_k F \eta}{R T}}, $$
    and $$ k_A^- = B_d + \frac{A}{\exp{\left(B_a \left(\eta + V_d
    \right) \right)}} + \exp{\left(B_b \left(\eta + V_d \right)
    \right)} $$ and $$ q = m * \eta + b. $$

The following table shows the symbols used in the governing equations
and their corresponding arguments for the `runLeveler` function.

.. raw:: latex

    \begin{tabular}{|rllr@{.}ll|}
    \hline
    Symbol                & Description                       & Keyword Argument                      & \multicolumn{2}{l}{Value} & Unit                               \\
    \hline
    \multicolumn{6}{|c|}{Deposition Rate Parameters}                                                                                                                   \\
    \hline
    $v$                   & deposition rate                   &                                       & \multicolumn{2}{l}{}      & m s$^{-1}$                         \\
    $i_A$                 & accelerator current density       & \verb+i0Accelerator+                  & \multicolumn{2}{l}{}      & A m$^{-2}$                         \\
    $i_L$                 & leveler current density           & \verb+i0Leveler+                      & \multicolumn{2}{l}{}      & A m$^{-2}$                         \\
    $\Omega$              & molar volume                      & \verb+molarVolume+                    & 7&1$\times$10$^{-6}$      & m$^3$ mol$^{-1}$                   \\
    $n$                   & ion charge                        & \verb+charge+                         & \multicolumn{2}{c}{2}     &                                    \\
    $F$                   & Faraday's constant                & \verb+faradaysConstant+               & 9&6$\times$10$^{-4}$      & C mol$^{-1}$                       \\
    $i_0$                 & exchange current density          &                                       & \multicolumn{2}{l}{}      & A m$^{-2}$                         \\
    $\alpha_A$            & accelerator transfer coefficient  & \verb+alphaAccelerator+               & 0&4                       &                                    \\
    $\alpha_S$            & leveler transfer coefficient      & \verb+alphaLeveler+                   & 0&5                       &                                    \\
    $\eta$                & overpotential                     & \verb+overpotential+                  & -0&3                      & V                                  \\
    $R$                   & gas constant                      & \verb+gasConstant+                    & 8&314                     & J K mol$^{-1}$                     \\
    $T$                   & temperature                       & \verb+temperature+                    & 298&0                     & K                                  \\
    \hline
    \multicolumn{6}{|c|}{Ion Parameters}                                                                                                                               \\
    \hline
    $c_I$                 & ion concentration                 & \verb+ionConcentration+               & 250&0                     & mol m$^{-3}$                       \\
    $c_I^{\infty}$        & far field ion concentration       & \verb+ionConcentration+               & 250&0                     & mol m$^{-3}$                       \\
    $D_I$                 & ion diffusion coefficient         & \verb+ionDiffusion+                   & 5&6$\times$10$^{-10}$     & m$^2$ s$^{-1}$                     \\
    \hline
    \multicolumn{6}{|c|}{Accelerator Parameters}                                                                                                                       \\
    \hline
    $\theta_A$            & accelerator coverage              & \verb+acceleratorCoverage+            & 0&0                       &                                    \\
    $c_A$                 & accelerator concentartion         & \verb+acceleratorConcentration+       & 5&0$\times$10$^{-3}$      & mol m$^{-3}$                       \\
    $c_A^{\infty}$        & far field accelerator concentration & \verb+acceleratorConcentration+     & 5&0$\times$10$^{-3}$      & mol m$^{-3}$                       \\
    $D_A$                 & catalyst diffusion coefficient    & \verb+catalystDiffusion+              & 1&0$\times$10$^{-9}$      & m$^2$ s$^{-1}$                     \\
    $\Gamma_A$            & accelerator site density          & \verb+siteDensity+                    & 9&8$\times$10$^{-6}$      & mol m$^{-2}$                       \\
    $k_A^+$               & accelerator adsorption            &                                       & \multicolumn{2}{l}{}      & m$^3$ mol$^{-1}$ s$^{-1}$          \\
    $k_{A0}^+$            & accelerator adsorption coeff      & \verb+kAccelerator0+                  & 2&6$times$10$^{-4}$       & m$^3$ mol$^{-1}$ s$^{-1}$          \\
    $\alpha_k$            & accelerator adsorption coeff      & \verb+alphaAdsorption+                & 0&62                      &                                    \\
    $k_A^-$               & accelerator consumption coeff     &                                       & \multicolumn{2}{l}{}      &                                    \\
    $B_a$                 & experimental parameter            & \verb+Bd+                             & -40&0                     &
                                \\
    $B_b$                 & experimental parameter            & \verb+Bd+                             & 60&0                      &
                                \\
    $V_d$                 & experimental parameter            & \verb+Bd+                             & 9&8$\times$10$^{-2}$      &
                                \\
    $B_d$                 & experimental parameter            & \verb+Bd+                             & 8&0$\times$10$^{-4}$      &
                                \\
    \hline
    \multicolumn{6}{|c|}{Geometry Parameters}                                                                                                                          \\
    \hline
    $D$                   & trench depth                      & \verb+trenchDepth+                    & 0&5$\times$10$^{-6}$      & m                                  \\
    $D / W$               & trench aspect ratio               & \verb+aspectRatio+                    & 2&0                       &                                    \\
    $S$                   & trench spacing                    & \verb+trenchSpacing+                  & 0&6$\times$10$^{-6}$      & m                                  \\
    $\delta$              & boundary layer depth              & \verb+boundaryLayerDepth+             & 0&3$\times$10$^{-6}$      & m                                  \\
    \hline
    \multicolumn{6}{|c|}{Simulation Control Parameters}                                                                                                                \\
    \hline
                          & computational cell size           & \verb+cellSize+                       & 0&1$\times$10$^{-7}$      & m                                  \\
                          & number of time steps              & \verb+numberOfSteps+                  & \multicolumn{2}{c}{5}     &                                    \\
                          & whether to display the viewers    & \verb+displayViewers+                 & \multicolumn{2}{c}{\texttt{True}} &                           \\
    \hline
    \end{tabular}

The following images show accelerator and leveler contour plots that
can be obtained by running this example.

.. image:: examples/levelSet/electroChem/accelerator.pdf
   :scale: 60
   :align: center
   :alt: resulting image

.. image:: examples/levelSet/electroChem/leveler.pdf
   :scale: 60
   :align: center
   :alt: resulting image
    
"""
__docformat__ = 'restructuredtext'

def runLeveler(kLeveler=0.018, bulkLevelerConcentration=0.02, cellSize=0.1e-7, rateConstant=0.00026, initialAcceleratorCoverage=0.0, levelerDiffusionCoefficient=5e-10, numberOfSteps=400, displayRate=10, displayViewers=True):

    
    kLevelerConsumption = 0.0005
    aspectRatio = 1.5
    faradaysConstant = 9.6485e4
    gasConstant = 8.314
    acceleratorDiffusionCoefficient = 4e-10
    siteDensity = 6.35e-6
    atomicVolume = 7.1e-6
    charge = 2
    metalDiffusionCoefficient = 4e-10
    temperature = 298.
    overpotential = -0.25
    bulkMetalConcentration = 250.
    bulkAcceleratorConcentration = 50.0e-3
    initialLevelerCoverage = 0.
    cflNumber = 0.2
    numberOfCellsInNarrowBand = 20
    cellsBelowTrench = 10
    trenchDepth = 0.4e-6
    trenchSpacing = 0.6e-6
    boundaryLayerDepth = 98.7e-6
    i0Suppressor = 0.3
    i0Accelerator = 22.5
    alphaSuppressor = 0.5
    alphaAccelerator = 0.4
    alphaAdsorption = 0.62
    m = 4
    b = 2.65
    A = 0.3
    Ba = -40
    Bb = 60
    Vd = 0.098
    Bd = 0.0008

    etaPrime = faradaysConstant * overpotential / gasConstant / temperature

    from fipy import TrenchMesh
    from fipy.tools import numerix
    mesh = TrenchMesh(cellSize = cellSize,
                      trenchSpacing = trenchSpacing,
                      trenchDepth = trenchDepth,
                      boundaryLayerDepth = boundaryLayerDepth,
                      aspectRatio = aspectRatio,
                      angle = numerix.pi * 4. / 180.,
                      bowWidth = 0.,
                      overBumpRadius = 0.,
                      overBumpWidth = 0.)

    narrowBandWidth = numberOfCellsInNarrowBand * cellSize
    from fipy.models.levelSet.distanceFunction.distanceVariable import DistanceVariable
    distanceVar = DistanceVariable(
        name = 'distance variable',
        mesh = mesh,
        value = -1,
        narrowBandWidth = narrowBandWidth)

    distanceVar.setValue(1, where=mesh.getElectrolyteMask())
    
    distanceVar.calcDistanceFunction(narrowBandWidth = 1e10)
    from fipy.models.levelSet.surfactant.surfactantVariable import SurfactantVariable
    levelerVar = SurfactantVariable(
        name = "leveler variable",
        value = initialLevelerCoverage,
        distanceVar = distanceVar)

    acceleratorVar = SurfactantVariable(
        name = "accelerator variable",
        value = initialAcceleratorCoverage,
        distanceVar = distanceVar)

    from fipy.variables.cellVariable import CellVariable
    bulkAcceleratorVar = CellVariable(name = 'bulk accelerator variable',
                                      mesh = mesh,
                                      value = bulkAcceleratorConcentration)

    bulkLevelerVar = CellVariable(
        name = 'bulk leveler variable',
        mesh = mesh,
        value = bulkLevelerConcentration)

    metalVar = CellVariable(
        name = 'metal variable',
        mesh = mesh,
        value = bulkMetalConcentration)

    def depositionCoeff(alpha, i0):
        expo = numerix.exp(-alpha * etaPrime)
        return 2 * i0 * (expo - expo * numerix.exp(etaPrime))

    coeffSuppressor = depositionCoeff(alphaSuppressor, i0Suppressor)
    coeffAccelerator = depositionCoeff(alphaAccelerator, i0Accelerator)

    exchangeCurrentDensity = acceleratorVar.getInterfaceVar() * (coeffAccelerator - coeffSuppressor) + coeffSuppressor

    currentDensity = metalVar / bulkMetalConcentration * exchangeCurrentDensity

    depositionRateVariable = currentDensity * atomicVolume / charge / faradaysConstant

    extensionVelocityVariable = CellVariable(
        name = 'extension velocity',
        mesh = mesh,
        value = depositionRateVariable)   

    from fipy.models.levelSet.surfactant.adsorbingSurfactantEquation \
             import AdsorbingSurfactantEquation

    kAccelerator = rateConstant * numerix.exp(-alphaAdsorption * etaPrime)
    kAcceleratorConsumption =  Bd + A / (numerix.exp(Ba * (overpotential + Vd)) + numerix.exp(Bb * (overpotential + Vd)))
    q = m * overpotential + b

    levelerSurfactantEquation = AdsorbingSurfactantEquation(
        levelerVar,
        distanceVar = distanceVar,
        bulkVar = bulkLevelerVar,
        rateConstant = kLeveler,
        consumptionCoeff = kLevelerConsumption * depositionRateVariable)

    accVar1 = acceleratorVar.getInterfaceVar()
    accVar2 = (accVar1 > 0) * accVar1
    accConsumptionCoeff = kAcceleratorConsumption * (accVar2**(q - 1))

    acceleratorSurfactantEquation = AdsorbingSurfactantEquation(
        acceleratorVar,
        distanceVar = distanceVar,
        bulkVar = bulkAcceleratorVar,
        rateConstant = kAccelerator,
        otherVar = levelerVar,
        otherBulkVar = bulkLevelerVar,
        otherRateConstant = kLeveler,
        consumptionCoeff = accConsumptionCoeff)

    from fipy.models.levelSet.advection.higherOrderAdvectionEquation \
         import buildHigherOrderAdvectionEquation

    advectionEquation = buildHigherOrderAdvectionEquation(
        advectionCoeff = extensionVelocityVariable)

    from fipy.boundaryConditions.fixedValue import FixedValue
    from fipy.models.levelSet.electroChem.metalIonDiffusionEquation \
         import buildMetalIonDiffusionEquation

    metalEquation = buildMetalIonDiffusionEquation(
        ionVar = metalVar,
        distanceVar = distanceVar,
        depositionRate = depositionRateVariable,
        diffusionCoeff = metalDiffusionCoefficient,
        metalIonMolarVolume = atomicVolume)

    metalEquationBCs = FixedValue(mesh.getTopFaces(), bulkMetalConcentration)

    from fipy.models.levelSet.surfactant.surfactantBulkDiffusionEquation \
         import buildSurfactantBulkDiffusionEquation

    bulkAcceleratorEquation = buildSurfactantBulkDiffusionEquation(
        bulkVar = bulkAcceleratorVar,
        distanceVar = distanceVar,
        surfactantVar = acceleratorVar,
        otherSurfactantVar = levelerVar,
        diffusionCoeff = acceleratorDiffusionCoefficient,
        rateConstant = kAccelerator * siteDensity)

    bulkAcceleratorEquationBCs = (FixedValue(
        mesh.getTopFaces(),
        bulkAcceleratorConcentration),)

    bulkLevelerEquation = buildSurfactantBulkDiffusionEquation(
        bulkVar = bulkLevelerVar,
        distanceVar = distanceVar,
        surfactantVar = levelerVar,
        diffusionCoeff = levelerDiffusionCoefficient,
        rateConstant = kLeveler * siteDensity)

    bulkLevelerEquationBCs =  (FixedValue(
        mesh.getTopFaces(),
        bulkLevelerConcentration),)

    eqnTuple = ( (advectionEquation, distanceVar, ()),
                 (levelerSurfactantEquation, levelerVar, ()),
                 (acceleratorSurfactantEquation, acceleratorVar, ()),
                 (metalEquation, metalVar,  metalEquationBCs),
                 (bulkAcceleratorEquation, bulkAcceleratorVar, bulkAcceleratorEquationBCs),
                 (bulkLevelerEquation, bulkLevelerVar, bulkLevelerEquationBCs))

    levelSetUpdateFrequency = int(0.7 * narrowBandWidth / cellSize / cflNumber / 2)

    totalTime = 0.0

    if displayViewers:
        from fipy.viewers.mayaviViewer.mayaviSurfactantViewer import MayaviSurfactantViewer
        viewers = (
            MayaviSurfactantViewer(distanceVar, acceleratorVar.getInterfaceVar(), zoomFactor = 1e6, limits = { 'datamax' : 0.5, 'datamin' : 0.0 }, smooth = 1, title = 'accelerator coverage'),
            MayaviSurfactantViewer(distanceVar, levelerVar.getInterfaceVar(), zoomFactor = 1e6, limits = { 'datamax' : 0.5, 'datamin' : 0.0 }, smooth = 1, title = 'leveler coverage'))
        
    for step in range(numberOfSteps):

        if displayViewers:
            if step % displayRate == 0:
                for viewer in viewers:
                    viewer.plot()
            
        if step % levelSetUpdateFrequency == 0:
            distanceVar.calcDistanceFunction(deleteIslands = True)

        extensionVelocityVariable.setValue(depositionRateVariable)

        extOnInt = numerix.where(distanceVar > 0,
                                 numerix.where(distanceVar < 2 * cellSize,
                                               extensionVelocityVariable,
                                               0),
                                 0)

        dt = cflNumber * cellSize / numerix.max(extOnInt)

        id = numerix.max(numerix.nonzero(distanceVar._getInterfaceFlag()))
        distanceVar.extendVariable(extensionVelocityVariable, deleteIslands = True)

        extensionVelocityVariable[mesh.getFineMesh().getNumberOfCells():] = 0.

        for eqn, var, BCs in eqnTuple:
            var.updateOld()

        for eqn, var, BCs in eqnTuple:
            eqn.solve(var, boundaryConditions = BCs, dt = dt)
            
        totalTime += dt

    try:
        testFile = 'testLeveler.gz'
        import os
        import examples.levelSet.electroChem
        from fipy.tools import dump
        data = dump.read(os.path.join(examples.levelSet.electroChem.__path__[0], testFile))
        N = mesh.getFineMesh().getNumberOfCells()
        print numerix.allclose(data[:N], levelerVar[:N], rtol = 1e-3)
    except:
        return 0
    
if __name__ == '__main__':
    runLeveler()
    raw_input("finished")    
