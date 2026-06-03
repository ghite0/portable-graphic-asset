# PGA
Portable Graphic Asset (PGA) is an open-source, human readable image format, primarily for games.
PGA files contain the image data, the position, and name of the asset. They also support transparency.
Yes, you can edit .pga files directly from a text editor!

# Documentation
When writing a PGA file, you must define the name of the asset, the author, and the coordinates.
For example, this is how the 'header' of a PGA file looks:

Name: Example
Author: John Doe
X: 0
Y: 0
Pixels:

After the header, you must define the actual sprite. Keep in mind the sprite is 10x10. see an example in the 'examples' folder.
