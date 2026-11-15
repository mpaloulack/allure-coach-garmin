#!/usr/bin/env python3
"""Régénère exemples/demo.html à partir du modèle et de exemple-coach.json.
Usage (depuis la racine du dépôt) : python3 -I exemples/build-demo.py
Les dates de l'exemple sont recalées sur la semaine en cours à l'ouverture de la page."""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
WRAP = (ROOT / "exemples" / "demo-shift.js").read_text(encoding="utf-8").strip()
tpl = (ROOT / "kit" / "coach-dashboard-template.html").read_text(encoding="utf-8")
ex = json.loads((ROOT / "exemples" / "exemple-coach.json").read_text(encoding="utf-8"))
data = json.dumps(ex, ensure_ascii=False).replace("</", "<\\/")
marker = "/*COACH_DATA_START*/{}/*COACH_DATA_END*/"
assert tpl.count(marker) == 1, "marqueurs COACH introuvables"
out = tpl.replace(marker, "/*COACH_DATA_START*/" + WRAP + "(" + data + ")/*COACH_DATA_END*/")
out = out.replace("<title>Coach course</title>", "<title>Démo · allure-coach-garmin</title>", 1)
(ROOT / "exemples" / "demo.html").write_text(out, encoding="utf-8")
print("exemples/demo.html régénéré")
