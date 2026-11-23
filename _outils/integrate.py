# Intègre les pages rédigées par les IA (fichiers dans ai/), après corrections.
import sys, re; sys.path.insert(0, "/home/claude/seo"); sys.path.insert(0, "/home/claude/seo/ai")
import newpages as N
from check import load
files = ["gemini.py", "gemini2.py", "deepseek.py", "mistral.py"]
P = []
for f in files: P += load("/home/claude/seo/ai/" + f)
slugs = {p["slug"] for p in P}
existing = set(N.TITLES)
for p in P:
    for k in ("title", "desc", "h1", "lead"):
        p[k] = p[k].replace("[reference:", "").strip()
    p["related"] = [r for r in p["related"] if r in existing or r in slugs][:4] or ["kit-de-survie-72h"]
    for sid, t, h in p["sections"]:
        pass
    p["sections"] = [(sid, t, re.sub(r'href="([a-z0-9-]+)\.html"', lambda m: m.group(0) if (m.group(1) in existing or m.group(1) in slugs) else 'href="tous-les-guides.html"', h)) for sid, t, h in p["sections"]]
    N.TITLES[p["slug"]] = p["h1"]
for p in P:
    open(f"{N.SITE}/{p['slug']}.html", "w", encoding="utf-8").write(N.build(p))
print(len(P), "pages")
open("/home/claude/seo/ai/slugs.txt", "w").write("\n".join(p["slug"] for p in P))
