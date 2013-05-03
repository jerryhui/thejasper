import VRScript
import lel_common

scene = lel_common.LELScenario()
scene.create_entity("DoorTest2_1", "models\\DoorTest2_1.osg", [-5.15169267326709,-4.42547834596913,-9.03557601863623e-018], True, False, "Concave", False, "Static")
scene.create_entity("stray_geometry", "models\\stray_geometry.osg", [0,0,0], True, True, "Concave", False)
scene.create_ground_plane()

import TheJasper