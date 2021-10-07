from FileUtilities import getListOfFiles, isSourceFile, count_lines, getFileMetrics

path = 'M:/dev/CodeVis/OpenRA/'

allFiles = getListOfFiles(path)
sourceFiles = list(filter(isSourceFile, allFiles))

files = getFileMetrics(sourceFiles)

for file in files:
    print(file['name'] + " has " + str(file['lines']))

print('There are ' + str(len(sourceFiles)) + ' total source file(s) with ' + str(sum(map(lambda f: f['lines'], files))) + ' total line(s)')