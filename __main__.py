import json
import re
import os
import sys
from pathlib import Path


PARENT = Path(__file__).parent

### SETTINGS BEGIN ###

# Topleft Minecraft coordinate of the output
TOPLEFT = (-12560, 4000)
# Bottomright 
BOTTOMRIGHT = (-10000, 7096)
# Output image horizontal resolution
IMAGE_WIDTH = 1000
# Size of the area in the map
MC_SIZE = ((BOTTOMRIGHT[0] - TOPLEFT[0]), (BOTTOMRIGHT[1] - TOPLEFT[1]))
# Output image size
IMAGE_SIZE = (IMAGE_WIDTH, IMAGE_WIDTH * MC_SIZE[1] / MC_SIZE[0])

# This is a mapping between nations and colors
# For some reason, this is in #BBGGRR format, not #RRGGBB
colors = {
	"Argentina": "#FF4444",
	"Uruguay": "#FF4444",
	"Peru": "#FF4444",
	"Bolivia": "#FF4444",
	"Chile": "#FF4444",
	"Paraguay": "#FF4444",
	"Colombia": "#FF4444",
	
	"Glacier_Spartan": "#FF8888",
	
	"Brazil": "#44FF44",
	"Los_Pampas": "#44FF44",
	
	"Cuba": "#4444FF",
	"Haiti": "#4444FF",
	"Dominican": "#4444FF",
	"Manabi": "#4444FF",
	"Cordoba": "#4444FF",
	"Panama": "#4444FF",
	"Nicaragua": "#4444FF",
	"Yucatan": "#4444FF",
	"New_Granada": "#4444FF",
	
	"Venezuela": "#CC88FF",
	"Ecuador": "#CC88FF",
	"Centroamérica": "#CC88FF",
	"South_America": "#CC88FF",
	
	"Peru-Bolivia": "#44FFFF",
	"Boyaca": "#44FFFF",
	
	"Spanish_Antilles": "#FF4444",
	
	"Patagonia": "#4488FF",
	
	"": "#FFFFFF",	
}

### SETTINGS END ###

# TODO use platform-independent Python modules to update the marker_earth frile

#os.system('rm marker_earth.json')
#os.system('wget https://earthmc.net/map/tiles/_markers_/marker_earth.json')

	
with open(PARENT / 'marker_earth.json') as f:
	d = json.load(f)["sets"]["townyPlugin.markerset"]["areas"]



	
import os
import pygame
import time
pygame.init()
pygame.mixer.quit()

starimg = pygame.image.load(PARENT / "star.png")
cityimg = pygame.image.load(PARENT / "city.png")
cityrect = cityimg.get_rect()

'''
	"Argentina": "#FF8800",
	"Uruguay": "#FF8888",
	"Peru": "#4444FF",
	"Inca": "#4444FF",
	"Chile": "#0088FF",
	"Paraguay": "#88FF88",
	"Colombia": "#c99960",
	"Bolivia": "#44FFCC",
'''

# Create city images for each nation
surfs = {}

for k, v in colors.items():
	surfs[k] = cityimg.copy()
	arr = pygame.PixelArray(surfs[k])
	arr.replace(pygame.Color("#FFFFFF"), pygame.Color(v))
	del arr
	

screen = pygame.Surface((IMAGE_SIZE[0], IMAGE_SIZE[1]), flags=pygame.SRCALPHA)
screen.set_alpha(0)

was_added = set()

print(screen.get_width(), screen.get_height())

for k, v in d.items():
	# Calculate average X and Y of town chunks (roughly)
	avg = [sum(v["x"]) / len(v["x"]), sum(v["z"]) / len(v["z"])]
	
	was_added.add(v["label"])
	m1 = re.search(r"<span style=\"font-size:120%\">(.+?)<\/span>", v["desc"])
	m = re.fullmatch(r"(.+) \((.*)\)", m1.group(1))
	m2 = re.fullmatch(r".+", m1.group(1))
	if m:
		if "(Shop)" in m.group(1):
			# This is a shop plot and doesn't count
			continue
		
		nation = m.group(2)
		if surfs.get(nation) is None:
			# Not a nation that should be displayed
			continue
		
		print(nation)
		cityimg = surfs[nation]
	elif m2:
		cityimg = surfs[""]
	else:
		continue
		
	# Transform to image coordinates
	cityrect.x = (int(avg[0]) - TOPLEFT[0]) * (IMAGE_SIZE[0] / MC_SIZE[0])
	cityrect.y = (int(avg[1]) - TOPLEFT[1]) * (IMAGE_SIZE[1] / MC_SIZE[1])
	
	if cityrect.x < 0 or cityrect.y < 0:
		# it's outside of the image
		continue
	screen.blit(cityimg, cityrect)

pygame.image.save(screen, "./out.png")

		
