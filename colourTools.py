
"""
Angus Goody
colourTools module for SHED
module containing functions for colour manipulation and generation
"""

#===================HEX Functions=================

def generateHexColour():
	"""
	Will generate a HEX colour
	"""
	colour = "%06x" % random.randint(0, 0xFFFFFF)
	colour="#"+colour.upper()
	return colour

def convertHEXtoRGB(hexColour):
	"""
	Will return 3 values in a tuple r g b respectivley
	"""
	hexColour = hexColour.lstrip('#')
	return tuple(int(hexColour[i:i+2], 16) for i in (0, 2, 4))

def convertRBGtoHEX(r,g,b):
	"""
	Will return a HEX value for the RGB values
	"""
	return "#{:02x}{:02x}{:02x}".format(r,g,b)

def generateShade(colour,percentage):
	"""
	Will generate percentage shade of colour
	"""
	rgbValue=convertHEXtoRGB(colour)
	redValue=int(rgbValue[0]*(percentage/100))
	greenValue=int(rgbValue[1]*(percentage/100))
	blueValue=int(rgbValue[2]*(percentage/100))
	return convertRBGtoHEX(redValue,greenValue,blueValue)

def generateTint(colour,percentage):
	"""
	Will generate a colour tint given
	a percentage value
	"""
	rgbValue=convertHEXtoRGB(colour)
	redValue=int(rgbValue[0] +((255-rgbValue[0])*(percentage/100)))
	greenValue=int(rgbValue[1] +((255-rgbValue[1])*(percentage/100)))
	blueValue=int(rgbValue[2] +((255-rgbValue[2])*(percentage/100)))
	return convertRBGtoHEX(redValue,greenValue,blueValue)

def generateMultipleShadesOrTints(colour,amountOfColours,tintOrShade):
	"""
	Will generate a certain amount of shades
	of a colour varying in percentages

	shade = generate shades
	tint = generate tint
	"""
	percentageChange=int(100/amountOfColours)
	percentCounter=1
	#Store shades
	newColours=[]
	#Loop over each shade
	for x in range(0,amountOfColours):
		#Calculate the percentage to shade by
		newPercent=percentageChange*percentCounter
		percentCounter+=1
		#Generate the colour
		if tintOrShade.upper() == "S":
			newColours.append(generateShade(colour,newPercent))
		else:
			newColours.append(generateTint(colour,newPercent))
	return newColours

def getColourForBackground(bgColour):
	"""
	Will decide on the best foreground text
	colour based on the colour of the 
	"""
	rgbValue=convertHEXtoRGB(bgColour)
	redValue=rgbValue[0]
	greenValue=rgbValue[1]
	blueValue=rgbValue[2]
	luminance = int(0.299*(redValue) + 0.587*(greenValue) + 0.114*(blueValue))
	if luminance/255 > 0.5:
		return "#000000"
	else:
		return "#FFFFFF"