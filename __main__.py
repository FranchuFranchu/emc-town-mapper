import json
import re
import os
import sys

#os.system('rm marker_earth.json')
#os.system('wget https://earthmc.net/map/tiles/_markers_/marker_earth.json')

	
with open('marker_earth.json') as f:
	d = json.load(f)["sets"]["townyPlugin.markerset"]["areas"]



	
import os
import pygame
import time
pygame.init()
pygame.mixer.quit()

bgimage = pygame.image.load("bg.png")
imagerect = bgimage.get_rect()

starimg = pygame.image.load("star.png")
cityimg = pygame.image.load("city.png")
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
	
colors = {
	"Argentina": "#FF4444",
	"Uruguay": "#FF4444",
	"Peru": "#FF4444",
	"Bolivia": "#FF4444",
	"Chile": "#FF4444",
	"Paraguay": "#FF4444",
	"Colombia": "#FF4444",
	
	"Brazil": "#44FF44",
	"Los_Pampas": "#44FF44",
	
	"Cuba": "#4444FF",
	"Haiti": "#4444FF",
	"Dominican": "#4444FF",
	"Manabi": "#4444FF",
	"Cordoba": "#4444FF",
	"Nicaragua": "#4444FF",
	"Yucatan": "#4444FF",
	"New Grenada": "#4444FF",
	
}

surfs = {}

for k, v in colors.items():
	surfs[k] = cityimg.copy()
	arr = pygame.PixelArray(surfs[k])
	arr.replace(pygame.Color("#FFFFFF"), pygame.Color(v))
	del arr
	

screen = pygame.display.set_mode((imagerect.width, imagerect.height))
time.sleep(2)
screen.blit(bgimage, imagerect)
pygame.display.flip()

was_added = set()

for k, v in d.items():
	avg = [sum(v["x"]) / len(v["x"]), sum(v["z"]) / len(v["z"])]
	if "(Shop)" in v["label"]:
		continue
	if v["label"] in was_added:
		continue
	was_added.add(v["label"])
	m = re.search(r"<span style=\"font-size:120%\">(.+?)<\/span>", v["desc"])
	m = re.fullmatch(r".+\((.+)\)", m.group(1))
	if m:
		nation = m.group(1)
		if surfs.get(nation) is None:
			continue
		print(nation)
		cityimg = surfs[nation]
	else:
		continue
	cityrect.x = (int(avg[0]) + 15600) * (1500 / 9000)
	cityrect.y = (int(avg[1]) + 2600) * (1500 / 9000)
	if cityrect.x < 0 or cityrect.y < 0:
		continue
	screen.blit(cityimg, cityrect)

pygame.display.flip()
time.sleep(2)
pygame.image.save(screen, "/tmp/out.png")

		
