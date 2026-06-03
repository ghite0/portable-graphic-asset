# PGA
Portable Graphic Asset (PGA) is an open-source, human readable image format, primarily for games.
PGA files contain the image data, the position, and name of the asset. They also support transparency.
Yes, you can edit .pga files directly from a text editor!

# Documentation
When writing a PGA file, you must define the name of the asset, the author, and the coordinates. This is called the 'header'.
After the header, you must define the actual sprite. Keep in mind the sprite is 10x10. See an example in the 'examples' folder.

# Decoder
In this repo, there is a file named pga-decoder.py it is meant to be ran in terminal, and displays whatever PGA file is selected. You may use his python file to decode the assets in your project that uses PGA.
