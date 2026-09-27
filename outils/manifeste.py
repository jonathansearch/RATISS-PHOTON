#!/usr/bin/env python3
"""MANIFESTE — sceau SHA-256 de RATISS-PHOTON (même protocole que RATISS-ETALONS).

python3 outils/manifeste.py             # scelle (écrit MANIFESTE.json)
python3 outils/manifeste.py --verifier  # vérifie le sceau
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import sys

RACINE = pathlib.Path(__file__).resolve().parent.parent
EXCLUS = {".git", "__pycache__"}


def empreintes():
    fichiers = {}
    for p in sorted(RACINE.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(RACINE)
        if any(part in EXCLUS for part in rel.parts):
            continue
        if rel.name == "MANIFESTE.json":
            continue
        fichiers[str(rel)] = hashlib.sha256(p.read_bytes()).hexdigest()
    return fichiers


def main():
    if "--verifier" in sys.argv:
        m = json.load(open(RACINE / "MANIFESTE.json", encoding="utf-8"))
        actuels = empreintes()
        manquants = [k for k in m["fichiers"] if k not in actuels]
        modifies = [k for k in m["fichiers"] if k in actuels and actuels[k] != m["fichiers"][k]]
        nouveaux = [k for k in actuels if k not in m["fichiers"]]
        ok = len(m["fichiers"]) - len(manquants) - len(modifies)
        print(f"{ok}/{len(m['fichiers'])} conformes · {len(manquants)} manquants · "
              f"{len(modifies)} modifies · {len(nouveaux)} nouveaux (non scelles)")
        sys.exit(1 if (manquants or modifies) else 0)
    fichiers = empreintes()
    with open(RACINE / "MANIFESTE.json", "w", encoding="utf-8") as f:
        json.dump({"algorithme": "sha256", "fichiers": fichiers}, f, indent=2, ensure_ascii=False)
    print(f"{len(fichiers)} fichiers scelles -> MANIFESTE.json")


if __name__ == "__main__":
    main()
