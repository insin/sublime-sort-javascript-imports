import itertools
import re

js_module_re = re.compile(r"""(?:^import\s+|\s+from\s+|require\(\s*)['"]([^'"]+)""")
module_weight_re = re.compile(r'^(\./)?((?:\.\./)*)')
whitespace_re = re.compile(r'^\s*$')

def is_blank(line):
    """Determines if a selected line consists entirely of whitespace."""
    return whitespace_re.match(line) is not None

def is_import(line):
    """Determines if a selected line contains an import statement."""
    return js_module_re.search(line) is not None

def module_sort_key(line):
    """
    Extracts the module name from a JavaScript import line and returns a tuple
    with a sorting weight and the module name/path as a sort key.

    The following import styles are supported:

    - ``import 'example'`` at the start of a line
    - ``...from 'example'`` anywhere in a line
    - ``...require('example')`` anywhere in a line

    The following sorting weights are assigned:

    - imports without any path prefixes: ``float('-inf')`` (sort to top)
    - imports starting with ``../``: ``-n`` where ``n`` is the the number of
       directories ascended (sort furthest to closest)
    - imports starting with ``./``: 0 (sort to bottom)
    """
    module_name = js_module_re.search(line).group(1)
    local_import, ascend_path = module_weight_re.match(module_name).groups()
    module_weight = float('-inf')
    if local_import:
        module_weight = 0
    elif ascend_path:
        module_weight = -ascend_path.count('/')
    return module_weight, module_name

def sort_js_imports(lines):
    """
    Sorts JavaScript import lines by module name, respecting blank lines which
    are in place to separate groups of imports.
    """
    sorted_lines = []
    non_imports = []

    for blank_lines, group in itertools.groupby(lines, key=is_blank):
        if blank_lines:
            # Normalise gaps between groups of imports to a single blank line
            if not sorted_lines or sorted_lines[-1] != '':
                sorted_lines.append('')
        else:
            lines = list(group)

            # Kick any non-import lines down to the end of the selected region
            non_import_indices = [i for i, line in enumerate(lines) if not is_import(line)]
            if non_import_indices:
                non_imports.extend(reversed([lines.pop(i) for i in reversed(non_import_indices)]))

            sorted_lines.extend(sorted(lines, key=module_sort_key))

    # Add an extra blank line if there were non-imports in the selection
    if non_imports and sorted_lines and sorted_lines[-1] != '':
        sorted_lines.append('')

    return sorted_lines + non_imports
