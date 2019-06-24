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
from hpp.corbaserver.tiago.robot import TiagoTools

class Robot (_Parent, TiagoTools):
    packageName = "hpp_tiago"
    urdfName = "tiago"
    urdfSuffix = "_steel"
    srdfSuffix = "_steel"

    def __init__ (self, compositeName, name, rootJointType, load = True, **kwargs):
        super(Robot, self).__init__(compositeName, name, rootJointType, load, **kwargs)
        self.tiagoName = name

    def homePosition(self,q=None):
        return self._homePosition (q, prefix=self.tiagoName+"/")

    def foldArm(self,q=None):
        return self._foldArm (q, prefix=self.tiagoName+"/")
