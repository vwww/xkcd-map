# Generate tiles
# adapted from https://github.com/dividuum/xkcd-1110

import os
import re
from PIL import Image

MAXIMUM_ZOOM = 10
FULL_QUALITY = 0
# FULL_QUALITY should be at least 2 ** MAXIMUM_ZOOM
# tested 2048 & ANTIALIAS: it is very slow and causes shifting error (similar to using 0 & BILINEAR)
DOWNSCALE_TYPE = Image.ANTIALIAS # Image.BILINEAR

worldmap = {}

if not os.path.isdir("converted"):
	os.makedirs("converted")

for name in os.listdir("tiles"):
    m = re.match("^([0-9]+)(s|n)([0-9]+)(w|e).png$", name)
    if m is None:
        print "fail", name
        continue
    y, yy, x, xx = m.groups()
    x, y = int(x), int(y)

    if xx == 'w':
        x  = 64 - x
    else:
        x  = 63 + x

    if yy == 'n':
        y = 64 - y
    else:
        y = 63 + y

    print x, y

    worldmap[x, y] = name

available = set()

def write_img(im, zoom, x, y):
    im.save('converted/%d-%d-%d.png' % (zoom, x, y))
    print 'save %d %d %d' % (zoom, x, y)
    available.add((zoom, x, y))

def load_img(zoom, x, y):
    if (zoom, x, y) not in available:
        return None
    #print 'load %d %d %d' % (zoom, x, y)
    return Image.open('converted/%d-%d-%d.png' % (zoom, x, y))

# render first set of tiles
for (x, y), name in worldmap.iteritems():
	im = Image.open('tiles/%s' % name)
	for xx in xrange(8):
		for yy in xrange(8):
			#part = im.crop((256 * xx, 256 * yy, 256 * (xx+1), 256 * (yy+1)))
			#write_img(part, MAXIMUM_ZOOM, x * 8 + xx, y * 8 + yy)
			available.add((MAXIMUM_ZOOM, x * 8 + xx, y * 8 + yy))#debug

if FULL_QUALITY:
	# new method: render every tile
	for zoom in xrange(MAXIMUM_ZOOM-1):
		print "zoom", zoom
		tilefactor = 2 ** (MAXIMUM_ZOOM - zoom)
		tilecount = 2 ** zoom
		tilequality = min(FULL_QUALITY, 256 * tilefactor)
		tilesize = tilequality / tilefactor
		for x in xrange(tilecount):
			for y in xrange(tilecount):
				if y >= (tilecount / 2):
					color = (36,36,36) #(0,0,0)
				else:
					color = (176,226,255) #(255, 255, 255)
				im = Image.new("RGB", (tilequality, tilequality), color)
				if zoom == 0:
					im.paste((176,226,255), (0, 0, tilequality, tilequality / 2))
					#im.paste((36,36,36), (0, tilequality / 2, tilequality, tilequality))
				found = 0
				for xx in xrange(tilefactor):
					for yy in xrange(tilefactor):
						tile = load_img(MAXIMUM_ZOOM, x * tilefactor + xx, y * tilefactor + yy)
						if tile is None:
							continue
						tile.thumbnail((tilesize, tilesize), DOWNSCALE_TYPE)
						im.paste(tile, (tilesize * xx, tilesize * yy))
						found += 1
				if found or True:
					if tilequality != 256:
						im.thumbnail((256, 256), DOWNSCALE_TYPE)
					write_img(im, zoom, x, y)
else:
	# old method: reuse tiles already rendered
	for zoom in xrange(MAXIMUM_ZOOM-1, -1, -1):
		print "zoom", zoom
		for x in xrange(2**zoom):
			for y in xrange(2**zoom):
				if y >= (2**(zoom-1)):
					color = (36,36,36) #(0,0,0)
				else:
					color = (176,226,255) #(255, 255, 255)
				im = Image.new("RGB", (512, 512), color)
				found = 0
				for xx in (0, 1):
					for yy in (0, 1):
						tile = load_img(zoom+1, x*2+xx, y*2+yy)
						if tile is None:
							continue
						im.paste(tile, (256 * xx, 256 * yy))
						found += 1
				if found:
					im.thumbnail((256, 256), DOWNSCALE_TYPE)
					write_img(im, zoom, x, y)
