import VRScript
import lel_common
import HouseObjects

scene = lel_common.LELScenario()
scene.create_entity("DoorTest2_1", "models\\DoorTest2_1.osg", [-4.32269268328572,-4.37363834659563,1.17099998584824], True, False, "Concave", False, "Static")
scene.create_entity("DoorTest2_2", "models\\DoorTest2_2.osg", [-5.09069267400429,-4.40547834621083,0.949999988519066], True, False, "Concave", False, "Static")
scene.create_entity("DoorTest2_3", "models\\DoorTest2_3.osg", [-5.09069267400429,-4.40547834621083,0.209999997462109], True, False, "Concave", False, "Static")
scene.create_entity("DoorTest2_4", "models\\DoorTest2_4.osg", [-5.09069267400429,-4.40547834621083,1.76999997860921], True, False, "Concave", False, "Static")
scene.create_entity("Group2", "models\\Group2.osg", [-5.15169267326709,-4.27669061721775,-9.03557601863623e-018], True, False, "Concave", False, "Static")

door = HouseObjects.Door("DoorProper", "models\\DoorProper.osg", [-5.09199479842989,-4.40669061564667,-6.72643819712604e-018], True, True, "Concave", True, "Dynamic")
door.SetPhysProperties([1.0, 0.25, 0.9, 1, 0.5])


scene.create_entity("stray_geometry", "models\\stray_geometry.osg", [0,0,0], True, True, "Concave", False)
scene.create_ground_plane()
