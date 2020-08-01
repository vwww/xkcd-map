# xkcd-map
Generate images for the XKCD 1110 map.

`convert.py` uses the images in `tiles` to generate map tiles in `converted`.

`list.py` writes a list of available tiles to `converted.js` as a global variable `available`, which is an object mapping zoom levels to an array of strings (tile names).
