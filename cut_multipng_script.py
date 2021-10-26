import png
import os
from pathlib import Path
from shutil import copyfile

# Color to cut
CUT_COLOR = (0,0,0,0)

# Get base directory
basePath = Path(os.getcwd()).resolve()

# outout directory
outputPath = Path(basePath.__str__()+"/output").resolve()

# create one if /output doesn´t exist
outputPath.mkdir(parents=True,exist_ok=True)

# list of PNG files
FILES = list(basePath.glob("*.png"))


# Write new PNG file in /output
def writeFile(newImage,FILE):
    openFile = open(Path(outputPath.__str__()+"/"+FILE.name.__str__()).resolve(),"wb+")
    png.Writer(newImage[0],newImage[1],alpha=True,greyscale=False).write(openFile,newImage[2])


# Cut image -> return pixels
def getPixels(pixels) -> tuple():
    i,j,newImage = 0,0,[]

    while j < h:
        pixelRow = tuple(next(pixels))
        if pixelRow[0:4] == CUT_COLOR: break
        while i < w:
            if pixelRow[i*4:(i+1)*4] == CUT_COLOR: break
            i+=1
        newImage.append(pixelRow[0:i*4])
        j+=1
    if (i,j) == (0,0): raise png.ProtocolError()
    return (i,j,newImage)


# Get every PNG files binaries in base path and proceed to cut em
for FILE in FILES:
    try:
        w, h, pixels, metadata = png.Reader(file=FILE.open("rb")).asRGBA()
        writeFile(getPixels(pixels),FILE)
        print("Name: "+FILE.name, "Status: Complete", sep='\t\t')
    except png.ChunkError:
        print("Name: "+FILE.name, "Status: Error", sep='\t\t')
    # if CUT_COLOT is in (0,0), copy original png to output
    except png.ProtocolError:
        copyfile(FILE, Path(outputPath.__str__()+"/"+FILE.name.__str__()).resolve())
        print("Name: "+FILE.name, "Status: Keep Same", sep='\t\t')