#!/usr/bin/env python3
"""Inject a COACH object (JSON) into the dashboard template without breaking the <script> tag.

Usage: python3 -I kit/inject-coach.py kit/coach-dashboard-template.html coach.json output.html "Goal: Harbour 10K"

- `</` becomes `<\\/` and U+2028/U+2029 are escaped: an activity name or text copied from the web
  cannot close the <script> tag and run code.
- Checks the syntax of the final script with node, if installed.
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
        sys.exit("COACH must be a JSON object")
    data = (json.dumps(coach, ensure_ascii=False, separators=(",", ":"))
            .replace("</", "<\\/").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029"))
    if tpl.count(START + "{}" + END) != 1:
        sys.exit("COACH markers not found (was the template already filled in?)")
    page = tpl.replace(START + "{}" + END, START + data + END)
    page = page.replace("<title>Coach course</title>", "<title>" + html.escape(title[:60]) + "</title>", 1)
    if shutil.which("node"):
        js = re.findall(r"<script>([\s\S]*?)</script>", page)[-1]
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
            f.write(js)
        r = subprocess.run(["node", "-e", "new Function(require('fs').readFileSync(process.argv[1],'utf8'))", f.name],
                           capture_output=True, text=True)
        if r.returncode:
            sys.exit("syntax error in the script:\n" + r.stderr[-800:])
    open(out_path, "w", encoding="utf-8").write(page)
    print(f"OK: {out_path} ({len(page) // 1024} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
