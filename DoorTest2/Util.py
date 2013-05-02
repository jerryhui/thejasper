import VRScript

##COLORS
red = VRScript.Core.Color(1,0,0)
green = VRScript.Core.Color(0,1,0)
blue = VRScript.Core.Color(0,0,1)
black = VRScript.Core.Color(0,0,0)
white = VRScript.Core.Color(1,1,1)

##PHYSICS PROPS
phys_heavy = VRScript.Core.PhysicsProperties(10,5.0,0,0,0)
phys_light = VRScript.Core.PhysicsProperties(1,1.0,0,0,0)
phys_ultraheavy = VRScript.Core.PhysicsProperties(1,0,0,0,0)

def split_list(lizt,pieces):
	newlist = []
	n = len(lizt)/pieces
	r = len(lizt)%pieces
	b,e = 0, int(n+min(1,r))
	for i in range(pieces):
		newlist.append(lizt[b:e])
		r = max(0,r-1)
		b,e, = e, int(e + n + min(1,r))	
	return newlist
	
def listToVectors(lizt, pieces):
	lizt = split_list(lizt,pieces)
	vects = list()
	for v in lizt:
		vect = VRScript.Math.Vector(v[0],-v[2],v[1])
		vects.append(vect)
	return vects

def SVMFormat(label, lizt):
        string = str(label)

        for i in range(0,len(lizt)):
                string += " " + str(i+1)+ ":" + str(lizt[i])
        return string+'\n'
