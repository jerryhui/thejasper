import VRScript
import lel_common
scene = lel_common.LELScenario()

door = scene.create_entity("Wood Door 760mm", "models\\Wood Door 760mm.ive", [-5.15169267326709,-4.40547834621083,0.0], True, False, "Concave", True, "Static")
door.SetDoor(True)

scene.create_entity("stray_geometry", "models\\stray_geometry.ive", [0,0,0], True, True, "Concave", False)
scene.create_ground_plane()

m = VRScript.Math.Matrix( VRScript.Math.Quat(1,0,0) )
