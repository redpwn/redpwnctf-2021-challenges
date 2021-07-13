#!/usr/bin/env python3
from pathlib import Path
from typing import Dict, Iterable, Set
from itertools import chain
from random import randint

import yaml


def find_rcds_challenges(root: Path) -> Iterable[Path]:
    return chain(*(root.rglob("challenge." + e) for e in ["yml", "yaml"]))


used_ports: Dict[int, Set[str]] = dict()


def gen_port() -> int:
    port = next(
        filter(lambda p: p not in used_ports, iter(lambda: randint(31000, 32000), None))
    )
    used_ports[port] = set()
    return port


if __name__ == "__main__":
    for chall in find_rcds_challenges(Path(".")):
        config = yaml.safe_load(chall.read_text())
        if "expose" in config:
            for ei in config["expose"].values():
                for ee in ei:
                    if "tcp" in ee:
                        p = ee["tcp"]
                        used_ports.setdefault(p, set())
                        used_ports[p].add(str(chall))
    for port, chall_set in used_ports.items():
        if len(chall_set) > 1:
            print(f"Port conflict: {port} ({chall_set})")
    print(list(used_ports.keys()))
    while True:
        input()
        print(gen_port())
