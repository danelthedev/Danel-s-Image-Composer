from PIL import Image
import threading as td


# TODO: PASTE OPTIMIZATION
# TODO: FIX JPG ISSUES

class ImageComposer:

    # initialize the class with the two images and size them correctly
    def __init__(self, pathToBigImg="", pathToSmallImg="", bigImgWidth=0, bigImgHeight=0, smallImgWidth=0,
                 smallImgHeight=0):
        if pathToBigImg == "" or pathToSmallImg == "":
            self.bigImg = None
            self.smallImg = None
        else:
            self.bigImg = self.getImgFromPath(pathToBigImg)
            self.smallImg = self.getImgFromPath(pathToSmallImg)

            # custom image sizes
            if bigImgWidth != 0 and bigImgHeight != 0 and smallImgWidth != 0 and smallImgHeight != 0:
                self.bigImg = self.scale(self.bigImg, bigImgWidth, bigImgHeight)
                self.smallImg = self.scale(self.smallImg, smallImgWidth, smallImgHeight)
            # default image sizes
            else:
                self.bigImg = self.scale(self.bigImg, 32, 32)
                self.smallImg = self.scale(self.smallImg, 32, 32)

        self.result = None
        self.coloredImages = {}

    # function that sets the big image
    def setBigImg(self, path, bigImgWidth=0, bigImgHeight=0):
        self.bigImg = self.getImgFromPath(path)
        if bigImgWidth != 0 and bigImgHeight != 0:
            self.bigImg = self.scale(self.bigImg, bigImgWidth, bigImgHeight)
        else:
            self.bigImg = self.scale(self.bigImg, 32, 32)

    # function that sets the small image
    def setSmallImg(self, path, smallImgWidth=0, smallImgHeight=0):
        self.smallImg = self.getImgFromPath(path)
        if smallImgWidth != 0 and smallImgHeight != 0:
            self.smallImg = self.scale(self.smallImg, smallImgWidth, smallImgHeight)
        else:
            self.smallImg = self.scale(self.smallImg, 32, 32)

    # function that takes a path and returns an image object
    def getImgFromPath(self, path):
        im = Image.open(path)
        return im

    # function that takes a picture and scales it down to a target resolution
    def scale(self, im, target_width, target_height):
        im = im.resize((target_width, target_height))
        return im

    # function that returns a grayscale image
    def grayscale(self, im):
        # instantiate a new image
        newImg = Image.new('RGBA', im.size)
        # loop through the image and convert each pixel to grayscale
        for x in range(im.size[0]):
            for y in range(im.size[1]):
                r, g, b = im.getpixel((x, y))[:3]
                # convert to grayscale
                gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
                # set the pixel color
                newImg.putpixel((x, y), (gray, gray, gray))
        return newImg

    # function that overlays a grayscale image using a given color
    def overlayColor(self, im, r, g, b):
        #daca nu avem imaginea salvata deja, o facem
        if self.coloredImages.get((r, g, b)) is None:
            # the grayscale of the image
            grayImg = self.grayscale(im)
            # instantiate a new image
            newImg = Image.new('RGBA', im.size)
            # loop through the image and overlay the color
            for x in range(im.size[0]):
                for y in range(im.size[1]):
                    # get the pixel color of the grayscale
                    data = grayImg.getpixel((x, y))[:3]
                    r2 = data[0]
                    g2 = data[1]
                    b2 = data[2]
                    # get the pixel color of the original image
                    a = im.getpixel((x, y))[3]
                    #set the pixel color
                    newImg.putpixel((x, y), (int(r / 2 + r2 / 2), int(g / 2 + g2 / 2), int(b / 2 + b2 / 2), a))

            #salvam imaginea
            self.coloredImages[(r, g, b)] = newImg
            #returnam imaginea
            return self.coloredImages[(r, g, b)]
        else:
            return self.coloredImages[(r, g, b)]


    #function to process a line of the image
    def processLine(self, x):
        for y in range(self.bigImg.size[1]):
            r, g, b, a = self.bigImg.getpixel((x, y))
            # create the overlayed image
            tmpImg = self.overlayColor(self.smallImg, r, g, b)
            self.resultLines[x].append([tmpImg, a])


    # function that makes a collage from a big image using a smaller image, that is color overlayed
    def makeCompositeWithTransparency(self):

        processes = []
        self.resultLines = [[] for _ in range(self.bigImg.size[0])]
        # instantiate a new image
        newImg = Image.new('RGBA', (self.bigImg.size[0] * self.smallImg.size[0], self.bigImg.size[1] * self.smallImg.size[1]))

        print(len(self.resultLines))
        #create a thread for each line
        for x in range(self.bigImg.size[0]):
            processes.append(td.Thread(target=self.processLine, args=(x,)))
            processes[x].start()

        #wait for all threads to finish
        for x in range(self.bigImg.size[0]):
            processes[x].join()

        #loop through the lines and add them to the new image
        for x in range(self.bigImg.size[0]):
            for y in range(self.bigImg.size[1]):
                if self.resultLines[x][y][1] > 240:
                    newImg.paste(self.resultLines[x][y][0], (x * self.smallImg.size[0], y * self.smallImg.size[1]))

        self.result = newImg


    # function that makes a collage from a big image using a smaller image, that is color overlayed but without transparency
    def makeComposite(self):
        processes = []
        self.resultLines = [[] for _ in range(self.bigImg.size[0])]
        # instantiate a new image
        newImg = Image.new('RGBA', (self.bigImg.size[0] * self.smallImg.size[0], self.bigImg.size[1] * self.smallImg.size[1]))

        print(len(self.resultLines))
        #create a thread for each line
        for x in range(self.bigImg.size[0]):
            processes.append(td.Thread(target=self.processLine, args=(x,)))
            processes[x].start()

        #wait for all threads to finish
        for x in range(self.bigImg.size[0]):
            processes[x].join()

        #loop through the lines and add them to the new image
        for x in range(self.bigImg.size[0]):
            for y in range(self.bigImg.size[1]):
                newImg.paste(self.resultLines[x][y][0], (x * self.smallImg.size[0], y * self.smallImg.size[1]))



    # function that saves the collage to a file
    def save(self, path):
        if self.result is not None:
            self.result.save(path)
