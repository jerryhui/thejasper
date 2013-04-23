import VRScript
import lel_common
import HouseObjects

user = VRScript.Core.Entity('User0')

doorL = HouseObjects.Door("DoorLeft", "models\\DoorLeft.osg", [-5.09199479842989,-4.40669061564667,-6.72643819712604e-018], True, -90)
#scene.set_physics_properties("DoorLeft", [1.0, 0.25, 0.9, 1, 0.5])

doorR = HouseObjects.Door("DoorLeft_1", "models\\DoorLeft_1.osg", [-3.40250259842728,-4.42017033590422,-6.54019670039207e-018], True, 90)
#scene.set_physics_properties("DoorLeft_1", [1.0, 0.25, 0.9, 1, 0.5])