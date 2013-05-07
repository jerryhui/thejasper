from JasperEngine import *

# The Jasper - A Haunted House for CAVE
# Modeling: Jerry Chen, Natalie Flunker, Hasti Mirkia
# Program: Jerry Hui
#
# Created for DS501, Spring 2013

		
#------------------------------------------------------------------------------
#-------------------------- MAIN PROGRAM --------------------------------------

theJasper = HauntedHouseEngine()

doorL = theJasper.AddObject(HouseObjects.Door("DoorLeft", "Furniture\\brDoor.ive", [-5.09199479842989,-4.40669061564667,0], True, -90))
doorR = theJasper.AddObject(HouseObjects.Door("DoorLeft_1", "Furniture\\brDoor.ive", [-3.40250259842728,-4.42017033590422,0], True, 90))
doorL.AddSlaveDoor(doorR)

# boxMonster = theJasper.AddParanormal(Paranormal.GhostFlyaway("boxMonster", "boxmon.osg", [-1,-3,0], "TOUCH"))
boxMonster2 = theJasper.AddParanormal(Paranormal.Crawler("boxMonster2", "boxmon.osg", [-1.5,-4,0], "TOUCH"))

# ghostMan = theJasper.AddParanormal(Paranormal.Lurcher("ghostMan", "ghostman.ive", [-1,-1,0], "NEAR", Paranormal.ParanormalState.Hiding))
ghostMan2 = theJasper.AddParanormal(Paranormal.GhostFlyaway("ghostManFlyaway", "ghostman.ive", [-1,-2,0], "CLICK", Paranormal.ParanormalState.Discovered))

chair = theJasper.AddObject(HouseObjects.BumpableObj("chair1", "Furniture\\chair001.ive",[1,1,0]))
chair.SetBumpedSound("ChairKick.wav")

# ghostMan.SetDiscoveredAnimation("001-01start.fbx", VRScript.Core.PlayMode.Loop, [90,0,0], VRScript.Math.Vector(0.01,0.01,0.01))
# ghostMan.SetCapturedAnimation("jc-001.fbx")

theJasper.AddMusic("ligeti-atmospheres.wav")
theJasper.AddMusic("ligeti-lux.wav")

# theJasper.create_entity("stairs", "Models\\stairs.osg", [-.5,0,0], True, True, "Concave", False, "Static")
theJasper.create_entity("stray_geometry", "models\\stray_geometry.osg", [0,0,0], True, True, "Concave", False, "Static")

theJasper.CreateGround()
# theJasper.create_ground_plane()
