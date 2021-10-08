import os


def get_file_list(dir_path, paths=None):
    files = list()
    contents = os.listdir(dir_path)

    for entry in contents:
        path = os.path.join(dir_path, entry)
        if os.path.isdir(path):
            # Ignore build and reporting directories
            if entry.lower() in ['obj', 'ndependout']:
                continue

            # Maintain an accurate, but separate, hierarchy array
            if paths is None:
                p = [entry]
            else:
                p = paths[:]
                p.append(entry)

            files = files + get_file_list(path, p)
        else:
            files.append((path, paths))

    return files


def is_source_file(file_label):
    file, _ = file_label
    name, ext = os.path.splitext(file)
    ext = ext.lower()
    return ext in ['.cs', '.r', '.agc', '.fs', '.js']


def count_lines(path):
    def _make_gen(reader):
        b = reader(2 ** 16)
        while b:
            yield b
            b = reader(2 ** 16)

    with open(path, "rb") as f:
        count = sum(buf.count(b"\n") for buf in _make_gen(f.raw.read))
    return count


def get_file_metrics(files, root):
    results = []

    for file, folders in files:
        lines = count_lines(file) # Slow as it actually reads the file
        path, filename = os.path.split(file)
        _, ext = os.path.splitext(filename)

        fullpath = ''

        if len(folders) > 0:
            project = folders[0]
            for folder in folders[1:]:
                if len(fullpath) > 0:
                    fullpath += '/'
                fullpath += folder
        else:
            project = ''

        if len(fullpath) <= 0:
            fullpath = '.'

        id = project + '/' + fullpath + '/' + filename

        file_details = {
                        'fullpath': id,
                        'project': project,
                        'path': fullpath,
                        'filename': filename,
                        'ext': ext,
                        'lines': lines,
                        }
        results.append(file_details)

    return results


def get_source_file_metrics(path):
    source_files = filter(is_source_file, get_file_list(path))
    return get_file_metrics(list(source_files), path)
