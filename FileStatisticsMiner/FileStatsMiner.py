from FileUtilities import get_file_list, is_source_file, count_lines, get_file_metrics

path = 'M:/dev/CodeVis/OpenRA/'

allFiles = get_file_list(path)
sourceFiles = list(filter(is_source_file, allFiles))

files = get_file_metrics(sourceFiles)

for file in files:
    print(file['filename'] + " has " + str(file['lines']))

print('There are ' + str(len(sourceFiles)) + ' total source file(s) with ' + str(sum(map(lambda f: f['lines'], files))) + ' total line(s)')