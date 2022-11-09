from typing import List
import os
from io import StringIO
import re
import shutil

from .math_block import fix_all as math_block_fix_all
from .admination import fix_all as admination_fix_all


def convert(in_path: str, out_path: str):
    with open(in_path, encoding='utf8', mode='r') as fin,\
        StringIO(newline='') as sio,\
        open(out_path, encoding='utf8', mode='w') as fout:

        admination_fix_all(fin, sio)
        
        sio.seek(0)
        
        math_block_fix_all(sio, fout)
    return

class PathPattern:

    def __init__(self, origin: str):
        def split(string: str):
            for a in string.split('\\\\'):
                for b in a.split('/'):
                    yield b
        self.pats = list(reversed(list(split(origin))))
        return
    
    def match(self, path: str):
        dirname = path
        for pat in self.pats:
            basename = os.path.basename(dirname)
            if re.match(pat, basename, flags=re.IGNORECASE) is None:
                return False
            dirname = os.path.dirname(dirname)
        return True


COMMENT_PAT = r'^\s*(#.*)?$'
def export_dir(
    in_dir: str,
    out_dir: str,
    ignore_path: str = '.mdignore',
    attachments_dirname: str = None
):
    """TODO

    Args:
        in_dir (str): _description_
        out_dir (str): _description_
        ignore_path (str, optional): _description_. Defaults to '.mdignore'.
        attachments_dirname (str, optional): _description_. Defaults to None.
    """

    assert os.path.isdir(in_dir)

    ignore_names: List[PathPattern] = []

    if not os.path.isfile(ignore_path):
        _export_dir(in_dir, out_dir, ignore_names)
        return

    with open(ignore_path, mode='r', encoding='utf8') as fin:
        ignore_names = [
            PathPattern(line.strip()) for line in fin if re.match(COMMENT_PAT, line) is None
        ]

    _export_dir(in_dir, out_dir, ignore_names, attachments_dirname)
    return

def _export_dir(
    in_dir: str,
    out_dir: str,
    ignore_patterns: List[PathPattern],
    attachments_dirname: str = None,
):
    os.makedirs(out_dir, exist_ok=True)

    if (
        attachments_dirname is not None
        and os.path.isdir(in_attch := os.path.join(in_dir, attachments_dirname))
    ):
        shutil.copytree(in_attch, os.path.join(out_dir, attachments_dirname), dirs_exist_ok=True)
        

    for a_dir in os.listdir(in_dir):
        is_ignore = False
        path = os.path.join(in_dir, a_dir)
        for pat in ignore_patterns:
            if pat.match(path):
                is_ignore = True
                break
        
        if is_ignore:
            continue

        if os.path.isdir(path):
            _export_dir(path, os.path.join(out_dir, a_dir), ignore_patterns, attachments_dirname)
        elif os.path.splitext(a_dir)[1] == '.md':
            print(f'fixing {path}')
            convert(path, os.path.join(out_dir, a_dir))
        