from typing import List
import os
from io import StringIO
import re

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

COMMENT_PAT = r'^\s*(#.*)?$'
def convert_dir(in_dir: str, out_dir: str, ignore_path: str = '.mdignore'):

    assert os.path.isdir(in_dir)

    ignore_names: List[str] = []

    if not os.path.isfile(ignore_path):
        _convert_dir(in_dir, out_dir, ignore_names)
        return

    with open(ignore_path, mode='r', encoding='utf8') as fin:
        ignore_names = [line.strip() for line in fin if re.match(COMMENT_PAT, line) is None]

    print(ignore_names)
    _convert_dir(in_dir, out_dir, ignore_names)
    return

def _convert_dir(in_dir: str, out_dir: str, ignore_patterns: List[str]):
    os.makedirs(out_dir, exist_ok=True)

    for a_dir in os.listdir(in_dir):
        is_ignore = False
        for pat in ignore_patterns:
            if re.match(pat, a_dir, flags=re.IGNORECASE):
                is_ignore = True
                break
        
        if is_ignore:
            continue

        path = os.path.join(in_dir, a_dir)
        if os.path.isdir(path):
            _convert_dir(path, os.path.join(out_dir, a_dir), ignore_patterns)
        elif os.path.splitext(a_dir)[1] == '.md':
            print(f'fixing {path}')
            convert(path, os.path.join(out_dir, a_dir))
        