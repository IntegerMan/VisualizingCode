from FileUtilities import get_source_file_metrics

path = 'C:/dev/OpenRA/'
files = get_source_file_metrics(path)

for file in files:
    print(file['filename'] + " has " + str(file['lines']))

print('There are ' + str(len(files)) + ' total source file(s) with ' + str(sum(map(lambda f: f['lines'], files))) + ' total line(s)')