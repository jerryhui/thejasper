import VRScript
import math

class WiiBoardMovement(VRScript.Core.Behavior):
    
    def __init__(self,entity=None):
        VRScript.Core.Behavior.__init__(self,entity)
        self.gX=0
        self.gY=0
        self.aveX=0
        self.aveY=0
        self.aveRot=0
        self.w=.2
        self.frontBias = .015
        self.data = [0.0,0.0,0.0,0.0]

    def SetBalanceValues(self, vals):
        self.data[0]=vals[0]
        self.data[1]=vals[1]
        self.data[2]=vals[2]
        self.data[3]=vals[3]
        # print("-----------")
        # print(self.data[0])
        # print(self.data[1])
        # print(self.data[2])
        # print(self.data[3])
		
    def OnUpdate(self, info):
        #data = viz.getData()
        
        #top left + top right together should move the user forward
        #bottom left + bottom right together should move the user back (in regards to whatever direction they're facing..
        
        #top left + bottom left together should move the user left (strafe)
        #top right + bottom right together should move the user right (strafe)
        
        #top right + bottom left together should turn user left
        #top left + bottom right together shold turn user right
        		
        nD = [0] * 4
        nD[0] = abs(self.data[0])
        nD[1] = abs(self.data[1])
        nD[2] = abs(self.data[2])
        nD[3] = abs(self.data[3])
        # tot=0
        # for i in range(4):
            # tot+=abs(self.data[i])

        
        # for i in range(4):
            # if(tot != 0):
                # nD[i] = (abs(self.data[i])) / tot
            # else:
                # nD[i] = 0
        #print("-----------")
        #print(nD[0])
        #print(nD[1])
        #print(nD[2])
        #print(nD[3])
        theUser = VRScript.Core.Entity('User0')
        user_rot = theUser.movable().selfToWorld().getQuat()
        vMoveX = ((nD[0] + nD[2]) - (nD[1] + nD[3])) * 0.01
        vMoveY = ((nD[0] + nD[1]) - (nD[2] + nD[3])) * 0.01
        v = VRScript.Math.Vector(vMoveX, vMoveY, 0)
        v = user_rot.rotate(v)
        m = theUser.movable().selfToWorld()
        mFinal = m.postTranslation(v)
        theUser.movable().setPose(mFinal)
        
        # # (TL + BL) - (TR + BR)
        # moveX = 0.075 * math.pow((nD[0] + nD[2]) - (nD[1] + nD[3]),3)
        # moveY = 0.050 * math.pow(-nD[0] - nD[1] + nD[2] + nD[3],5)+self.frontBias
        
        # rot = math.pow((nD[0] + nD[3]) - (nD[1] + nD[2]),1)

        # #print(tot, moveX, moveY, "\r")
        # # amount = .075#tot / 500.0
        # wiiThresholdX = 0
        # wiiThresholdY = 0
        # wiiThresholdRot = .6
        # if (tot > 5 and abs(moveX) > wiiThresholdX) and (abs(moveY) > wiiThresholdY) :
            # theUser = VRScript.Core.Entity('User0')
            # user_rot = theUser.movable().selfToWorld().getQuat()
        
            # self.aveX = self.w*moveX + (1.0-self.w)*self.aveX;
            # self.aveY = self.w*moveY + (1.0-self.w)*self.aveY;
            # self.aveRot = self.w*rot + (1.0-self.w)*self.aveRot;
            
            # v = VRScript.Math.Vector(self.aveX, self.aveY, 0)
            # self.gX +=v.x
            # self.gY +=v.y
            # #print(self.gX, self.gY)
         # #   print(amount, moveX*amount,moveY*amount)
            # #v = user_rot.rotate(v)
            # #theUser.physical().applyImpulse(v,VRScript.Math.Vector(0,0,0))
            # m = theUser.movable().selfToWorld()
            # if (abs(self.aveRot) > wiiThresholdRot):
                # mFinal = m.postAxisAngle(self.aveRot, VRScript.Math.Vector(0,0,1))
            # else:
                # mFinal = m.postTranslation(v)
            # theUser.movable().setPose(mFinal)

#WiiBoardMovement()
