import numpy
from numpy.linalg import norm
from math import sqrt
from hpp.corbaserver.manipulation import Client, ConstraintGraph, \
  ProblemSolver, Constraints
from hpp.corbaserver.manipulation.tiago import Robot
from hpp.gepetto.manipulation import ViewerFactory
from hpp.corbaserver import loadServerPlugin
loadServerPlugin ("corbaserver", "manipulation-corba.so")
Client ().problem.resetProblem ()

#
#  Initialize robot, object and environment
#

# Information to load the environment
class Environment (object):
  packageName = 'gerard_bauzil'
  urdfName = 'staircases_koroibot'
  urdfSuffix = ""
  srdfSuffix = ""

# Information to load the object
class WoodBox (object) :
    rootJointType = "freeflyer"
    packageName = "gerard_bauzil"
    urdfName = "plank_of_wood1"
    urdfSuffix = ""
    srdfSuffix = ""

s = sqrt (2) / 2

# Load Tiago robot, define mobility of base as "planar"
robot = Robot ('tiago', 'tiago', 'planar')
# Create client to HPP CORBA server
ps = ProblemSolver (robot)
# Create client to HPP and gepetto-gui CORBA servers
vf = ViewerFactory (ps)

q_foldedArm = [0.0, 0.0, 1.0, 0.0, # base
     0.15, # trunk
     0.20, -1.34, -0.20, 1.94, -1.57, 1.37, 0.0, # arm
     0.05, # gripper
     0.0, 0.0, # head
     0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0 # box
]
# load model of environment
vf.loadEnvironmentModel (Environment, 'staircases_koroibot')

# Set bounds of mobile base
robot.setJointBounds ('tiago/root_joint',
                      [-3.0, 4.0, -1.5, 3.0, -1.01, 1.01, -1.01, 1.01])
# Modify upper bound of gripper
robot.setJointBounds ('tiago/gripper_finger_joint', [0.002, 0.050])

# Load piece of wood
vf.loadObjectModel (WoodBox, "box")

# Set bounds of box
robot.setJointBounds ('box/root_joint', [-4.5, 5.5, -3.0, 4.5, 0.0, 2.5,
                                         -1.01, 1.01, -1.01, 1.01, -1.01, 1.01,
                                         -1.01, 1.01])

# Initial configuration
q_init = q_foldedArm [::]
q_init [1] = -.5

#
#  Create locked joint and pre-grasp constraints
#

# Select line search algorithm for non-linear problem solving
ps.setDefaultLineSearchType ('Backtracking')
# Create constraint graph with one node and no edge
cg = ConstraintGraph (robot, 'graph')
cg.createNode (['free'])
cg.initialize ()
# Create pre-grasp constraint as a numerical constraint
cg.createPreGrasp ('pg', 'tiago/gripper', 'box/handle1')
# create placement constraint as a numerical constraint
ps.createPlacementConstraints ('box-on-small-platform',
                               ['box/front_surface',],
                               ['staircases_koroibot/small-platform',])

# Create lockedJoint for robot base
ps.createLockedJoint ('locked-tiago/root_joint', 'tiago/root_joint',
                      [0,0,1,0,])
# Right hand side is parameterizable
ps.setConstantRightHandSide ('locked-tiago/root_joint', False)

# Create locked joint constraints for head
lockedHead = list ()
rank = robot.rankInConfiguration ['tiago/head_1_joint']
for i in range (2):
  jointName = 'tiago/head_{0}_joint'.format (i+1)
  lockedJointName = 'locked-tiago/head_{0}_joint'.format (i+1)
  ps.createLockedJoint (lockedJointName, jointName,
                        q_foldedArm [rank+i:rank+i+1])
  lockedHead.append (lockedJointName)

# Create locked joint constraints for torso
rank = robot.rankInConfiguration ['tiago/torso_lift_joint']
ps.createLockedJoint ('locked-torso', 'tiago/torso_lift_joint',
                      q_foldedArm [rank: rank+1])

# Create locked joint constraints for gripper
grId = robot.rankInConfiguration ['tiago/gripper_finger_joint']
ps.createLockedJoint ('locked-gripper', 'tiago/gripper_finger_joint',
                      q_foldedArm [grId:grId+1])

