from JasperEngine import *
import time

# The Jasper - A Haunted House for CAVE
# Modeling: Jerry Chen, Natalie Flunker, Hasti Mirkia
# Program: Jerry Hui
#
# Created for DS501, Spring 2013
		
#-------------------------- MAIN PROGRAM --------------------------------------
timestamp_start = time.time()

theJasper = HauntedHouseEngine()

houseCoord = [-12.7, 2.25, 0]
landscapeCoord = [-12.7, 2.25, 0]
# landscapeCoord = [-12.7, 2.25, -0.53]

# baked model for showing
# theJasper.create_entity("fullHouse", "Models\\final.ive", houseCoord, True, False, "Concave", False, "Static")
theJasper.create_entity("landscape", "Models\\landscape.ive", landscapeCoord, True, True, "Concave", False, "Static")
# simple model for physics
theJasper.create_entity("simpleHouse", "Models\\simpleHouse.ive", houseCoord, True, True, "Concave", False, "Static")

ghostMan = theJasper.AddParanormal(Paranormal.Ghost("ghostMan", "ghostman.ive", [0,0,0], "LOOK"))
# ghostMan = theJasper.AddParanormal(Paranormal.GhostFlyaway("ghostManFlyaway", "ghostman.ive", [-1,-2,0], "LOOK"))

chair = theJasper.AddObject(HouseObjects.BumpableObj("chair1", "Furniture\\chair001.ive",[1,1,0]))
chair.SetBumpedSound("ChairKick.wav")
chair = theJasper.AddObject(HouseObjects.BumpableObj("chair2", "Furniture\\chair001.ive",[1,3,0],"ChairKick.wav"))

# Doors, furniture
MainDoorLeft = theJasper.AddObject(HouseObjects.Door("MainDoorLeft", "Furniture\\lobby-door-left.ive", [-4.785,-0.712,0], True, -90))
MainDoorRight = theJasper.AddObject(HouseObjects.Door("MainDoorRight", "Furniture\\lobby-door-right.ive", [-2.44,-0.742,0], True, 90))
MainDoorLeft.AddSlaveDoor(MainDoorRight)

theJasper.AddObject(HouseObjects.Door("BR1Door", "Furniture\\brDoor.ive", [-1.950541497481799,11.9752809323588,4.43999994634174], True, -90))
theJasper.AddObject(HouseObjects.Door("BR2Door", "Furniture\\brDoor.ive", [-4.858116923442199,7.54166174274206,4.43999994634174], True, -90))
theJasper.AddObject(HouseObjects.Door("BR3Door", "Furniture\\brDoor.ive", [-1.950541497481799,6.95758311744,4.43999994634174], True, -90))
theJasper.AddObject(HouseObjects.Door("BR4Door", "Furniture\\brDoor.ive", [-4.858116923442199,2.563359678464464,4.43999994634174], True, -90))
theJasper.AddObject(HouseObjects.Door("BR1BathDoor", "Furniture\\brDoor.ive", [-1.341027110955999,8.93479536299549,4.43999994634174], True, -90))
theJasper.AddObject(HouseObjects.Door("BR2BathDoor", "Furniture\\brDoor.ive", [-6.351631299284609,10.59214731198452,4.43999994634174], True, -90))
theJasper.AddObject(HouseObjects.Door("BR3BathDoor", "Furniture\\brDoor.ive", [-1.311631360193999,3.93479542342146,4.43999994634174], True, -90))
theJasper.AddObject(HouseObjects.Door("BR4BathDoor", "Furniture\\brDoor.ive", [-6.391027049925829,5.592147372410491,4.43999994634174], True, -90))


theJasper.AddMusic("ligeti-lux.wav")
theJasper.AddMusic("ligeti-atmospheres.wav")
# VRScript.Interaction.setJumpPoint(0,VRScript.Math.Matrix().setTranslation(VRScript.Math.Vector(-5,-4,0.52115)))

print("Finished loading The Jasper in {0} seconds.".format(time.time()-timestamp_start))