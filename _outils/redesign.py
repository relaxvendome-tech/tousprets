# -*- coding: utf-8 -*-
"""Refonte de présentation des pages éditoriales de tousprets.fr (idempotent).
En-tête avec slogan + recherche, menu horizontal par thèmes, pas de barre latérale,
héros éditorial (signature, 2 boutons, encart), cartes illustrées « À lire aussi ».
À relancer après toute régénération (newpages.py, qa.py…)."""
import re, glob, json, html, os, unicodedata

SITE = "/home/claude/tousprets"
ICONS = "/home/claude/icons/node_modules/lucide-static/icons"

# slug: (catégorie, icône lucide, couleur1, couleur2, titre court)
CAT = {
 # Les bases du kit
 "kit-de-survie-72h": ("bases", "backpack", "#173F70", "#2F6DB5", "Kit de survie 72 h : la liste"),
 "checklist-kit-urgence-72h": ("bases", "list-checks", "#173F70", "#2F6DB5", "Checklist à imprimer"),
 "que-mettre-dans-un-kit-d-urgence": ("bases", "package", "#173F70", "#2F6DB5", "Que mettre dans un kit d'urgence"),
 "combien-eau-stocker-par-personne": ("bases", "droplets", "#1F5C8A", "#3C86B8", "Combien d'eau stocker"),
 "aliments-sans-cuisson-kit-urgence": ("bases", "utensils", "#8A5A1F", "#B98236", "Aliments sans cuisson"),
 "sac-de-secours": ("bases", "briefcase-medical", "#7A3B2E", "#A85A45", "Le sac de secours"),
 "kit-de-survie-72h-pas-cher": ("bases", "piggy-bank", "#5B6B2E", "#7E9142", "Un kit pas cher"),
 # Guide officiel
 "kit-de-survie-gouvernement-pdf": ("guide", "file-text", "#1E3A64", "#3462A3", "Le guide officiel en PDF"),
 "kit-urgence-72h-gouvernement": ("guide", "landmark", "#1E3A64", "#3462A3", "Ce que dit le guide de l'État"),
 "guide-tous-responsables-resume": ("guide", "book-open", "#1E3A64", "#3462A3", "Le guide résumé"),
 "fr-alert-que-faire": ("guide", "bell-ring", "#8A2E2E", "#B84A3F", "Alerte FR-Alert"),
 "questions-reponses-kit-urgence": ("guide", "circle-help", "#3E3A6B", "#5F5A9A", "Questions pratiques"),
 # Selon votre foyer
 "kit-urgence-72h-famille-appartement-voiture": ("foyer", "users", "#8A6420", "#B88A36", "Famille, appartement, voiture"),
 "kit-urgence-bebe": ("foyer", "baby", "#8A4C6B", "#B56E91", "Avec un bébé"),
 "kit-urgence-animaux": ("foyer", "paw-print", "#6B4A2E", "#966A45", "Un chien, un chat"),
 "entraide-voisins-crise": ("foyer", "heart-handshake", "#2E6B5E", "#469383", "Entraide entre voisins"),
 # Selon les risques
 "coupure-electricite-que-faire": ("risques", "zap-off", "#3A3F4A", "#5D6576", "Coupure d'électricité"),
 "inondation-que-faire": ("risques", "waves", "#1F5C8A", "#3C86B8", "Inondation"),
 "tempete-que-faire": ("risques", "wind", "#465A6B", "#6B8496", "Tempête"),
 "canicule-que-faire": ("risques", "sun", "#A8561F", "#D07B35", "Canicule"),
 "vague-de-froid-que-faire": ("risques", "snowflake", "#2E6B8A", "#5A9CBD", "Vague de froid"),
 "confinement-que-faire": ("risques", "house", "#4E4A6B", "#706A96", "Confinement"),
 "attaque-terroriste-que-faire": ("risques", "shield-alert", "#6B2E2E", "#934545", "Attaque terroriste"),
 "cyberattaque-que-faire": ("risques", "laptop", "#2E3A5B", "#4A5A86", "Cyberattaque"),
 "tensions-internationales-se-preparer": ("risques", "globe", "#2E5B5B", "#468686", "Tensions internationales"),
 "preparation-catastrophe-naturelle": ("risques", "mountain", "#4E5B2E", "#718446", "Catastrophe naturelle"),
 # Matériel et pratique
 "radio-a-piles-kit-urgence": ("materiel", "radio", "#5B3A2E", "#875845", "Radio à piles"),
 "recharger-telephone-coupure-courant": ("materiel", "battery-charging", "#2E5B3A", "#468657", "Recharger son téléphone"),
 "frigo-congelateur-coupure-electricite": ("materiel", "refrigerator", "#2E4F6B", "#4A7396", "Frigo et congélateur"),
 # À propos
 "pourquoi": ("apropos", "info", "#0F2440", "#2A4A78", "Pourquoi cette appli"),
 "sources": ("apropos", "scale", "#0F2440", "#2A4A78", "Sources et méthode"),
 "licence-visuels": ("apropos", "image", "#0F2440", "#2A4A78", "Réutiliser nos visuels"),
 "diagnostic-suis-je-pret": ("bases", "clipboard-check", "#173F70", "#2F6DB5", "Test : suis-je prêt ?"),
 "charte-editoriale": ("apropos", "badge-check", "#0F2440", "#2A4A78", "Charte éditoriale"),
 "glossaire-preparation-crise": ("guide", "book-a", "#3E3A6B", "#5F5A9A", "Glossaire"),
 "reagir-en-cas-de-crise": ("apropos", "siren", "#8A2E2E", "#B84A3F", "Réagir en cas de crise"),
 "proteger-son-foyer": ("apropos", "house", "#8A6420", "#B88A36", "Protéger son foyer"),
 "s-equiper-kit-urgence": ("apropos", "flashlight", "#3A3F4A", "#5D6576", "S'équiper"),
 "anticiper-s-entraider": ("apropos", "heart-handshake", "#2E6B5E", "#469383", "Anticiper et s'entraider"),
 "preparation-outre-mer": ("apropos", "tree-palm", "#1F6B6B", "#3A9494", "Préparation outre-mer"),
 "comprendre-s-informer": ("apropos", "book-open", "#1E3A64", "#3462A3", "Comprendre et s'informer"),
 "tous-les-guides": ("apropos", "layout-grid", "#0F2440", "#2A4A78", "Tous les guides"),
 # Ajouts 2026-11-23 (pages rédigées avec les IA, vérifiées)
 "kit-urgence-enfants-ecole": ("foyer", "school", "#8A6420", "#B88A36", "Les enfants et l'école"),
 "kit-urgence-personne-agee": ("foyer", "hand-heart", "#7A4E6B", "#A26E91", "Une personne âgée"),
 "kit-urgence-handicap": ("foyer", "accessibility", "#2E5B7A", "#4A80A3", "Handicap"),
 "kit-urgence-voiture": ("foyer", "car", "#3A4A5B", "#5D7086", "La voiture"),
 "plan-familial-mise-en-surete": ("foyer", "clipboard-list", "#2E6B5E", "#469383", "Plan familial de mise en sûreté"),
 "arnaque-kit-urgence-gratuit": ("guide", "shield-x", "#8A2E2E", "#B84A3F", "Arnaques au « kit gratuit »"),
 "signal-alerte-sirene": ("guide", "siren", "#8A2E2E", "#B84A3F", "Le signal d'alerte (sirène)"),
 "feu-de-foret-que-faire": ("risques", "flame", "#A8461F", "#D0673A", "Feu de forêt"),
 "seisme-que-faire": ("risques", "activity", "#5B4A3A", "#836B56", "Séisme"),
 "accident-nucleaire-iode": ("risques", "radiation", "#6B6B1F", "#949436", "Accident nucléaire et iode"),
 "cyclone-que-faire": ("risques", "tornado", "#2E4F6B", "#4A7396", "Cyclone"),
 "groupe-electrogene-securite": ("materiel", "plug-zap", "#3A3F4A", "#5D6576", "Groupe électrogène"),
 "lampe-frontale-lanterne-kit-urgence": ("materiel", "flashlight", "#5B4A2E", "#866E45", "Lampe frontale et lanterne"),
 "piles-kit-urgence": ("materiel", "battery-full", "#2E5B3A", "#468657", "Les piles"),
 "trousse-de-secours-kit-urgence": ("materiel", "cross", "#8A2E2E", "#B84A3F", "Trousse de secours"),
 "batterie-externe-station-electrique": ("materiel", "plug", "#2E4A5B", "#466E86", "Batterie et station électrique"),
 "couverture-de-survie": ("materiel", "thermometer-snowflake", "#6B5A2E", "#968046", "Couverture de survie"),
 "detecteur-de-fumee": ("materiel", "alarm-smoke", "#4A4A4A", "#6E6E6E", "Détecteur de fumée"),
 "purifier-eau-pastilles-filtre": ("materiel", "glass-water", "#1F5C8A", "#3C86B8", "Purifier l'eau"),
 "kit-7-jours-strategie-europeenne-72h": ("bases", "calendar-days", "#1E3A64", "#3462A3", "Tenir 7 jours"),
 "kit-urgence-guadeloupe": ("outremer", "tree-palm", "#1F6B6B", "#3A9494", "Guadeloupe"),
 "kit-urgence-martinique": ("outremer", "mountain-snow", "#1F6B5B", "#3A9480", "Martinique"),
 "kit-urgence-la-reunion": ("outremer", "mountain", "#6B3A1F", "#94573A", "La Réunion"),
 "kit-urgence-guyane": ("outremer", "trees", "#2E5B2E", "#468646", "Guyane"),
 "kit-urgence-mayotte": ("outremer", "waves", "#1F5C8A", "#3C86B8", "Mayotte"),
 "kit-urgence-saint-martin-saint-barthelemy": ("outremer", "sun", "#A8561F", "#D07B35", "Saint-Martin et Saint-Barthélemy"),
}
GROUPS = [
 ("kit", "Le kit d'urgence 72 h", "L'eau, les repas sans cuisson, la liste à cocher, le sac à emporter, le guide officiel et un kit à petit prix."),
 ("reagir", "Réagir en cas de crise", "Les bons réflexes pour chaque situation, dans l'ordre : avant, pendant, après. Pour les risques de votre commune : georisques.gouv.fr."),
 ("foyer", "Protéger son foyer", "Adapter la préparation à votre famille, aux enfants, aux personnes fragiles, aux animaux, au logement et à la voiture."),
 ("equiper", "S'équiper intelligemment", "Radio, lampes, piles, trousse, batteries, eau potable, détecteur de fumée : des critères de choix neutres, sans marques."),
 ("anticiper", "Anticiper et s'entraider", "Faire le point sur sa préparation, s'organiser en famille et avec ses voisins."),
 ("outremer", "Préparation outre-mer", "Cyclones, séismes, volcans : ce qui change dans le kit selon votre territoire."),
 ("comprendre", "Comprendre et s'informer", "Le guide officiel résumé, les questions pratiques, le glossaire, nos sources et notre méthode."),
]
# Pages piliers des univers (le kit 72 h a déjà sa page centrale)
PILLARS = {"kit": "kit-de-survie-72h", "reagir": "reagir-en-cas-de-crise", "foyer": "proteger-son-foyer",
           "equiper": "s-equiper-kit-urgence", "anticiper": "anticiper-s-entraider", "outremer": "preparation-outre-mer",
           "comprendre": "comprendre-s-informer"}
