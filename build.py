"""Build hello.fs for the Tang Nano 9K and write the directory that `fabricgate push` takes.

Run with: uv run build.py   (needs only uv; the tools are fetched at the pinned versions)
Output:   dist/fabricgate-index.yaml, dist/tangnano9k/programmer/{manifest.yaml,hello.fs}
"""
import hashlib
import shutil
import subprocess
from pathlib import Path

VERSION = "1.0.0"
YOSYS = "yowasp-yosys==0.70.0.0.post1259"
NEXTPNR = "yowasp-nextpnr-himbaechel-gowin==0.11.1.0.post826"
APYCULA = "apycula==0.32"

ROOT = Path(__file__).parent
OUT = ROOT / "dist" / "tangnano9k" / "programmer"
WORK = ROOT / "build"


def run(pkg: str, *cmd: str) -> None:
    subprocess.run(["uvx", "--from", pkg, *cmd], cwd=WORK, check=True)


def main() -> None:
    shutil.rmtree(ROOT / "dist", ignore_errors=True)
    shutil.rmtree(WORK, ignore_errors=True)
    OUT.mkdir(parents=True)
    WORK.mkdir()
    # The WASM tools see only the working directory reliably, so the inputs are copied in.
    for name in ("hello.v", "tangnano9k.cst"):
        shutil.copyfile(ROOT / name, WORK / name)

    run(YOSYS, "yowasp-yosys", "-q", "-p", "read_verilog hello.v; synth_gowin -top top -json synth.json")
    run(NEXTPNR, "yowasp-nextpnr-himbaechel-gowin", "--json", "synth.json", "--write", "pnr.json",
        "--device", "GW1NR-LV9QN88PC6/I5", "--vopt", "family=GW1N-9C", "--vopt", "cst=tangnano9k.cst", "--seed", "1", "--quiet")
    run(APYCULA, "gowin_pack", "-d", "GW1N-9C", "-c", "-o", "hello.fs", "pnr.json")

    # Apicula writes text; LF line ends keep the digest the same on every OS.
    fs = (WORK / "hello.fs").read_bytes().replace(b"\r\n", b"\n")
    (OUT / "hello.fs").write_bytes(fs)

    manifest = f"""\
schema: fabricgate-platform/v1
runtime: programmer
board: tangnano9k
device_family: gw1n-9c
design_ref: fabricgate/hello:{VERSION}
artifacts:
  bitstream:
    file: hello.fs
    sha256: {hashlib.sha256(fs).hexdigest()}
design_portability: board-specific
tool_requirements:
  - tool: yosys
    min_version: "0.70"
  - tool: nextpnr-himbaechel-gowin
    min_version: "0.11.1"
  - tool: apicula
    min_version: "0.32"
""".encode()
    (OUT / "manifest.yaml").write_bytes(manifest)

    index = f"""\
schema: fabricgate-index/v1
name: fabricgate/hello
version: {VERSION}
summary: Hello FabricGate! — minimal reference design (LED counter on the Tang Nano 9K)
license: MIT
author: FabricGate Project
repository: https://github.com/harurun78/fabricgate-hello
tags:
  - reference
  - hello
  - getting-started
platforms:
  - platform: tangnano9k/programmer
    digest: sha256:{hashlib.sha256(manifest).hexdigest()}
"""
    (ROOT / "dist" / "fabricgate-index.yaml").write_text(index, encoding="utf-8", newline="\n")
    print(f"hello.fs sha256 {hashlib.sha256(fs).hexdigest()}")


if __name__ == "__main__":
    main()
