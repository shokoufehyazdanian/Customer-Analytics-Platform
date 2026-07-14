from pathlib import Path

import great_expectations as gx

gx_path = Path.cwd() / "gx"

context = gx.get_context(mode="file", context_root_dir=gx_path)

print(context)
