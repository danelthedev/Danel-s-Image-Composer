import ImageComposer as ic
import tkinter as tk
from tkinter import filedialog
from time import sleep

class ImageType:
    BIGFILE = 0
    SMALLFILE = 1
    OUTPUTFILE = 2

#browse function
def browse_file(file_type: ImageType):

    if file_type != ImageType.OUTPUTFILE:
        filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select a File")
    else:
        filename = filedialog.askdirectory(initialdir="/",
                                              title="Select a Directory")

    if file_type == ImageType.BIGFILE:
        bigFilePath['text'] = filename
    elif file_type == ImageType.SMALLFILE:
        smallFilePath['text'] = filename
    elif file_type == ImageType.OUTPUTFILE:
        outputFilePath['text'] = filename + "/output.png"

#validation function for entries
def validate(P):
    if len(P) == 0:
        return True
    elif len(P) < 5 and P.isnumeric():
        return True
    else:
        return False

def createComposition(bigPath, bigW, bigH, smallPath, smallW, smallH, outputPath, transparency):
    if bigPath == "" or smallPath == "" or outputPath == "" or bigW == "" or bigH == "" or smallW == "" or smallH == "":
        resultLabel['text'] = "Please fill in all fields"
        return False
    elif not(bigPath.lower().endswith(".png") or bigPath.lower().endswith(".jpg") or bigPath.lower().endswith(".jpeg"))\
            or not(smallPath.lower().endswith(".png") or smallPath.lower().endswith(".jpg") or smallPath.lower().endswith(".jpeg")):
        resultLabel['text'] = "Please select a valid image"
        return False
    else:
        composer = ic.ImageComposer()
        composer.setBigImg(bigPath, int(bigW), int(bigH))
        composer.setSmallImg(smallPath, int(smallW), int(smallH))
        if int(transparency) == 1:
            composer.makeCompositeWithTransparency()
        else:
            composer.makeComposite()

        composer.save(outputPath)
        resultLabel['text'] = "Completed!"
        return True



if __name__ == "__main__":

    #create a window
    root = tk.Tk()
    root.resizable(False, False)
    root.title("Image Composer")

    #entry limitations
    vcmd = (root.register(validate), '%P')

    #Big image path
    bigLabel = tk.Label(root, text="Big Image: ", font=("Arial", 10), height=2, width=10)
    bigLabel.grid(row=0, column=0, padx=2, pady=5, sticky=tk.W)

    browseBigFileButton = tk.Button(root, text="Browse", command=lambda: browse_file(ImageType.BIGFILE), height=2, width=10)
    browseBigFileButton.grid(row=0, column=1, padx=2, pady=5, sticky=tk.W)

    bigFilePath = tk.Label(root, text=" ", font=("Arial", 10), height=1, borderwidth=1, relief="solid")
    bigFilePath.grid(row=0, column=2, padx=3, pady=5, sticky=tk.E, columnspan=3)

    #Small image path
    bigLabel = tk.Label(root, text="Small Image: ", font=("Arial", 10), height=2, width=10)
    bigLabel.grid(row=1, column=0, padx=2, pady=5, sticky=tk.W)

    browseSmallFileButton = tk.Button(root, text="Browse", command=lambda: browse_file(ImageType.SMALLFILE), height=2, width=10)
    browseSmallFileButton.grid(row=1, column=1, padx=2, pady=5, sticky=tk.W)

    smallFilePath = tk.Label(root, text=" ", font=("Arial", 10), height=1, borderwidth=1, relief="solid")
    smallFilePath.grid(row=1, column=2, padx=3, pady=5, sticky=tk.W, columnspan=3)

    #Output image path
    outputLabel = tk.Label(root, text="Output Folder: ", font=("Arial", 10), height=2, width=10)
    outputLabel.grid(row=2, column=0, padx=2, pady=5, sticky=tk.W)

    browseOutputFileButton = tk.Button(root, text="Browse", command=lambda: browse_file(ImageType.OUTPUTFILE), height=2, width=10)
    browseOutputFileButton.grid(row=2, column=1, padx=2, pady=5, sticky=tk.W)

    outputFilePath = tk.Label(root, text=" ", font=("Arial", 10), height=1, borderwidth=1, relief="solid")
    outputFilePath.grid(row=2, column=2, padx=3, pady=5, sticky=tk.W, columnspan=3)


    #Custom size for the big and small images with text fields

    bigWidthLabel = tk.Label(root, text="Width of big file: ", font=("Arial", 10), height=2, width=12)
    bigWidthLabel.grid(row=3, column=0, padx=2, pady=5, sticky=tk.W)

    bigWidth = tk.Entry(root, width=10, validate="key", validatecommand=vcmd)
    bigWidth.grid(row=3, column=1, padx=2, pady=5, sticky=tk.W)

    bigHeightLabel = tk.Label(root, text="Height of big file: ", font=("Arial", 10), height=2, width=12)
    bigHeightLabel.grid(row=4, column=0, padx=2, pady=5, sticky=tk.W)

    bigHeight = tk.Entry(root, width=10, validate="key", validatecommand=vcmd)
    bigHeight.grid(row=4, column=1, padx=2, pady=5, sticky=tk.W)


    smallWidthLabel = tk.Label(root, text="Width of small file: ", font=("Arial", 10), height=2, width=14)
    smallWidthLabel.grid(row=5, column=0, padx=2, pady=5, sticky=tk.W)

    smallWidth = tk.Entry(root, width=10, validate="key", validatecommand=vcmd)
    smallWidth.grid(row=5, column=1, padx=2, pady=5, sticky=tk.W)

    smallHeightLabel = tk.Label(root, text="Height of small file: ", font=("Arial", 10), height=2, width=14)
    smallHeightLabel.grid(row=6, column=0, padx=2, pady=5, sticky=tk.W)

    smallHeight = tk.Entry(root, width=10, validate="key", validatecommand=vcmd)
    smallHeight.grid(row=6, column=1, padx=2, pady=5, sticky=tk.W)

    #Transparency checkbox
    var = tk.IntVar()
    transparency = tk.Checkbutton(root, text="Transparency", font=("Arial", 10), height=2, width=12, variable=var)
    transparency.grid(row=7, column=0, padx=2, pady=5, sticky=tk.W)

    #Apply button
    applyButton = tk.Button(root, text="Apply", height=2, width=8, command=lambda: createComposition(bigFilePath.cget("text"), bigWidth.get(), bigHeight.get(),
                                                                                                     smallFilePath.cget("text"), smallWidth.get(), smallHeight.get(),
                                                                                                     outputFilePath.cget("text"), var.get()))
    applyButton.grid(row=8, column=0, padx=2, pady=5, sticky=tk.W)

    #Result label
    resultLabel = tk.Label(root, text="", font=("Arial", 10), height=2, width=19)
    resultLabel.grid(row=8, column=1, padx=2, pady=5, sticky=tk.W)

    #run the main loop
    root.mainloop()