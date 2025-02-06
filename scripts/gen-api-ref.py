"""Generate the code reference pages and navigation."""

from pathlib import Path

import griffe
import mkdocs_gen_files

nav = mkdocs_gen_files.Nav()

root = Path(__file__).parent.parent

data = griffe.load("httpx")

def render_module(module: griffe.Module) -> None:
    if module.name.startswith("_"):
        return

    path = module.path
    parts = tuple(path.split(".")[1:])

    if module.is_init_module:
        doc_path = Path(*parts, "index.md")
    else:
        doc_path = Path(*parts).with_suffix(".md")

    if parts:
        nav[parts] = doc_path.as_posix()

    with mkdocs_gen_files.open(doc_path, "w") as fd:
        fd.write(f"---\ntitle: {path}\n---\n\n# ::: {path}")

    for submodule in module.modules.values():
        render_module(submodule)

    # mkdocs_gen_files.set_edit_path(full_doc_path, path.relative_to(root))

render_module(data)

if nav._data:
    with mkdocs_gen_files.open("SUMMARY.md", "w") as nav_file:
        nav_file.writelines(nav.build_literate_nav())