import VRScript
import lel_common


class Door(lel_common.GenericObject):
	def __init__(self, sName, sMeshName, position, bVis, bPhysics, physicsShape, interact, physicsType):
		lel_common.GenericObject.__init__(self, sName, sMeshName, position, bVis, bPhysics, physicsShape, interact, physicsType)

	def OnButtonRelease(self, cbInfo, btInfo, user):
		print("Yo")
		if (btInfo.button == 0):
			#self.physical('').applyImpulse( VRScript.Math.Vector(10,0,0) )
			m = self.movable().getPose()
			m.postEuler(90,0,0)
			self.movable().setPose(m)
		
scene = lel_common.LELScenario()

#door = scene.create_entity("Wood Door 760mm", "models\\Wood Door 760mm.ive", [-5.15169267326709,-4.40547834621083,0.0], True, True, "Concave", True, "Static")
#door.SetDoor(True)
door = Door("Wood Door 760mm", "models\\Wood Door 760mm.ive", [-5.15169267326709,-4.40547834621083,0.0], True, True, "Concave", True, "Static")

scene.create_entity("stray_geometry", "models\\stray_geometry.ive", [0,0,0], True, True, "Concave", False)
scene.create_ground_plane()

m = VRScript.Math.Matrix( VRScript.Math.Quat(1,0,0) )
