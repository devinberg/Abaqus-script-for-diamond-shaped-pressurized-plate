# -*- coding: mbcs -*-
from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from optimization import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *

import math
#import time
# SET VARIABLES
EdgeLengths = [0.25,0.5,0.75,1.0,1.25,1.5]
BraidAngles = [5,15,25,35,45,55]
Thicknesses = [0.05,0.1,0.15,0.2,0.25]
Pressures = [0.2,0.4,0.6,0.8,1.0]    # Units are MPa
E = 6.5
nu = 0.5

i=1
for EdgeLength in EdgeLengths:
    for BraidAngle in BraidAngles:
        for Thickness in Thicknesses:
            for Pressure in Pressures:
                x = EdgeLength*math.cos(BraidAngle*math.pi/180)
                y = EdgeLength*math.sin(BraidAngle*math.pi/180)
                xmidpoint = EdgeLength/2*math.cos(BraidAngle*math.pi/180)
                ymidpoint = EdgeLength/2*math.sin(BraidAngle*math.pi/180)

                # CREATE THE MODEL AND DEFINE EDGE LENGTH, BRAID ANGLE, AND THICKNESS
                mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=5.0)
                mdb.models['Model-1'].sketches['__profile__'].Line(point1=(-x, 0), point2=(
                    0, y))
                mdb.models['Model-1'].sketches['__profile__'].Line(point1=(0, y), point2=(
                    x, 0))
                mdb.models['Model-1'].sketches['__profile__'].Line(point1=(x, 0), point2=(
                    0, -y))
                mdb.models['Model-1'].sketches['__profile__'].Line(point1=(0, -y), point2=(
                    -x, 0))
                mdb.models['Model-1'].Part(dimensionality=THREE_D, name='Part-1', type=
                    DEFORMABLE_BODY)
                mdb.models['Model-1'].parts['Part-1'].BaseSolidExtrude(depth=Thickness, sketch=
                    mdb.models['Model-1'].sketches['__profile__'])
                del mdb.models['Model-1'].sketches['__profile__']

                # SPECIFY THE ELASTIC MATERIAL PROPERTIES
                mdb.models['Model-1'].Material(name='Material-1')
                mdb.models['Model-1'].materials['Material-1'].Elastic(table=((E, nu), ))

                # SECTION AND ASSIGN TO PART
                mdb.models['Model-1'].HomogeneousSolidSection(material='Material-1', name=
                    'Section-1', thickness=None)
                mdb.models['Model-1'].parts['Part-1'].SectionAssignment(offset=0.0, 
                    offsetField='', offsetType=MIDDLE_SURFACE, region=Region(
                    cells=mdb.models['Model-1'].parts['Part-1'].cells.findAt(((0.0, 
                    0.0, 0.0), ), )), sectionName='Section-1', thicknessAssignment=
                    FROM_SECTION)

                # CREATE INSTANCE AND STATIC STEP
                mdb.models['Model-1'].rootAssembly.DatumCsysByDefault(CARTESIAN)
                mdb.models['Model-1'].rootAssembly.Instance(dependent=OFF, name='Part-1-1', 
                    part=mdb.models['Model-1'].parts['Part-1'])
                mdb.models['Model-1'].StaticStep(name='Step-1', previous='Initial')

                # SET THE PRESSURE LOAD AND BOUNDARY CONDITIONS
                mdb.models['Model-1'].Pressure(amplitude=UNSET, createStepName='Step-1', 
                    distributionType=UNIFORM, field='', magnitude=Pressure, name='Load-1', region=
                    Region(
                    side1Faces=mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].faces.findAt(
                    ((0.0, 0.0, 0.0), ), )))
                mdb.models['Model-1'].PinnedBC(createStepName='Step-1', localCsys=None, name=
                    'BC-1', region=Region(
                    faces=mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].faces.findAt(
                    ((-xmidpoint, ymidpoint, Thickness/2), ), ((xmidpoint, ymidpoint, Thickness/2), ), ((
                    xmidpoint, -ymidpoint, Thickness/2), ), ((-xmidpoint, -ymidpoint, Thickness/2), ), 
                    )))

                # SEED THE INSTANCE AND MESH IT (MIGHT CHANGE MESH SIZE HERE)
                mdb.models['Model-1'].rootAssembly.seedPartInstance(deviationFactor=0.1, 
                    regions=(mdb.models['Model-1'].rootAssembly.instances['Part-1-1'], ), size=
                    0.05)
                mdb.models['Model-1'].rootAssembly.generateMesh(regions=(
                    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'], ))

                # CREATE THE JOB AND SUBMIT
                jobname = 'Job-%s' %i
                mdb.Job(atTime=None, contactPrint=OFF, description='', echoPrint=OFF, 
                    explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF, 
                    memory=90, memoryUnits=PERCENTAGE, model='Model-1', modelPrint=OFF, 
                    multiprocessingMode=DEFAULT, name=jobname, nodalOutputPrecision=SINGLE, 
                    numCpus=1, queue=None, scratch='', type=ANALYSIS, userSubroutine='', 
                    waitHours=0, waitMinutes=0)
                mdb.jobs[jobname].submit(consistencyChecking=OFF)
                #time.sleep(30)
                i=i+1
# END OF FOR LOOPS
