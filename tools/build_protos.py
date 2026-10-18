"""Compile proto/cloud/*.proto into eufy_omni_cloud/pb/ with relative imports.

Usage: python tools/build_protos.py [--protoc PATH]
The generated modules import each other as `from . import x_pb2`, so the package
can be vendored under custom_components/ without touching sys.path.
"""
from __future__ import annotations

import argparse
import pathlib
import re
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "proto" / "cloud"
OUT = ROOT / "eufy_omni_cloud" / "pb"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--protoc", default=shutil.which("protoc") or "protoc")
    args = ap.parse_args()

    if OUT.exists():
        for p in OUT.glob("*_pb2.py*"):
            p.unlink()
    OUT.mkdir(parents=True, exist_ok=True)
    protos = sorted(SRC.glob("*.proto"))
    cmd = [args.protoc, f"-I{ROOT}", f"--python_out={OUT}", f"--pyi_out={OUT}", *map(str, protos)]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode:
        print(res.stderr, file=sys.stderr)
        return res.returncode
    # protoc mirrors the input path: OUT/proto/cloud/x_pb2.py -> flatten.
    nested = OUT / "proto" / "cloud"
    for gen in nested.glob("*_pb2.py*"):
        text = gen.read_text(encoding="utf-8")
        text = re.sub(r"^from proto\.cloud import (\w+) as", r"from . import \1 as", text, flags=re.M)
        text = re.sub(r"^from proto\.cloud import (\w+)$", r"from . import \1", text, flags=re.M)
        text = re.sub(r"^import proto\.cloud\.(\w+)", r"from . import \1", text, flags=re.M)
        (OUT / gen.name).write_text(text, encoding="utf-8")
    shutil.rmtree(OUT / "proto")
    init = OUT / "__init__.py"
    init.write_text(
        '"""Generated protobuf modules. Source schemas: proto/cloud (see proto/LICENSE-eufy-clean-protos.md)."""\n',
        encoding="utf-8",
    )
    print(f"built {len(list(OUT.glob('*_pb2.py')))} modules into {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
