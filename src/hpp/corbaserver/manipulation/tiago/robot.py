from hpp.corbaserver.manipulation.robot import Robot as _Parent

class Robot (_Parent):
    packageName = "hpp_tiago"
    urdfName = "tiago"
    urdfSuffix = "_airbus"
    srdfSuffix = "_airbus"

    def __init__ (self, compositeName, name, rootjointtype, load = True):
        super(Robot, self).__init__(compositeName, name, rootjointtype, load)