# Create locked joint constraints for arm
lockedArm = list ()
rank = robot.rankInConfiguration ['tiago/arm_1_joint']
for i in range (7):
  jointName = 'tiago/arm_{0}_joint'.format (i+1)
  lockedJointName = 'locked-tiago/arm_{0}_joint'.format (i+1)
  ps.createLockedJoint (lockedJointName, jointName,
                        q_foldedArm [rank+i:rank+i+1])
  lockedArm.append (lockedJointName)

# Generate configuration where the box is on the small platform
ps.resetConstraints ()
ps.addNumericalConstraints ('solver', ['box-on-small-platform',])
res, q1, err = ps.applyConstraints (q_init)
boxId = robot.rankInConfiguration ['box/root_joint']
if res:
  q1 [boxId:boxId+2] = [-1.30, 0.50,]  # horizontal position
  q1 [boxId+3: boxId+7] = [0, s, 0, s] # vertical position
q_init = q1 [::]

# Generate configurations where the robot grasps the box
ps.createLockedJoint ('locked-box', 'box/root_joint', q1 [boxId: boxId+7])

ps.resetConstraints ()
ps.addLockedJointConstraints ('solver', ['locked-box', 'locked-gripper'] +\
                              lockedHead)
ps.addNumericalConstraints ('solver', ['pg',])
grasp_placement = list ()
for i in range (100):
  q = robot.shootRandomConfig ()
  res, q2, err = ps.applyConstraints (q)
  if not res: continue
  res, msg = robot.isConfigValid (q2)
  if res: grasp_placement.append (q2)

#
#  Plan path for the base to a position where to grasp
#

# Lock torso, head, arm and gripper
ps.resetConstraints ()
ps.addLockedJointConstraints ('solver', ['locked-box', 'locked-gripper',
                                         'locked-torso'] + lockedHead + \
                              lockedArm)
# Remove useless collision pairs.
ps.filterCollisionPairs ()
goalConfigs = list ()
for q in grasp_placement:
  res, q3, err = ps.applyConstraints (q)
  if not res: raise RuntimeError ('Failed to apply constraints')
  res, msg = robot.isConfigValid (q3)
  if res:
    goalConfigs.append (q3)
  else:
    goalConfigs.append (None)

# Select steering method for non-holonomic base
ps.selectSteeringMethod ('ReedsShepp')
# Select path planning algorithms
ps.selectPathPlanner ('kPRM*')
ps.setParameter ('kPRM*/numberOfNodes', 80)
# Set initial configuration
ps.setInitialConfig (q_init)
# Set goal configurations
ps.resetGoalConfigs ()
for q in goalConfigs:
  if not q is None:
    ps.addGoalConfig (q)
# Solve
ps.solve ()

#
#  Plan a path to pre-grasp position
#

# Define q_init as end of navigation path
navPid = ps.numberPaths () - 1
l = ps.pathLength (navPid)
q_init = ps.configAtParam (navPid, l)
# Search which goal configuration has been reached by navigation path
for q, i in zip (goalConfigs, xrange (10000)):
  if q and norm (numpy.array (q) - numpy.array (q_init)) < 1e-6:
    break
if i == len (goalConfigs): raise RuntimeError \
   ("failed to retrieve goal configuration")
# Define goal configuration as pre-grasp configuration with the same base
# placement
q_goal = grasp_placement [i]

# Set fixed base constraint and object position
ps.resetConstraints ()
ps.addLockedJointConstraints ('solver', ['locked-tiago/root_joint',
                                         'locked-box',])
# Set parameter value for fixed base constraint
ps.setRightHandSideFromConfig (q_init)

# Reset planner
ps.clearRoadmap ()
ps.resetGoalConfigs ()
ps.setInitialConfig (q_init)
ps.addGoalConfig (q_goal)
ps.solve ()
graspPid = ps.numberPaths () - 1
# Concatenate navigation and grasp paths.
ps.concatenatePath (navPid, graspPid)

# After starting gepetto-gui, create a client to display paths
# v = vf.createViewer ()
