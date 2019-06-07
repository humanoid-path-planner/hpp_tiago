#!/usr/bin/env python
# Copyright (c) 2018 CNRS
# Author: Joseph Mirabel
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

from hpp.corbaserver.manipulation.robot import Robot as _Parent

class Robot (_Parent):
    packageName = "hpp_tiago"
    urdfName = "tiago"
    urdfSuffix = "_steel"
    srdfSuffix = "_steel"

    def __init__ (self, compositeName, name, rootjointtype, load = True):
        super(Robot, self).__init__(compositeName, name, rootjointtype, load)
        self.tiagoName = name

    def homePosition(self,q=None):
        if q is None:
            q = self.getCurrentConfig()
        from math import pi
        q[self.rankInConfiguration[self.tiagoName + "/torso_lift_joint"]] = 0
        q[self.rankInConfiguration[self.tiagoName + "/arm_1_joint"]] = 0
        q[self.rankInConfiguration[self.tiagoName + "/arm_2_joint"]] = -pi/2+\
                                                                       1e-4
        q[self.rankInConfiguration[self.tiagoName + "/arm_3_joint"]] = -pi/2+\
                                                                       1e-4
        q[self.rankInConfiguration[self.tiagoName + "/arm_4_joint"]] = 2.35619449019
        q[self.rankInConfiguration[self.tiagoName + "/arm_5_joint"]] = 0
        q[self.rankInConfiguration[self.tiagoName + "/arm_6_joint"]] = 0
        q[self.rankInConfiguration[self.tiagoName + "/arm_7_joint"]] = 0
        q[self.rankInConfiguration[self.tiagoName + "/head_1_joint" ]] = 0
        q[self.rankInConfiguration[self.tiagoName + "/head_2_joint"]] = 0
        return q
