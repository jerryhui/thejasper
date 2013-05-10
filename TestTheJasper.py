from JasperEngine import *
from Paranormal import ParanormalState

# The Jasper - A Haunted House for CAVE
# Modeling: Jerry Chen, Natalie Flunker, Hasti Mirkia
# Program: Jerry Hui
#
# Created for DS501, Spring 2013

		
#------------------------------------------------------------------------------
#-------------------------- MAIN PROGRAM --------------------------------------

theJasper = HauntedHouseEngine()

# ----- Double door test -----
doorL = theJasper.AddObject(HouseObjects.Door("DoorLeft", "Furniture\\brDoor.ive", [-5.09199479842989,-4.40669061564667,0], True, -90))
doorR = theJasper.AddObject(HouseObjects.Door("DoorLeft_1", "Furniture\\brDoor.ive", [-3.40250259842728,-4.42017033590422,0], True, 90))
doorL.AddSlaveDoor(doorR)

# boxMonster = theJasper.AddParanormal(Paranormal.GhostFlyaway("boxMonster", "boxmon.osg", [-1,-3,0], "TOUCH"))
# boxMonster2 = theJasper.AddParanormal(Paranormal.Crawler("boxMonster2", "boxmon.osg", [-1.5,-4,0], "TOUCH"))

ghostMan = theJasper.AddParanormal(Paranormal.SkeletonBiker("skelBike", "skeletonbike.ive", [-1,-1,0], "NEAR", Paranormal.ParanormalState.Hiding, "CLICK", [90,0,0]))
ghostMan = theJasper.AddParanormal(Paranormal.SkeletonBiker("skelBike2", "skeletonbike.ive", [1,-1,0], "NEAR", Paranormal.ParanormalState.Hiding, "CLICK", [135,0,0]))
# ghostMan = theJasper.AddParanormal(Paranormal.Lurcher("ghostMan", "ghostman.ive", [-1,-1,0], "NEAR", Paranormal.ParanormalState.Hiding, "CLICK"))
ghostMan2 = theJasper.AddParanormal(Paranormal.GhostFlyaway("ghostManFlyaway", "ghostman.ive", [-1,-2,0], "NEAR", Paranormal.ParanormalState.Discovered, .001, .01, "CLICK"))

fireMonster = theJasper.AddParanormal(Paranormal.Paranormal("FireMonster", "firemon-hidden.fbx", [3,5,1], "LOOK", ParanormalState.Hiding))
fireMonster.SetDiscoveredAnimation("firemon-hidden.fbx",VRScript.Core.PlayMode.Loop,[90,0,-90])
fireMonster.SetDiscoveredSound("AudioFiles\\Fire.wav")
fireMonster.SetCapturedAnimation("firemon-captured.fbx",VRScript.Core.PlayMode.Loop,[90,0,0])
fireMonster.SetStaring(True)

# ----- chair bump test -----
chair = theJasper.AddObject(HouseObjects.BumpableObj("chair1", "Furniture\\chair001.ive",[1,1,0]))
chair.SetBumpedSound("ChairKick.wav")

# ghostMan.SetDiscoveredAnimation("001-01start.fbx", VRScript.Core.PlayMode.Loop, [90,0,0], VRScript.Math.Vector(0.01,0.01,0.01))
# ghostMan.SetCapturedAnimation("jc-001.fbx")

# houseCoord = [-12.7, 2.25, 0]
# landscapeCoord = [ houseCoord[0]-18.36, houseCoord[1]-30.47, 0]
# landscapeObj = HouseObjects.ScalableObj("landscape", "Models\\Landscape\\landscape.ive", [0,0,0], True, False, "Concave", False, "Static", [0.3048,0.3048,0.3048])
# theJasper.AddObject( landscapeObj )
# chair = theJasper.AddObject(HouseObjects.ScalableObj("landscape", "Landscape\\landscape.ive",[1,1,0]))

# theJasper.AddMusic("ligeti-atmospheres.wav")
theJasper.AddMusic("ligeti-lux.wav")

# theJasper.create_entity("stairs", "Models\\stairs.osg", [-.5,0,0], True, True, "Concave", False, "Static")

theJasper.CreateGround()
# theJasper.create_ground_plane()