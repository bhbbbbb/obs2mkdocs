import re
import logging
from typing import TextIO
from .base import IterBuff, ParsingException

logger = logging.getLogger(__name__)

MATH_BLOCK_WRAP = [r'\$\$', r'\$\$']
LIST_START_PATTERN = r'^\s*[\+\-\*]'

def fix(fiter: IterBuff, fout: TextIO):
    """fix math block format

    1. pymarkdown only accept math block with both blankline at preceding and following lines.
    2. blankline in block is not allowed.

    Args:
        fiter (IterBuff): from the line before opening to the line at closing.
            (opening_line - 1, closing)
        fout (TextIO): _description_

    Raises:
        ParsingException: _description_
    """

    if fiter.lookahead is None:
        return

    if re.search(MATH_BLOCK_WRAP[0], fiter.lookahead) is None:
        return
    
    is_not_list = re.search(LIST_START_PATTERN, fiter.lookahead) is None

    if is_not_list:
        match = re.search(r'^([>\s]*)' + MATH_BLOCK_WRAP[0], fiter.lookahead)
        if match is None:
            raise ParsingException(
                f'Unsupported Format for content "{fiter.lookahead}" at line {fiter.idx + 1}'
            )
    
    indent = match[1] if is_not_list else ''
    blankline = f'{indent}\n'
    blankline_pattern = r'\s*' + indent.strip() + r'\s+$'

    if is_not_list and re.match(blankline_pattern, fiter.cur) is None: # if not blank
        fout.write(blankline)
        logger.info(f'inserted blank line before block at line {fiter.idx}')

    fout.write(fiter.next().cur)
    opening_line = fiter.idx

    # check is not one-line block. e.g. $$equations$$
    if re.search(f'{MATH_BLOCK_WRAP[0]}.*?{MATH_BLOCK_WRAP[1]}', fiter.cur) is None:
    
        # find closing
        while True:
            try:
                ## delete blankline
                if next(fiter).strip() == '':
                    continue
                fout.write(fiter.cur)
                if re.search(MATH_BLOCK_WRAP[1], fiter.cur):
                    break
            except StopIteration:
                raise ParsingException(
                    f'Found opening math block symbol \'{MATH_BLOCK_WRAP[0]}\''
                    f' at line {opening_line}'
                    f' , but closing symbol \'{MATH_BLOCK_WRAP[1]}\' not found until line {fiter.idx}.'
                )

    if (
        is_not_list 
        and (
            fiter.lookahead is None
            or re.match(blankline_pattern, fiter.lookahead) is None
        )
    ):
        fout.write(blankline)
        logger.info(f'inserted blankline after block at line {fiter.idx}')
    
    fix(fiter, fout)
    return

def fix_all(fin: TextIO, fout: TextIO):
    fiter = IterBuff(fin)
    while True:
        try:
            fix(fiter, fout)
            fout.write(fiter.next().cur)
        except StopIteration:
            break
    return