UNIV = {
 "kit": ["kit-de-survie-72h","kit-urgence-72h-gouvernement","checklist-kit-urgence-72h","que-mettre-dans-un-kit-d-urgence","combien-eau-stocker-par-personne","aliments-sans-cuisson-kit-urgence","sac-de-secours","kit-de-survie-72h-pas-cher","kit-7-jours-strategie-europeenne-72h","kit-de-survie-gouvernement-pdf"],
 "reagir": ["inondation-que-faire","feu-de-foret-que-faire","seisme-que-faire","tempete-que-faire","cyclone-que-faire","canicule-que-faire","vague-de-froid-que-faire","accident-nucleaire-iode","coupure-electricite-que-faire","confinement-que-faire","attaque-terroriste-que-faire","cyberattaque-que-faire","tensions-internationales-se-preparer","preparation-catastrophe-naturelle","fr-alert-que-faire","signal-alerte-sirene"],
 "foyer": ["kit-urgence-72h-famille-appartement-voiture","kit-urgence-bebe","kit-urgence-enfants-ecole","kit-urgence-personne-agee","kit-urgence-handicap","kit-urgence-animaux","kit-urgence-voiture","plan-familial-mise-en-surete"],
 "equiper": ["radio-a-piles-kit-urgence","lampe-frontale-lanterne-kit-urgence","piles-kit-urgence","batterie-externe-station-electrique","recharger-telephone-coupure-courant","couverture-de-survie","detecteur-de-fumee","trousse-de-secours-kit-urgence","purifier-eau-pastilles-filtre","groupe-electrogene-securite","frigo-congelateur-coupure-electricite"],
 "anticiper": ["diagnostic-suis-je-pret","entraide-voisins-crise","plan-familial-mise-en-surete","arnaque-kit-urgence-gratuit"],
 "outremer": ["kit-urgence-guadeloupe","kit-urgence-martinique","kit-urgence-guyane","kit-urgence-la-reunion","kit-urgence-mayotte","kit-urgence-saint-martin-saint-barthelemy"],
 "comprendre": ["guide-tous-responsables-resume","questions-reponses-kit-urgence","glossaire-preparation-crise","sources","charte-editoriale","pourquoi","licence-visuels"],
}
NAV = [("diagnostic-suis-je-pret.html", "Suis-je prêt ?"), ("kit-de-survie-72h.html", "Kit 72 h"), ("reagir-en-cas-de-crise.html", "Réagir aux crises"),
       ("proteger-son-foyer.html", "Protéger mon foyer"), ("s-equiper-kit-urgence.html", "S'équiper"), ("preparation-outre-mer.html", "Outre-mer"),
       ("anticiper-s-entraider.html", "S'entraider"), ("tous-les-guides.html", "Tous les guides")]

