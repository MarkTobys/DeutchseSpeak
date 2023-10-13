import os

def getScripts():
    #obtain filepath to Scripts directory
    dir = os.getcwd()
    Scripts = os.path.join(dir, "Scripts")
    #check if the "Scripts" folder exists
    if os.path.exists(Scripts) and os.path.isdir(Scripts):
        #get a list of all the Script folders in Scripts then sort by alphanumeric order
        subdirectories = [d for d in os.listdir(Scripts) if os.path.isdir(os.path.join(Scripts, d))]
        subdirectories.sort()
        scriptFiles = []
        bgFiles = []
        #check if there are any subdirectories,
        for subdir in subdirectories:
            Scripts_path = os.path.join(Scripts, subdir)
            script = [f for f in os.listdir(Scripts_path) if f.endswith('.txt')]
            background = [f for f in os.listdir(Scripts_path) if f.endswith('.png')]
            #check to see if there is both a png file and txt file, if only one of either or neither, skip import
            if script and background:
                scriptFiles.append(os.path.join(subdir, script[0]).replace(os.path.sep, '/'))  #assuming only one .txt file per folder
                bgFiles.append(os.path.join(subdir, background[0]).replace(os.path.sep, '/'))  #assuming only one .png file per folder
            else:
                scriptFiles.append(None)  # No .txt file found
                bgFiles.append(None)  # No .png file found
        return scriptFiles, bgFiles
    else:
        return None

