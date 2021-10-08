import os


def get_file_list(dir_path, project=None, folder=None):
    files = list()
    contents = os.listdir(dir_path)

    for entry in contents:
        path = os.path.join(dir_path, entry)
        if os.path.isdir(path):

            # Grab or set our project and then folder variables
            # These will get set if blank as we drill in. This gives us a cheaper hierarchy
            lab = project
            fold = folder

            if lab is None:
                lab = entry
            elif fold is None:
                fold = entry

            # Ignore build and reporting directories
            if not entry.lower() in ['obj', 'ndependout']:
                files = files + get_file_list(path, lab, fold)
        else:
            files.append((path, project, folder))

    return files


def is_source_file(file_label):
    file, _, _ = file_label
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

    for file, project, folder in files:
        lines = count_lines(file) # Slow as it actually reads the file
        path, filename = os.path.split(file)
        _, ext = os.path.splitext(filename)

        small_path = path.replace(root, '')
        small_path = small_path.replace(project + '\\', '')

        file_details = {'path': small_path, 'fullpath': path, 'filename': filename, 'ext': ext, 'lines': lines, 'project': project, 'folder': folder}
        results.append(file_details)

    return results


def get_source_file_metrics(path):
    source_files = filter(is_source_file, get_file_list(path))
    return get_file_metrics(list(source_files), path)