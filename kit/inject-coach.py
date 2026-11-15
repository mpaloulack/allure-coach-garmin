#!/usr/bin/env python3
"""Injecte un objet COACH (JSON) dans le modèle du dashboard, sans casser la balise <script>.

Usage : python3 -I kit/inject-coach.py kit/coach-dashboard-template.html coach.json sortie.html "Objectif Foulées du Port"

- `</` devient `<\\/` et U+2028/U+2029 sont échappés : un nom d'activité ou un texte copié du web
  ne peut pas fermer la balise <script> et exécuter du code.
- Vérifie la syntaxe du script final avec node s'il est installé.
"""
import html, json, re, shutil, subprocess, sys, tempfile

START, END = "/*COACH_DATA_START*/", "/*COACH_DATA_END*/"


def main() -> int:
    if len(sys.argv) != 5:
        print(__doc__)
        return 2
    tpl_path, coach_path, out_path, title = sys.argv[1:]
    tpl = open(tpl_path, encoding="utf-8").read()
    coach = json.load(open(coach_path, encoding="utf-8"))
    if not isinstance(coach, dict):
        sys.exit("COACH doit être un objet JSON")
    data = (json.dumps(coach, ensure_ascii=False, separators=(",", ":"))
            .replace("</", "<\\/").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029"))
    if tpl.count(START + "{}" + END) != 1:
        sys.exit("marqueurs COACH introuvables (le modèle a déjà été rempli ?)")
    page = tpl.replace(START + "{}" + END, START + data + END)
    page = page.replace("<title>Coach course</title>", "<title>" + html.escape(title[:60]) + "</title>", 1)
    if shutil.which("node"):
        js = re.findall(r"<script>([\s\S]*?)</script>", page)[-1]
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
            f.write(js)
        r = subprocess.run(["node", "-e", "new Function(require('fs').readFileSync(process.argv[1],'utf8'))", f.name],
                           capture_output=True, text=True)
        if r.returncode:
            sys.exit("erreur de syntaxe dans le script :\n" + r.stderr[-800:])
    open(out_path, "w", encoding="utf-8").write(page)
    print(f"OK : {out_path} ({len(page) // 1024} Ko)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
