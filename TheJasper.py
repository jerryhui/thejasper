from JasperEngine import *

# The Jasper - A Haunted House for CAVE
# Modeling: Jerry Chen, Natalie Flunker, Hasti Mirkia
# Program: Jerry Hui
#
# Created for DS501, Spring 2013
		
#-------------------------- MAIN PROGRAM --------------------------------------

theJasper = HauntedHouseEngine()

houseCoord = [-12.7, 2.25, 0]
landscapeCoord = [ houseCoord[0]-18.36, houseCoord[1]-30.47, 0]
theJasper.create_entity("fullHouse", "Models\\final.ive", houseCoord, True, False, "Concave", False, "Static")
theJasper.create_entity("simpleHouse", "Models\\simpleHouse.ive", houseCoord, False, True, "Concave", False, "Static")
theJasper.AddObject( HouseObjects.ScalableObj("landscape", "Models\\Landscape\\landscape.ive", landscapeCoord, True, False, "Concave", False, "Static", [0.3048,0.3048,0.3048]))

ghostMan = theJasper.AddParanormal(Paranormal.Ghost("ghostMan", "ghostman.ive", [0,0,0], "LOOK"))
# ghostMan = theJasper.AddParanormal(Paranormal.GhostFlyaway("ghostManFlyaway", "ghostman.ive", [-1,-2,0], "LOOK"))

chair = theJasper.AddObject(HouseObjects.BumpableObj("chair1", "Furniture\\chair001.ive",[1,1,0]))
chair.SetBumpedSound("ChairKick.wav")
chair = theJasper.AddObject(HouseObjects.BumpableObj("chair2", "Furniture\\chair001.ive",[1,3,0]))
chair.SetBumpedSound("ChairKick.wav")

theJasper.AddMusic("ligeti-atmospheres.wav")
theJasper.AddMusic("ligeti-lux.wav")
# VRScript.Interaction.setJumpPoint(0,VRScript.Math.Matrix().setTranslation(VRScript.Math.Vector(-5,-4,0.52115)))