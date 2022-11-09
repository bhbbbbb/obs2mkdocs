Convert obsidian-type markdown to mkdocs-accepted markdown.

1. Block Math

```md
## Before Converted. OK in obsidian, illegal according to python-markdown

line before
$$a = b + c$$
line after

## After converted.

line before

$$a = b + c$$

line after
```

2. Admonition

convert obsidian's [callouts](https://help.obsidian.md/How+to/Use+callouts) to admontion format.

## Getting Started

### Installation

```sh
pip install git+https://github.com/bhbbbbb/obs2mkdocs
```

### Basic Usage

```python
from obs2mkdocs import export_dir

export_dir(
    src_dir,
    dest_dir,
    ignore_path = '.mdignore',
    attachments_dirname: str = None,
)
```

- `export_dir` convert every markdown file in `src_dir` **deeply** and output to the corresponding dir in `dest_dir`.

- the `.mdignore` is similar to `.gitignore` but work only with python's regex

```sh
# ignore file or dir
ignore\.md
.*?ignore.*?

# '/' and '\\' is equivalent
a/b
c\\d
```

- `attachments_dirname` can be specified to copy the attachments folder in every `src_dir` to the corresponding `dest_dir`. See [obsidian-consistent-attachments-and-links](https://github.com/dy-sh/obsidian-consistent-attachments-and-links) for attachments management.