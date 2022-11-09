import logging
from typing import TextIO
import re
from .base import IterBuff

NAMES = r'(?:note|abstract|summary|tldr|info|todo|tip|hint|important|success|question|help|faq|warning|caution|attention|failure|fail|missing|danger|error|bug|example|quote|cite)'
PAT = r'^(.*?)>\s*\[\!' + f'({NAMES})' +  r'\](-|\+)?(\s+(.*?))?\r?\n'
logger = logging.getLogger(__name__)

def fix(fiter: IterBuff, fout: TextIO, indent: str = '    '):

    if fiter.lookahead is None:
        return
    
    match = re.search(PAT, fiter.lookahead, flags=re.IGNORECASE)
    if match is None:
        return
    
    start_line = fiter.idx + 1
    origin_indent, ad_type, expansion, _, title = match.groups()

    expansion = '!!!' if expansion is None else f'???{expansion}'
    title = f'"{title}"' if title else f'"{ad_type}"'

    content_to_write = f'{origin_indent}{expansion} {ad_type} {title}\n'

    while True:

        fiter.next()
        fout.write(content_to_write)

        if fiter.lookahead is None or re.search(r'^\s*>\s*', fiter.lookahead) is None:
            break

        content = re.sub(r'> {0,3}', '', fiter.lookahead)
        content_to_write = f'{origin_indent}{indent}{content}'

    logger.info(f'converted admonition format from line {start_line} to {fiter.idx}')
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