def _remap():
    for u, lst in UNIV.items():
        for sl in lst:
            if sl in CAT and not getattr(_remap, "done_" + sl, False):
                v = CAT[sl]; CAT[sl] = (u,) + tuple(v[1:]); setattr(_remap, "done_" + sl, True)
_remap()

def icon_inner(name):
    s = open(f"{ICONS}/{name}.svg").read()
    return re.search(r"<svg[^>]*>(.*)</svg>", s, re.S).group(1).strip()

def thumb(slug):
    cat, ic, c1, c2, _ = CAT[slug]
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 270" width="480" height="270" role="img" aria-hidden="true">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient></defs>
<rect width="480" height="270" fill="url(#g)"/>
<circle cx="400" cy="40" r="120" fill="#fff" fill-opacity=".07"/><circle cx="60" cy="250" r="90" fill="#fff" fill-opacity=".06"/>
<circle cx="240" cy="135" r="74" fill="#fff" fill-opacity=".12"/>
<g transform="translate(192 87) scale(4)" fill="none" stroke="#fff" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{icon_inner(ic)}</g>
</svg>'''
    os.makedirs(f"{SITE}/img/cards", exist_ok=True)
    open(f"{SITE}/img/cards/{slug}.svg", "w").write(svg)

def desc_of(slug):
    try: s = open(f"{SITE}/{slug}.html", encoding="utf-8").read()
    except FileNotFoundError: return ""
    m = re.search(r'name="description" content="(.*?)"', s)
    return html.unescape(m.group(1)) if m else ""

def card(slug):
    t = CAT[slug][4]; d = html.escape(desc_of(slug))
    img = f"img/photos/{slug}.jpg" if os.path.exists(f"{SITE}/img/photos/{slug}.jpg") else f"img/cards/{slug}.svg"
    return (f'<a class="gcard" href="{slug}.html"><img src="{img}" alt="" width="480" height="270" loading="lazy">'
            f'<span class="gcard-b"><strong>{html.escape(t)}</strong><span>{d}</span></span></a>')

def cards(slugs): return '<div class="gcards">' + "".join(card(s) for s in slugs) + "</div>"

SEARCH_SVG = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>'

def header(cur):
    AC = ' aria-current="page"'
    nav = "".join(f'<li><a href="{h}"{AC if h == cur else ""}>{t}</a></li>' for h, t in NAV)
    return ('<div class="site-head"><div class="wrap-w head-in">'
            '<a class="brand" href="./"><img src="icon-192.png" alt="" width="40" height="40"><span class="brand-t"><span class="brand-n">Tous prêts</span>'
            '<span class="brand-s">Se préparer chez soi, d\'après le guide officiel</span></span></a>'
            '<form class="search" role="search" action="tous-les-guides.html"><label class="sr" for="q">Rechercher un guide</label>'
            '<input id="q" name="q" type="search" placeholder="Rechercher : eau, radio, coupure…" autocomplete="off">'
            f'<button type="submit" aria-label="Rechercher">{SEARCH_SVG}</button><ul class="search-res" hidden></ul></form>'
            '<a class="head-cta" href="./">Ouvrir l\'appli</a></div></div>'
            f'<nav class="topnav" aria-label="Thèmes"><div class="wrap-w"><ul>{nav}</ul></div></nav>')

EXTRA_REL = {
 "inondation-que-faire": ["cyclone-que-faire", "kit-urgence-voiture"],
 "tempete-que-faire": ["cyclone-que-faire", "groupe-electrogene-securite"],
 "canicule-que-faire": ["feu-de-foret-que-faire", "kit-urgence-personne-agee"],
 "vague-de-froid-que-faire": ["groupe-electrogene-securite", "couverture-de-survie"],
 "coupure-electricite-que-faire": ["groupe-electrogene-securite", "batterie-externe-station-electrique", "lampe-frontale-lanterne-kit-urgence"],
 "confinement-que-faire": ["accident-nucleaire-iode", "signal-alerte-sirene"],
 "preparation-catastrophe-naturelle": ["seisme-que-faire", "feu-de-foret-que-faire", "cyclone-que-faire"],
 "kit-urgence-72h-famille-appartement-voiture": ["kit-urgence-voiture", "kit-urgence-enfants-ecole", "kit-urgence-personne-agee", "kit-urgence-handicap"],
 "radio-a-piles-kit-urgence": ["piles-kit-urgence", "lampe-frontale-lanterne-kit-urgence"],
 "checklist-kit-urgence-72h": ["diagnostic-suis-je-pret", "plan-familial-mise-en-surete"],
 "kit-de-survie-72h": ["diagnostic-suis-je-pret", "kit-7-jours-strategie-europeenne-72h"],
 "fr-alert-que-faire": ["signal-alerte-sirene", "arnaque-kit-urgence-gratuit"],
 "entraide-voisins-crise": ["kit-urgence-personne-agee", "plan-familial-mise-en-surete"],
 "combien-eau-stocker-par-personne": ["purifier-eau-pastilles-filtre"],
 "questions-reponses-kit-urgence": ["glossaire-preparation-crise", "diagnostic-suis-je-pret"],
 "guide-tous-responsables-resume": ["glossaire-preparation-crise", "kit-de-survie-gouvernement-pdf"],
 "kit-urgence-72h-gouvernement": ["arnaque-kit-urgence-gratuit", "kit-de-survie-gouvernement-pdf"],
}

def related_for(slug, have):
    cat = CAT.get(slug, ("bases",))[0]
    pool = [s for s, v in CAT.items() if v[0] == cat and s != slug and s not in have and v[0] not in ("apropos", "comprendre")]
    pool += [s for s in ("kit-de-survie-72h", "checklist-kit-urgence-72h", "questions-reponses-kit-urgence") if s != slug and s not in have and s not in pool]
    return pool

def transform(f):
    slug = f[:-5]
    s = open(f"{SITE}/{f}", encoding="utf-8").read()
    o = s
    # 1. en-tête
    if 'class="topnav"' not in s:
        s = re.sub(r'<div class="site-head">.*?</div></div></header>', lambda m: header(f) + "</header>", s, count=1, flags=re.S)
    else:
        s = re.sub(r'<div class="site-head">.*?</nav>', lambda m: header(f), s, count=1, flags=re.S)
    # 2. barre latérale
    s = re.sub(r'<div class="layout"><nav class="risks".*?</nav>', "", s, count=1, flags=re.S)
    s = s.replace("</main></div>\n<footer", "</main>\n<footer")
    # 3. héros
    s = re.sub(r'<span class="emoji"[^>]*>.*?</span>\n?', "", s, count=1)
    m = re.search(r'<div class="meta"><span>Mis à jour le ([^<]+)</span><span>(.*?)</span></div>', s)
    if m:
        date, src = m.group(1), re.sub(r"^Sources? : ", "", m.group(2))
        cta2 = ('<a class="btn btn-2" href="kit-urgence-72h-gouvernement.html">Comprendre le guide de l\'État</a>'
                if slug == "checklist-kit-urgence-72h" else
                '<a class="btn btn-2" href="checklist-kit-urgence-72h.html">Imprimer la checklist</a>')
        new = (f'<p class="byline">Par la rédaction de <a href="pourquoi.html">Tous prêts</a> · Mis à jour le {date}</p>'
               f'<div class="hero-cta noprint"><a class="btn" href="./">Cocher ma liste dans l\'appli</a>{cta2}</div>'
               '<p class="hero-note noprint">La liste se coche sur votre appareil, même hors ligne. Rien n\'est envoyé.</p>')
        s = s[:m.start()] + new + s[m.end():]
        disc = (f'<p class="disclaimer"><strong>Informations pratiques, sources officielles</strong> ({src}). '
                'Elles ne remplacent pas les consignes des autorités. En cas d\'urgence, appelez le <a href="tel:112">112</a> '
                'et suivez les consignes de la préfecture, de la radio et de FR-Alert.</p>')
        s = s.replace('</div></div>\n<div class="wrap">\n', '</div></div>\n<div class="wrap">\n' + disc, 1)
    # 4. À lire aussi en cartes
    def va(mm):
        hrefs = re.findall(r'href="([a-z0-9-]+)\.html"', mm.group(0))
        sl = [h for h in hrefs if h in CAT and h != slug][:6]
        extra = [x for x in related_for(slug, sl)][: max(0, 3 - len(sl))]
        return ('<section id="voir-aussi" aria-labelledby="voir-aussi-t"><h2 id="voir-aussi-t">À lire aussi</h2>'
                + cards(sl + extra) + "</section>")
    if 'id="voir-aussi"' in s and 'class="gcards"' not in s[s.find('id="voir-aussi"'):s.find('id="voir-aussi"') + 4000]:
        s = re.sub(r'<section id="voir-aussi".*?</section>', va, s, count=1, flags=re.S)
    elif 'id="voir-aussi"' not in s and slug in CAT and CAT[slug][0] not in ("apropos",) and '<div class="cta-box' in s:
        rel = related_for(slug, [])[:3]
        sec = ('<section id="voir-aussi" aria-labelledby="voir-aussi-t"><h2 id="voir-aussi-t">À lire aussi</h2>'
               + cards(rel) + "</section>\n")
        s = s.replace('<div class="cta-box', sec + '<div class="cta-box', 1)
    # 3 bis. image du héros (photo de la page, sinon illustration)
    if 'class="hero-img"' not in s and '<p class="hero-note' in s:
        src = f"img/photos/{slug}.jpg" if os.path.exists(f"{SITE}/img/photos/{slug}.jpg") else (f"img/cards/{slug}.svg" if slug in CAT else None)
        if src:
            s = s.replace('<div class="hero"><div class="wrap">', '<div class="hero hero--img"><div class="wrap">', 1)
            s = re.sub(r'(<p class="hero-note[^>]*>.*?</p>)', lambda m: m.group(1) + f'<figure class="hero-img"><img src="{src}" alt="{html.escape(CAT[slug][4])} : illustration" width="960" height="540" fetchpriority="high"></figure>', s, count=1)
    # 4 ter. fil d'Ariane : Tous prêts › Tous les guides › Rubrique › page
    s = re.sub(r'(<div class="crumbs"><a href="\./">Tous prêts</a> › )<a href="tous-les-guides\.html">Tous les guides</a> › <a href="[^"]*">[^<]*</a> › ', r'\1', s, count=1)
    cat = CAT.get(slug, (None,))[0]
    gname = dict((g[0], g[1]) for g in GROUPS).get(cat)
    if gname and 'class="crumbs"' in s and 'tous-les-guides.html' not in s[s.find('class="crumbs"'):s.find('class="crumbs"')+400]:
        s = s.replace('<div class="crumbs"><a href="./">Tous prêts</a> › ',
                      f'<div class="crumbs"><a href="./">Tous prêts</a> › <a href="tous-les-guides.html">Tous les guides</a> › <a href="{PILLARS.get(cat, "tous-les-guides")}.html">{gname}</a> › ', 1)
        def bc(mm):
            j = json.loads(mm.group(1))
            for node in j.get("@graph", [j]):
                if node.get("@type") == "BreadcrumbList":
                    it = node["itemListElement"]
                    if len(it) == 2:
                        node["itemListElement"] = [it[0], {"@type": "ListItem", "position": 2, "name": "Tous les guides", "item": "https://tousprets.fr/tous-les-guides.html"}, dict(it[1], position=3)]
            return '<script type="application/ld+json">' + json.dumps(j, ensure_ascii=False) + '</script>'
        s = re.sub(r'<script type="application/ld\+json">(.*?)</script>', bc, s, flags=re.S)
    # 4 bis. image de partage = photo de la page si elle existe
    if os.path.exists(f"{SITE}/img/photos/{slug}.jpg"):
        url = f"https://tousprets.fr/img/photos/{slug}.jpg"
        s = re.sub(r'(property="og:image" content=")[^"]*"', lambda m: m.group(1) + url + '"', s, count=1)
        s = re.sub(r'(name="twitter:image" content=")[^"]*"', lambda m: m.group(1) + url + '"', s, count=1)
        s = re.sub(r'<meta property="og:image:(?:width|height|type)"[^>]*>\n?', "", s)
        try:
            cred = {c["slug"]: c for c in json.load(open(f"{SITE}/img/photos/credits.json"))}.get(slug, {})
        except Exception:
            cred = {}
        auteur = (cred.get("auteur") or "").strip()
        imgobj = {"@type": "ImageObject", "url": url, "contentUrl": url, "width": 960, "height": 540,
                  "caption": CAT.get(slug, (0, 0, 0, 0, slug))[4] + " : illustration",
                  "license": "https://creativecommons.org/publicdomain/zero/1.0/deed.fr",
                  "acquireLicensePage": "https://tousprets.fr/licence-visuels.html#photos-credits",
                  "creditText": (auteur + " (CC0)") if auteur else "Domaine public (CC0)"}
        if auteur: imgobj["creator"] = {"@type": "Person", "name": auteur}
        def setimg(mm):
            j = json.loads(mm.group(1))
            for node in j.get("@graph", [j]):
                if node.get("@type") in ("Article", "WebPage"):
                    node["image"] = imgobj
            return '<script type="application/ld+json">' + json.dumps(j, ensure_ascii=False) + '</script>'
        s = re.sub(r'<script type="application/ld\+json">(.*?)</script>', setimg, s, flags=re.S)
    # 4 quinquies. liens connexes supplémentaires (maillage vers les nouvelles pages)
    if slug in EXTRA_REL and 'id="voir-aussi"' in s:
        i = s.find('id="voir-aussi"'); j = s.find('</section>', i)
        block = s[i:j]
        add = "".join(card(x) for x in EXTRA_REL[slug] if f'href="{x}.html"' not in block and os.path.exists(f"{SITE}/{x}.html"))
        if add and '<div class="gcards">' in block:
            k = s.rfind('</div>', i, j)
            s = s[:k] + add + s[k:]
    # 4 quater. lien « Signaler une erreur »
    if 'class="report' not in s and '<div class="cta-box' in s:
        import urllib.parse
        t = re.search(r"<title>(.*?)</title>", s)
        subj = urllib.parse.quote("Erreur sur " + slug + ".html")
        rep = (f'<p class="report noprint">Une information vous semble fausse ou dépassée ? '
               f'<a href="mailto:relaxvendome@gmail.com?subject={subj}">Signaler une erreur</a> · '
               f'<a href="charte-editoriale.html">Notre charte éditoriale</a></p>\n')
        s = s.replace('<div class="cta-box', rep + '<div class="cta-box', 1)
    # 5. scripts
    if "search.js" not in s:
        s = s.replace("</body>", '<script src="search.js" defer></script>\n</body>', 1)
    if s != o:
        open(f"{SITE}/{f}", "w", encoding="utf-8").write(s)
        return True
    return False

def search_index():
    out = []
    for f in sorted(glob.glob(f"{SITE}/*.html")):
        slug = os.path.basename(f)[:-5]
        if slug not in CAT or slug == "tous-les-guides": continue
        s = open(f, encoding="utf-8").read()
        h1 = re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S)
        qs = re.findall(r'"@type": "Question", "name": "(.*?)"', s)
        cat = CAT[slug][0]; gname = dict((g[0], g[1]) for g in GROUPS).get(cat, "Outils et repères")
        out.append({"u": slug + ".html", "c": gname, "t": re.sub("<[^>]+>", "", h1.group(1)) if h1 else CAT[slug][4],
                    "d": desc_of(slug), "k": " ".join(qs)[:1500]})
    json.dump(out, open(f"{SITE}/search-index.json", "w"), ensure_ascii=False, separators=(",", ":"))
    return len(out)

if __name__ == "__main__":
    for slug in CAT: thumb(slug)
    n = 0
    for f in sorted(os.listdir(SITE)):
        if f.endswith(".html") and f != "index.html" and '<div class="site-head">' in open(f"{SITE}/{f}").read():
            n += transform(f)
    print("pages transformées", n, "index recherche", search_index())
