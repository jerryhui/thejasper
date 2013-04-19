import VRScript
import math		

class Billboard(VRScript.Core.Behavior):
	def __init__(self, sName, position, follow=True):
		VRScript.Core.Behavior.__init__(self, sName)
		self.name = sName
		self.pos = position
		self.alignToUser = follow
	
	def OnInit(self, cbInfo):
		m = VRScript.Math.Matrix()
		m.setTranslation(self.pos)
		self.movable().setPose(m)
		
	def OnUpdate(self, cbInfo):
		if(self.alignToUser):
			us = VRScript.Core.Entity("User0Head")
			#get our world pose
			m = us.movable().selfToWorld()
			ourPos = m.getTranslation()
			billTrans = self.movable().getPose()
			#print("Old:")
			#print(str(billTrans.toString()))
			
			#print("Us:")
			#print(str(ourPos.x))
			#print(str(ourPos.y))
			#print(str(ourPos.z))
			
			billPos = billTrans.getTranslation()
			ourPos.z = 0.0
			oldZ = billPos.z
			billPos.z = 0.0
			billPos.y = billPos.y - 0.1
			v = VRScript.Math.Vector(billPos - ourPos)
			billPos.y = billPos.y + 0.1
			v = v.normalize()
			forward = VRScript.Math.Vector(0.0, 1.0, 0.0)
			angle = math.acos(forward.dot(v))
			angle = 360-math.degrees(angle)
			up = VRScript.Math.Vector(0.0, 0.0, 1.0)
			billPos.z = oldZ
			newMat = VRScript.Math.Matrix()
			newMat = newMat.postAxisAngle(angle, up)
			newMat.setTranslation(billPos)
			#print("New:")
			#print(str(newMat.toString()))
			self.movable().setPose(newMat)
		
	def AddFont(self, fontVRScriptName, text, transform, fontType, height=0.1, justification=VRScript.Core.Justification.Left):
		f = VRScript.Core.FontText(fontVRScriptName, text, fontType, transform)
		f.setHeight(height)
		f.setJustification(justification)
		f.show()
		self.attach(f)
	
	def AddShortNutritionLabel(self, textScale=1.0, trans=VRScript.Math.Matrix()):
		#todo - combine shortnutrionlabel and other function below into one..
		strFontName = "Helvetica___.ttf"
		strFontBlackName = "HelveticaBlk___.ttf"
		left = VRScript.Core.Justification.Left
		m = trans
		topPos = m.getTranslation()
		fHeightSpace = 0.25 * textScale
		self.AddFont("nfacts", "Nutrition Facts", m, strFontBlackName, fHeightSpace, left)
		v = VRScript.Math.Vector(topPos.x, topPos.y, topPos.z - fHeightSpace)
		m.setTranslation(v)
		fHeight = 0.08 * textScale
		self.AddFont("serving", "Serving Size 1 Cup (248g)", m, strFontName, fHeight, left)
		fHeightSpace = fHeightSpace + fHeight
		v = VRScript.Math.Vector(topPos.x, topPos.y, topPos.z - fHeightSpace)
		m.setTranslation(v)
		fHeight = 0.07 * textScale
		self.AddFont("amount", "Amount Per Serving", m, strFontBlackName, fHeight, left)
		fHeightSpace = fHeightSpace + fHeight + 0.01
		v = VRScript.Math.Vector(topPos.x, topPos.y, topPos.z - fHeightSpace)
		m.setTranslation(v)
		fHeight = 0.1 * textScale
		self.AddFont("cals", "Calories", m, strFontBlackName, fHeight, left)
		self.AddFont("cal_amount", "                   110                   Carlories from Fat 0", m, strFontName, fHeight, left)
		fHeightSpace = fHeightSpace + fHeight
		v = VRScript.Math.Vector(topPos.x, topPos.y, topPos.z - fHeightSpace)
		m.setTranslation(v)
		fHeightSpace = fHeightSpace + fHeight
		self.AddFont("perc", "                                              % Daily Value", m, strFontBlackName, fHeight, left)
		v = VRScript.Math.Vector(topPos.x, topPos.y, topPos.z - fHeightSpace)
		m.setTranslation(v)
		self.AddFont("total_fat", "Total Fat", m, strFontBlackName, fHeight, left)
		self.AddFont("total_fat_percent", "                                                             1%", m, strFontBlackName, fHeight, left)
		self.AddFont("total_fat_grams", "                    0.5g", m, strFontName, fHeight, left)
		fHeightSpace = fHeightSpace + fHeight
		v = VRScript.Math.Vector(topPos.x, topPos.y, topPos.z - fHeightSpace)
		m.setTranslation(v)
		self.AddFont("sodium", "Sodium 0mg", m, strFontName, fHeight, left)
		self.AddFont("sodium_perc", "                                                             0%", m, strFontBlackName, fHeight, left)
		fHeightSpace = fHeightSpace + fHeight
		v = VRScript.Math.Vector(topPos.x, topPos.y, topPos.z - fHeightSpace)
		m.setTranslation(v)
		self.AddFont("carbohydrate", "Total Carbohydrate", m, strFontBlackName, fHeight, left)
		self.AddFont("carbohydrate_perc", "                                                             9%", m, strFontBlackName, fHeight, left)
		self.AddFont("carbohydrate_grams", "                                     26g", m, strFontName, fHeight, left)
		fHeightSpace = fHeightSpace + fHeight
		v = VRScript.Math.Vector(topPos.x, topPos.y, topPos.z - fHeightSpace)
		m.setTranslation(v)
		self.AddFont("sugar", "   Sugars 21g", m, strFontName, fHeight, left)
		fHeightSpace = fHeightSpace + fHeight
		v = VRScript.Math.Vector(topPos.x, topPos.y, topPos.z - fHeightSpace)
		m.setTranslation(v)
		self.AddFont("protein", "Protein", m, strFontBlackName, fHeight, left)
		self.AddFont("protein_grams", "                 2g", m, strFontName, fHeight, left)
		fHeightSpace = fHeightSpace + fHeight
		v = VRScript.Math.Vector(topPos.x, topPos.y, topPos.z - fHeightSpace)
		m.setTranslation(v)
		self.AddFont("vitA", "Vitamin A 0%                      *              Vitamin C 210%", m, strFontName, fHeight, left)
		fHeightSpace = fHeightSpace + fHeight
		v = VRScript.Math.Vector(topPos.x, topPos.y, topPos.z - fHeightSpace)
		m.setTranslation(v)
		self.AddFont("calcium", "Calcium 2%                      *               Iron 2%", m, strFontName, fHeight, left)
		fHeightSpace = fHeightSpace + fHeight
		v = VRScript.Math.Vector(topPos.x, topPos.y, topPos.z - fHeightSpace)
		m.setTranslation(v)
		self.AddFont("hello_world", "Hello World!", m, strFontName, fHeight, left)
		fHeightSpace = fHeightSpace + fHeight + 0.2
		v = VRScript.Math.Vector(topPos.x, topPos.y, topPos.z - fHeightSpace)
		m.setTranslation(v)
		self.AddFont("msg_1", "Not a significant source of saturated fat, trans\n fat, cholesterol, dietary fiber.", m, strFontName, fHeight, left)
		fHeightSpace = fHeightSpace + fHeight + 0.2
		v = VRScript.Math.Vector(topPos.x, topPos.y, topPos.z - fHeightSpace)
		m.setTranslation(v)
		self.AddFont("msg_2", "*Percent Daily Values are based on a 2,000 calorie diet.\nYour Daily Values may be higher or lower depending\n on your calorie needs.", m, strFontName, fHeight, left)
		
	def AddNutritionLabel(self, textScale=1.0, trans=VRScript.Math.Matrix()):
		strFontName = "Helvetica___.ttf"
		strFontBlackName = "HelveticaBlk___.ttf"
		left = VRScript.Core.Justification.Left
		m = trans
		topPos = m.getTranslation()
		fHeightSpace = 0.25 * textScale
		self.AddFont("nfacts", "Nutrition Facts", m, strFontBlackName, fHeightSpace, left)
		v = VRScript.Math.Vector(topPos.x, topPos.y, topPos.z - fHeightSpace)
		m.setTranslation(v)
		fHeight = 0.08 * textScale
		self.AddFont("serving", "Serving Size 1 Cup (228g)\nServing per Container 2\n", m, strFontName, fHeight, left)
		fHeightSpace = fHeightSpace + fHeight
		v = VRScript.Math.Vector(topPos.x, topPos.y, topPos.z - fHeightSpace)
		m.setTranslation(v)
		fHeight = 0.07 * textScale
		self.AddFont("amount", "Amount Per Serving", m, strFontBlackName, fHeight, left)
		fHeightSpace = fHeightSpace + fHeight + 0.01
		v = VRScript.Math.Vector(topPos.x, topPos.y, topPos.z - fHeightSpace)
		m.setTranslation(v)
		fHeight = 0.1 * textScale
		self.AddFont("cals", "Calories", m, strFontBlackName, fHeight, left)
		self.AddFont("cal_amount", "                   260                   Carlories from Fat 120", m, strFontName, fHeight, left)
		fHeightSpace = fHeightSpace + fHeight
		v = VRScript.Math.Vector(topPos.x, topPos.y, topPos.z - fHeightSpace)
		m.setTranslation(v)
		fHeightSpace = fHeightSpace + fHeight
		self.AddFont("perc", "                                              % Daily Value", m, strFontBlackName, fHeight, left)
		#f51 = VRScript.Core.FontText("perc_line", "_______________________________________", strFontName, m5)
		#f51.setHeight(0.1)
		#f51.setJustification(VRScript.Core.Justification.Left)
		#f51.show()
		v = VRScript.Math.Vector(topPos.x, topPos.y, topPos.z - fHeightSpace)
		m.setTranslation(v)
		self.AddFont("total_fat", "Total Fat", m, strFontBlackName, fHeight, left)
		self.AddFont("total_fat_percent", "                                                             20%", m, strFontBlackName, fHeight, left)
		self.AddFont("total_fat_grams", "                    13g", m, strFontName, fHeight, left)
		fHeightSpace = fHeightSpace + fHeight
		v = VRScript.Math.Vector(topPos.x, topPos.y, topPos.z - fHeightSpace)
		m.setTranslation(v)
		self.AddFont("sat_fat", "  Saturated Fat 5g", m, strFontName, fHeight, left)
		self.AddFont("sat_fat_perc", "                                                             25%", m, strFontBlackName, fHeight, left)
		fHeightSpace = fHeightSpace + fHeight
		v = VRScript.Math.Vector(topPos.x, topPos.y, topPos.z - fHeightSpace)
		m.setTranslation(v)
		self.AddFont("trans_fat", "  Trans Fat 2g", m, strFontName, 0.1 * textScale, left)
		fHeightSpace = fHeightSpace + fHeight
		v = VRScript.Math.Vector(topPos.x, topPos.y, topPos.z - fHeightSpace)
		m.setTranslation(v)
		self.AddFont("cholesterol", "Cholesterol", m, strFontBlackName, fHeight, left)
		self.AddFont("cholesterol_perc", "                                                             10%", m, strFontBlackName, fHeight, left)
		self.AddFont("cholesterol_grams", "                          30mg", m, strFontName, fHeight, left)
		fHeightSpace = fHeightSpace + fHeight
		v = VRScript.Math.Vector(topPos.x, topPos.y, topPos.z - fHeightSpace)
		m.setTranslation(v)
		self.AddFont("sodium", "Sodium 660mg", m, strFontName, fHeight, left)
		self.AddFont("sodium_perc", "                                                             28%", m, strFontBlackName, fHeight, left)
		fHeightSpace = fHeightSpace + fHeight
		v = VRScript.Math.Vector(topPos.x, topPos.y, topPos.z - fHeightSpace)
		m.setTranslation(v)
		self.AddFont("carbohydrate", "Total Carbohydrate", m, strFontBlackName, fHeight, left)
		self.AddFont("carbohydrate_perc", "                                                             10%", m, strFontBlackName, fHeight, left)
		self.AddFont("carbohydrate_grams", "                                     31g", m, strFontName, fHeight, left)
		fHeightSpace = fHeightSpace + fHeight
		v = VRScript.Math.Vector(topPos.x, topPos.y, topPos.z - fHeightSpace)
		m.setTranslation(v)
		self.AddFont("fiber", "   Dietary Fiber 0g", m, strFontName, fHeight, left)
		self.AddFont("fiber_perc", "                                                               0%", m, strFontBlackName, fHeight, left)
		fHeightSpace = fHeightSpace + fHeight
		v = VRScript.Math.Vector(topPos.x, topPos.y, topPos.z - fHeightSpace)
		m.setTranslation(v)
		self.AddFont("sugar", "   Sugars 5g", m, strFontName, fHeight, left)
		fHeightSpace = fHeightSpace + fHeight
		v = VRScript.Math.Vector(topPos.x, topPos.y, topPos.z - fHeightSpace)
		m.setTranslation(v)
		self.AddFont("protein", "Protein", m, strFontBlackName, fHeight, left)
		self.AddFont("protein_grams", "                 5g", m, strFontName, fHeight, left)
		fHeightSpace = fHeightSpace + fHeight
		v = VRScript.Math.Vector(topPos.x, topPos.y, topPos.z - fHeightSpace)
		m.setTranslation(v)
		self.AddFont("vitA", "Vitamin A 4%                      *              Vitamin C 2%", m, strFontName, fHeight, left)
		fHeightSpace = fHeightSpace + fHeight
		v = VRScript.Math.Vector(topPos.x, topPos.y, topPos.z - fHeightSpace)
		m.setTranslation(v)
		self.AddFont("calcium", "Calcium 15%                      *               Iron 4%", m, strFontName, fHeight, left)
		fHeightSpace = fHeightSpace + fHeight
		v = VRScript.Math.Vector(topPos.x, topPos.y, topPos.z - fHeightSpace)
		m.setTranslation(v)
		self.AddFont("hello_world", "Hello World!", m, strFontName, fHeight, left)
		fHeightSpace = fHeightSpace + fHeight + 0.2
		v = VRScript.Math.Vector(topPos.x, topPos.y, topPos.z - fHeightSpace)
		m.setTranslation(v)
		self.AddFont("msg", "*Percent Daily Values are based on a 2,000 calorie diet.\nYour Daily Values may be higher or lower depending\n on your calorie needs.", m, strFontName, fHeight, left)
		