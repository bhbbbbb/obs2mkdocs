import logging
from io import StringIO

from .base import IterBuff
from .math_block import fix_all as math_block_fix_all
from .admination import fix_all as admination_fix_all

logger = logging.getLogger(__name__)


def fix(in_path: str, out_path: str):
    with open(in_path, encoding='utf8', mode='r') as fin,\
        StringIO(newline='') as sio,\
        open(out_path, encoding='utf8', mode='w') as fout:

        admination_fix_all(fin, sio)
        
        sio.seek(0)
        
        math_block_fix_all(sio, fout)

    return
        