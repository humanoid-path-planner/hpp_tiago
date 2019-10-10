#!/usr/bin/env python
# Copyright (c) 2018 CNRS
# Author: Florent Lamiraux
#
# This file is part of hpp_tiago.
# hpp_tiago is free software: you can redistribute it
# and/or modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation, either version
# 3 of the License, or (at your option) any later version.
#
# hpp_tiago is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Lesser Public License for more details.  You should have
# received a copy of the GNU Lesser General Public License along with
# hpp_tiago.  If not, see
# <http://www.gnu.org/licenses/>.

from hpp.corbaserver.robot import Robot as _Parent

class TiagoTools(object):
    def _homePosition(self,q=None, prefix=""):
        if q is None:
            q = self.getCurrentConfig()
        from math import pi
        ric = self.rankInConfiguration
        q[ric[prefix + "torso_lift_joint"]] = 0
        q[ric[prefix + "arm_1_joint"]] = 0
        q[ric[prefix + "arm_2_joint"]] = -pi/2+ 1e-4
        q[ric[prefix + "arm_3_joint"]] = -pi/2+ 1e-4
        q[ric[prefix + "arm_4_joint"]] = 2.35619449019
        q[ric[prefix + "arm_5_joint"]] = 0
        q[ric[prefix + "arm_6_joint"]] = 0
        q[ric[prefix + "arm_7_joint"]] = 0
        q[ric[prefix + "head_1_joint" ]] = 0
        q[ric[prefix + "head_2_joint"]] = 0
        return q

    def _foldArm(self,q=None, prefix=""):
        if q is None:
            q = self.getCurrentConfig()
        from math import pi
        ric = self.rankInConfiguration
        q[ric[prefix + "torso_lift_joint"]] = 0.15
        q[ric[prefix + "arm_1_joint"]] = 0.2
        q[ric[prefix + "arm_2_joint"]] = -1.34
        q[ric[prefix + "arm_3_joint"]] = -0.2
        q[ric[prefix + "arm_4_joint"]] = 1.94
        q[ric[prefix + "arm_5_joint"]] = -1.57
        q[ric[prefix + "arm_6_joint"]] = 1.37
        q[ric[prefix + "arm_7_joint"]] = 0
        return q

class Robot (_Parent, TiagoTools):
    packageName = "hpp_tiago"
    urdfName = "tiago"
    urdfSuffix = "_steel"
    srdfSuffix = "_steel"
    rootJointType = "planar"

    def __init__ (self, robotName, load = True):
        super(Robot, self).__init__(robotName = robotName,
                                    rootJointType = self.rootJointType,
                                    load = load)

    def homePosition(self,q=None):
        return self._homePosition (q)

    def foldArm(self,q=None):
        return self._foldArm (q)
