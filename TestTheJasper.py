from JasperEngine import *

# The Jasper - A Haunted House for CAVE
# Modeling: Jerry Chen, Natalie Flunker, Hasti Mirkia
# Program: Jerry Hui
#
# Created for DS501, Spring 2013

		
#------------------------------------------------------------------------------
#-------------------------- MAIN PROGRAM --------------------------------------

theJasper = HauntedHouseEngine()
# doorL = theJasper.AddObject(HouseObjects.Door("DoorLeft", "DoorLeft.osg", [-5.09199479842989,-4.40669061564667,-6.72643819712604e-018], True, -90))
# theJasper.set_physics_properties("DoorLeft", [1.0, 0.25, 0.9, 1, 0.5])
# doorR = theJasper.AddObject(HouseObjects.Door("DoorLeft_1", "DoorLeft.osg", [-3.40250259842728,-4.42017033590422,-6.54019670039207e-018], True, 90))
# theJasper.set_physics_properties("DoorLeft_1", [1.0, 0.25, 0.9, 1, 0.5])

# boxMonster = theJasper.AddParanormal(Paranormal.GhostFlyaway("boxMonster", "boxmon.osg", [-1,-3,0], "TOUCH"))
boxMonster2 = theJasper.AddParanormal(Paranormal.Crawler("boxMonster2", "boxmon.osg", [-1.5,-4,0], "TOUCH"))

# ghostMan = theJasper.AddParanormal(Paranormal.Lurcher("ghostMan", "ghostman.ive", [-1,-1,0], "NEAR", Paranormal.ParanormalState.Hiding))
ghostMan2 = theJasper.AddParanormal(Paranormal.GhostFlyaway("ghostManFlyaway", "ghostman.ive", [-1,-2,0], "CLICK", Paranormal.ParanormalState.Discovered))

chair = theJasper.AddObject(HouseObjects.BumpableObj("chair1", "Models\\Furniture\\chair001.ive",[1,1,0]))
chair.SetBumpedSound("ChairKick.wav")

# ghostMan.SetDiscoveredAnimation("001-01start.fbx", VRScript.Core.PlayMode.Loop, [90,0,0], VRScript.Math.Vector(0.01,0.01,0.01))
# ghostMan.SetCapturedAnimation("jc-001.fbx")

theJasper.AddMusic("ligeti-atmospheres.wav")
theJasper.AddMusic("ligeti-lux.wav")

# theJasper.create_entity("stairs", "Models\\stairs.osg", [-.5,0,0], True, True, "Concave", False, "Static")
theJasper.create_entity("stray_geometry", "models\\stray_geometry.osg", [0,0,0], True, True, "Concave", False, "Static")

theJasper.CreateGround()
# theJasper.create_ground_plane()
