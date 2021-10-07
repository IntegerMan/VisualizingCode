import os

def getListOfFiles(dirName):
    # create a list of file and sub directories
    # names in the given directory
    listOfFile = os.listdir(dirName)
    allFiles = list()

    print(dirName)
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath):
            # Ignore build directories
            if not entry.lower() in ['obj']:
                allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)

    return allFiles

def isSourceFile(file):
    name, ext = os.path.splitext(file)
    ext = ext.lower()
    return ext in ['.cs','.r','.agc','.fs','.js']

def count_lines(path):
    def _make_gen(reader):
        b = reader(2 ** 16)
        while b:
            yield b
            b = reader(2 ** 16)

    with open(path, "rb") as f:
        count = sum(buf.count(b"\n") for buf in _make_gen(f.raw.read))
    return count

def getFileMetrics(sourceFiles):
    files = []

    for file in sourceFiles:
        file_lines = count_lines(file)
        file_details = {'name': file, 'lines': file_lines}
        files.append(file_details)

    return files