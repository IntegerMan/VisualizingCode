import os


def get_file_list(dir_path, label=None):
    files = list()
    contents = os.listdir(dir_path)

    for entry in contents:
        path = os.path.join(dir_path, entry)
        if os.path.isdir(path):
            lab = label
            if lab is None:
                lab = entry

            # Ignore build and reporting directories
            if not entry.lower() in ['obj', 'ndependout']:
                files = files + get_file_list(path, lab)
        else:
            files.append((path, label))

    return files


def is_source_file(file_label):
    file, label = file_label
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


def get_file_metrics(files):
    results = []

    for file, label in files:
        lines = count_lines(file) # Slow as it actually reads the file
        path, filename = os.path.split(file)
        _, ext = os.path.splitext(filename)

        file_details = {'path': path, 'filename': filename, 'ext': ext, 'lines': lines, 'project': label}
        results.append(file_details)

    return results
