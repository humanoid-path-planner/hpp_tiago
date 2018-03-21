from hpp.corbaserver.manipulation.robot import Robot as _Parent

class Robot (_Parent):
    packageName = "hpp_tiago"
    urdfName = "tiago"
    urdfSuffix = "_airbus"
    srdfSuffix = "_airbus"

    def __init__ (self, compositeName, name, rootjointtype, load = True):
        super(Robot, self).__init__(compositeName, name, rootjointtype, load)
        self.tiagoName = name

    def homePosition(self,q=None):
        if q is None:
            q = self.getCurrentConfig()
        from math import pi
        q[self.rankInConfiguration[self.tiagoName + "/torso_lift_joint"]] = 0
        q[self.rankInConfiguration[self.tiagoName + "/arm_1_joint"]] = 0
        q[self.rankInConfiguration[self.tiagoName + "/arm_2_joint"]] = - pi / 2
        q[self.rankInConfiguration[self.tiagoName + "/arm_3_joint"]] = - pi / 2
        q[self.rankInConfiguration[self.tiagoName + "/arm_4_joint"]] = 2.35619449019
        q[self.rankInConfiguration[self.tiagoName + "/arm_5_joint"]] = 0
        q[self.rankInConfiguration[self.tiagoName + "/arm_6_joint"]] = 0
        q[self.rankInConfiguration[self.tiagoName + "/arm_7_joint"]] = 0
        q[self.rankInConfiguration[self.tiagoName + "/head_1_joint" ]] = 0
        q[self.rankInConfiguration[self.tiagoName + "/head_2_joint"]] = 0
        return q
