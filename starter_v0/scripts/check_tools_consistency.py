import re
from pathlib import Path
import sys
import yaml

root = Path(__file__).resolve().parents[1]
tools_yaml = root / "artifacts" / "tools.yaml"
tools_init = root / "tools" / "__init__.py"

declared = [item.get("name") for item in yaml.safe_load(tools_yaml.read_text(encoding="utf-8"))["tools"]]
content = tools_init.read_text(encoding="utf-8")
keys = re.findall(r"\"([a-zA-Z0-9_]+)\"\s*:\s*[a-zA-Z0-9_\.]+,", content)

declared_set = set(declared)
keys_set = set(keys)

ok = True
only_declared = declared_set - keys_set
only_keys = keys_set - declared_set
if only_declared:
    print("Missing implementations for:", ", ".join(sorted(only_declared)))
    ok = False
if only_keys:
    print("Declared implementations not in tools.yaml:", ", ".join(sorted(only_keys)))
    ok = False
if ok:
    print("OK: artifacts/tools.yaml and tools/__init__.py are consistent (names match).")
    sys.exit(0)
else:
    sys.exit(2)
