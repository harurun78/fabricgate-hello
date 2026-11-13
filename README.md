# fabricgate-hello

Source of the reference design `fabricgate/hello` on [FabricGate](https://fabricgate.dev).
It is the smallest design that shows a pull working end to end: after you write it to the
board, the six on-board LEDs count up in binary, about one step every 0.6 seconds.

| Version | Platform | Board |
| --- | --- | --- |
| 1.0.0 | `tangnano9k/programmer` | Sipeed Tang Nano 9K (GW1NR-9C) |

## Use it

```sh
pip install fabricgate
fabricgate pull fabricgate/hello:1.0.0 --platform tangnano9k/programmer
openFPGALoader -b tangnano9k hello.fs        # into SRAM; gone after a power cycle
openFPGALoader -b tangnano9k -f hello.fs     # into flash; stays
```

`pull` prints where it saved `hello.fs`. FabricGate does not write to the board; any tool that
takes a Gowin `.fs` file works (openFPGALoader, Gowin Programmer).

## Build it yourself

You need only [uv](https://docs.astral.sh/uv/). The build uses open tools at pinned versions
(Yosys, nextpnr-himbaechel-gowin and Apicula) and downloads them on first run.

```sh
uv run build.py
```

This writes `dist/`, the directory that `fabricgate push dist` takes. The same sources and tool
versions give the same `hello.fs` byte for byte, so its sha256 should match the published one.

## Clean-license checklist

Checked before each publish:

1. No vendor board files and no vendor tools: the build uses open-source tools only.
2. No vendor IP cores: the design is the plain Verilog in `hello.v`.
3. No third-party IP and nothing that cannot be redistributed.

## Release checklist

- [ ] `uv run build.py` gives the same sha256 on a second machine
- [ ] Written to a real Tang Nano 9K; the LEDs count
- [ ] `fabricgate push dist` to the `fabricgate` namespace
- [ ] From a clean environment, the commands under "Use it" work

## License

MIT. See `LICENSE`.
