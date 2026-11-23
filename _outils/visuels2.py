# -*- coding: utf-8 -*-
"""Fiches visuelles v2 — tousprets.fr — rendu haute définition (2160x2700, export web 1080x1350)."""
import base64, asyncio, pathlib, io
import segno
from playwright.async_api import async_playwright
from PIL import Image

OUT = pathlib.Path("/home/claude/tousprets/img/qr"); OUT.mkdir(parents=True, exist_ok=True)
ICON = base64.b64encode(open("/home/claude/tousprets/icon-192.png", "rb").read()).decode()
PAGE = "https://tousprets.fr/questions-reponses-kit-urgence.html"

def qr_svg(url):
    q = segno.make(url, error="m")
    buf = io.BytesIO(); q.save(buf, kind="svg", scale=4, border=0, dark="#1F2B24", light=None, xmldecl=False, svgns=True)
    return buf.getvalue().decode()

# ------------------------------------------------------------------ défs SVG communes
DEFS = """<defs>
 <filter id="sh" x="-30%" y="-30%" width="160%" height="170%"><feDropShadow dx="0" dy="10" stdDeviation="12" flood-color="#1F2B24" flood-opacity=".18"/></filter>
 <filter id="shs" x="-30%" y="-30%" width="160%" height="170%"><feDropShadow dx="0" dy="4" stdDeviation="5" flood-color="#1F2B24" flood-opacity=".16"/></filter>
 <radialGradient id="floor" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#1F2B24" stop-opacity=".22"/><stop offset="1" stop-color="#1F2B24" stop-opacity="0"/></radialGradient>
 <linearGradient id="orange" x1="0" x2="1"><stop offset="0" stop-color="#E06A1B"/><stop offset=".35" stop-color="#F7923A"/><stop offset=".7" stop-color="#EE7F26"/><stop offset="1" stop-color="#C85612"/></linearGradient>
 <linearGradient id="orangeIn" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#9C430E"/><stop offset="1" stop-color="#C2581A"/></linearGradient>
 <linearGradient id="bag" x1="0" x2="1"><stop offset="0" stop-color="#E9ECEF"/><stop offset=".45" stop-color="#FFFFFF"/><stop offset="1" stop-color="#D9DEE3"/></linearGradient>
 <linearGradient id="foam" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#6DB6F2"/><stop offset=".5" stop-color="#2F7FCF"/><stop offset="1" stop-color="#1E5C9E"/></linearGradient>
 <linearGradient id="kraft" x1="0" x2="1"><stop offset="0" stop-color="#C79A5E"/><stop offset=".5" stop-color="#E2BC84"/><stop offset="1" stop-color="#B98A4E"/></linearGradient>
 <linearGradient id="tank" x1="0" x2="1"><stop offset="0" stop-color="#C9D2DA"/><stop offset=".18" stop-color="#F4F7F9"/><stop offset=".5" stop-color="#FFFFFF"/><stop offset=".85" stop-color="#DCE3E9"/><stop offset="1" stop-color="#B9C4CE"/></linearGradient>
 <linearGradient id="blueP" x1="0" x2="1"><stop offset="0" stop-color="#1F5FA8"/><stop offset=".5" stop-color="#4C93DB"/><stop offset="1" stop-color="#1F5FA8"/></linearGradient>
 <linearGradient id="redP" x1="0" x2="1"><stop offset="0" stop-color="#9E2F22"/><stop offset=".5" stop-color="#D9533F"/><stop offset="1" stop-color="#9E2F22"/></linearGradient>
 <linearGradient id="brass" x1="0" x2="1"><stop offset="0" stop-color="#9C7424"/><stop offset=".5" stop-color="#E5C36B"/><stop offset="1" stop-color="#8F6A1F"/></linearGradient>
 <linearGradient id="water" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#8FD0F5"/><stop offset="1" stop-color="#3D97D6"/></linearGradient>
 <linearGradient id="dark" x1="0" x2="1"><stop offset="0" stop-color="#202826"/><stop offset=".5" stop-color="#3B4643"/><stop offset="1" stop-color="#1A201F"/></linearGradient>
 <linearGradient id="green" x1="0" x2="1"><stop offset="0" stop-color="#2E5748"/><stop offset=".5" stop-color="#4E8670"/><stop offset="1" stop-color="#284C3F"/></linearGradient>
 <linearGradient id="gold" x1="0" x2="1"><stop offset="0" stop-color="#B8862B"/><stop offset=".3" stop-color="#F6DA8A"/><stop offset=".6" stop-color="#C99A3A"/><stop offset="1" stop-color="#F1D07A"/></linearGradient>
 <linearGradient id="steel" x1="0" x2="1"><stop offset="0" stop-color="#8E9AA3"/><stop offset=".5" stop-color="#E3E8EC"/><stop offset="1" stop-color="#7D8992"/></linearGradient>
 <linearGradient id="wood" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#C99A68"/><stop offset="1" stop-color="#A87A4C"/></linearGradient>
 <linearGradient id="wall" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#F3EEE4"/><stop offset="1" stop-color="#E8E0D2"/></linearGradient>
</defs>"""

def callout(x, y, n, text, tx, ty, anchor="start", color="#2E5748"):
    """Pastille numérotée + étiquette, reliée au point (x,y)."""
    w = 18 * len(text) * 0.62 + 64
    bx = tx if anchor == "start" else tx - w
    return (f'<line x1="{x}" y1="{y}" x2="{tx + (0 if anchor=="start" else 0)}" y2="{ty}" stroke="{color}" stroke-width="3" stroke-dasharray="2 7" stroke-linecap="round"/>'
            f'<circle cx="{x}" cy="{y}" r="9" fill="#fff" stroke="{color}" stroke-width="4"/>'
            f'<g filter="url(#shs)"><rect x="{bx}" y="{ty-26}" width="{w}" height="52" rx="26" fill="#fff"/></g>'
            f'<circle cx="{bx+26}" cy="{ty}" r="18" fill="{color}"/>'
            f'<text x="{bx+26}" y="{ty+7}" font-family="Inter Display" font-weight="800" font-size="20" fill="#fff" text-anchor="middle">{n}</text>'
            f'<text x="{bx+52}" y="{ty+7}" font-family="Inter" font-weight="700" font-size="21" fill="#1F2B24">{text}</text>')

# ------------------------------------------------------------------ 1. Toilettes sèches
ILL_TOILETTES = f"""<svg viewBox="0 0 960 520" xmlns="http://www.w3.org/2000/svg">{DEFS}
 <ellipse cx="470" cy="478" rx="250" ry="26" fill="url(#floor)"/>
 <!-- rouleau sur l'anse -->
 <path d="M318 232 Q262 238 262 300" fill="none" stroke="#5B6560" stroke-width="6"/>
 <g filter="url(#shs)"><rect x="214" y="288" width="64" height="108" rx="14" fill="#FBFBF8"/><ellipse cx="246" cy="290" rx="32" ry="10" fill="#fff" stroke="#DADDD6" stroke-width="2"/><ellipse cx="246" cy="290" rx="9" ry="3.5" fill="#B9A587"/>
 <path d="M214 330 Q246 340 278 330" stroke="#E5E6E0" stroke-width="2" fill="none"/></g>
 <!-- seau -->
 <g filter="url(#sh)">
  <path d="M322 196 L352 456 Q470 486 588 456 L618 196 Z" fill="url(#orange)"/>
  <path d="M336 262 Q470 286 604 262" fill="none" stroke="#B9500F" stroke-width="5" opacity=".55"/>
  <path d="M344 330 Q470 354 596 330" fill="none" stroke="#B9500F" stroke-width="5" opacity=".45"/>
  <path d="M350 398 Q470 420 590 398" fill="none" stroke="#B9500F" stroke-width="5" opacity=".35"/>
  <rect x="420" y="352" width="104" height="58" rx="8" fill="#FFF6EA" opacity=".9"/>
  <text x="472" y="377" font-family="Inter Display" font-weight="800" font-size="20" fill="#B9500F" text-anchor="middle">20 L</text>
  <text x="472" y="399" font-family="Inter" font-weight="600" font-size="13" fill="#B9500F" text-anchor="middle">avec couvercle</text>
 </g>
 <!-- sac rabattu -->
 <path d="M300 170 L640 170 L646 250 Q628 274 606 256 Q588 280 566 260 Q546 284 524 262 Q502 286 480 264 Q458 286 436 262 Q414 284 392 260 Q370 280 350 256 Q326 274 294 250 Z" fill="url(#bag)" stroke="#C7CDD3" stroke-width="2"/>
 <path d="M360 186 Q366 220 356 250 M430 184 Q440 224 432 258 M512 184 Q520 224 514 260 M584 186 Q590 222 584 252" stroke="#CDD3D9" stroke-width="3" fill="none" opacity=".8"/>
 <!-- frite de piscine -->
 <ellipse cx="470" cy="170" rx="186" ry="52" fill="none" stroke="#174E87" stroke-width="44" opacity=".35" transform="translate(0 8)"/>
 <ellipse cx="470" cy="170" rx="186" ry="52" fill="none" stroke="url(#foam)" stroke-width="40"/>
 <ellipse cx="470" cy="160" rx="186" ry="52" fill="none" stroke="#9AD2FA" stroke-width="7" opacity=".55" stroke-dasharray="40 30"/>
 <ellipse cx="470" cy="170" rx="152" ry="36" fill="#9C430E" opacity=".25"/>
 <!-- ruban adhésif de fixation -->
 <rect x="292" y="176" width="30" height="40" rx="4" fill="#9BA4A8" opacity=".85" transform="rotate(-14 307 196)"/>
 <rect x="618" y="176" width="30" height="40" rx="4" fill="#9BA4A8" opacity=".85" transform="rotate(14 633 196)"/>
 <!-- sac de sciure + pelle -->
 <g filter="url(#sh)">
  <path d="M700 300 L820 300 L834 462 L688 462 Z" fill="url(#kraft)"/>
  <path d="M700 300 Q760 270 820 300 L812 316 Q760 296 708 316 Z" fill="#A77B43"/>
  <text x="761" y="402" font-family="Inter Display" font-weight="900" font-size="26" fill="#6E4C22" text-anchor="middle">SCIURE</text>
  <text x="761" y="426" font-family="Inter" font-weight="600" font-size="14" fill="#6E4C22" text-anchor="middle">bois non traité</text>
 </g>
 <g transform="rotate(-24 860 360)"><rect x="846" y="230" width="16" height="120" rx="8" fill="url(#wood)"/><path d="M830 346 h48 l-6 52 h-36 z" fill="url(#steel)"/></g>
 <circle cx="742" cy="292" r="6" fill="#D9B27A"/><circle cx="760" cy="284" r="7" fill="#CFA56C"/><circle cx="778" cy="292" r="6" fill="#D9B27A"/>
 {callout(390, 400, "1", "Seau solide", 60, 440)}
 {callout(612, 236, "2", "2 sacs épais", 700, 150)}
 {callout(300, 150, "3", "Frite fixée", 40, 92)}
 {callout(800, 300, "4", "Sciure", 940, 236, "end")}
</svg>"""

# ------------------------------------------------------------------ 2. Chauffe-eau
ILL_CHAUFFE = f"""<svg viewBox="0 0 960 520" xmlns="http://www.w3.org/2000/svg">{DEFS}
 <rect x="0" y="0" width="960" height="520" fill="url(#wall)"/>
 <g opacity=".35" stroke="#D8CFBF" stroke-width="2">{''.join(f'<line x1="0" y1="{y}" x2="960" y2="{y}"/>' for y in range(60, 520, 70))}</g>
 <rect x="0" y="470" width="960" height="50" fill="#D9CFBF"/>
 <!-- ballon -->
 <g filter="url(#sh)">
  <rect x="300" y="40" width="200" height="330" rx="90" fill="url(#tank)"/>
  <rect x="300" y="110" width="200" height="190" fill="url(#tank)"/>
  <rect x="352" y="120" width="96" height="64" rx="10" fill="#EEF2F5" stroke="#C9D2DA" stroke-width="2"/>
  <text x="400" y="148" font-family="Inter Display" font-weight="900" font-size="22" fill="#2E5748" text-anchor="middle">200 L</text>
  <text x="400" y="170" font-family="Inter" font-weight="600" font-size="12" fill="#52655A" text-anchor="middle">eau du réseau</text>
  <circle cx="400" cy="238" r="18" fill="#fff" stroke="#C9D2DA" stroke-width="3"/><path d="M400 238 l9 -9" stroke="#A3452F" stroke-width="4" stroke-linecap="round"/>
 </g>
 <!-- tuyaux -->
 <rect x="342" y="360" width="22" height="130" fill="url(#blueP)"/>
 <rect x="436" y="360" width="22" height="70" fill="url(#redP)"/>
 <rect x="436" y="416" width="190" height="22" fill="url(#redP)"/>
 <rect x="604" y="300" width="22" height="138" fill="url(#redP)"/>
 <!-- robinet d'eau chaude ouvert -->
 <g filter="url(#shs)"><rect x="586" y="262" width="80" height="40" rx="10" fill="url(#steel)"/><rect x="650" y="292" width="16" height="30" rx="4" fill="url(#steel)"/>
 <rect x="612" y="236" width="10" height="30" fill="#7D8992"/><rect x="596" y="228" width="44" height="12" rx="6" fill="#A3452F"/></g>
 <path d="M680 296 q18 -20 0 -40 M698 300 q22 -26 0 -52" stroke="#3D97D6" stroke-width="4" fill="none" stroke-linecap="round" opacity=".8"/>
 <!-- vanne arrivée froide -->
 <g filter="url(#shs)"><rect x="330" y="398" width="46" height="34" rx="6" fill="url(#brass)"/><rect x="300" y="404" width="44" height="14" rx="7" fill="#C62F2F" transform="rotate(90 353 411)"/></g>
 <!-- groupe de sécurité + vidange -->
 <g filter="url(#shs)"><rect x="328" y="446" width="50" height="30" rx="6" fill="url(#brass)"/><circle cx="353" cy="461" r="9" fill="#C62F2F"/></g>
 <path d="M346 476 q4 30 -2 52" stroke="url(#water)" stroke-width="8" fill="none" opacity=".9"/>
 <g filter="url(#sh)"><path d="M290 486 L410 486 L398 520 L302 520 Z" fill="#3F6F5E"/><rect x="286" y="480" width="128" height="12" rx="6" fill="#2E5748"/></g>
 <!-- tableau électrique -->
 <g filter="url(#sh)"><rect x="760" y="70" width="150" height="190" rx="16" fill="#FAFAF7" stroke="#D5DCD1" stroke-width="3"/>
  {''.join(f'<rect x="{782+i*32}" y="112" width="24" height="56" rx="5" fill="#E6EAE4"/><rect x="{787+i*32}" y="118" width="14" height="22" rx="3" fill="#7D8992"/>' for i in range(4))}
  <rect x="782" y="186" width="56" height="56" rx="6" fill="#FFE8E2" stroke="#A3452F" stroke-width="3"/><rect x="800" y="208" width="20" height="26" rx="4" fill="#A3452F"/>
  <text x="868" y="220" font-family="Inter Display" font-weight="900" font-size="20" fill="#A3452F" text-anchor="middle">OFF</text></g>
 {callout(810, 214, "1", "Couper le courant", 940, 316, "end", "#A3452F")}
 {callout(353, 411, "2", "Fermer l'eau froide", 40, 300)}
 {callout(660, 300, "3", "Ouvrir l'eau chaude", 940, 440, "end")}
 {callout(353, 461, "4", "Vidanger", 40, 452)}
</svg>"""

# ------------------------------------------------------------------ 3. Communication
ILL_COMM = f"""<svg viewBox="0 0 960 520" xmlns="http://www.w3.org/2000/svg">{DEFS}
 <ellipse cx="480" cy="470" rx="400" ry="30" fill="url(#floor)"/>
 <!-- radio -->
 <g filter="url(#sh)"><rect x="70" y="250" width="260" height="190" rx="28" fill="url(#green)"/>
  <rect x="92" y="272" width="120" height="146" rx="18" fill="#203F34"/>
  {''.join(f'<circle cx="{112+ (i%5)*20}" cy="{294+(i//5)*20}" r="5" fill="#4E8670"/>' for i in range(30))}
  <rect x="228" y="276" width="84" height="40" rx="8" fill="#F4E7C8"/><line x1="240" y1="296" x2="300" y2="296" stroke="#A87A32" stroke-width="2"/><rect x="262" y="284" width="4" height="24" fill="#A3452F"/>
  <circle cx="248" cy="372" r="22" fill="url(#steel)"/><circle cx="296" cy="372" r="16" fill="url(#steel)"/>
  <line x1="300" y1="250" x2="360" y2="120" stroke="#5B6560" stroke-width="6" stroke-linecap="round"/><circle cx="360" cy="120" r="7" fill="#5B6560"/></g>
 <path d="M380 118 q20 20 0 40 M396 106 q32 32 0 64" stroke="#3F6F5E" stroke-width="5" fill="none" stroke-linecap="round"/>
 <!-- téléphone -->
 <g filter="url(#sh)"><rect x="420" y="150" width="150" height="300" rx="28" fill="#1F2B24"/><rect x="432" y="172" width="126" height="256" rx="16" fill="#F4F6F0"/>
  <text x="495" y="262" font-family="Inter Display" font-weight="900" font-size="58" fill="#A3452F" text-anchor="middle">112</text>
  <rect x="452" y="290" width="86" height="40" rx="20" fill="#3F6F5E"/><path d="M482 310 l8 8 l16 -16" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round"/>
  <text x="495" y="366" font-family="Inter" font-weight="700" font-size="15" fill="#52655A" text-anchor="middle">Urgences</text>
  <text x="495" y="386" font-family="Inter" font-weight="600" font-size="13" fill="#7A8B81" text-anchor="middle">autre réseau</text>
  <rect x="478" y="158" width="34" height="6" rx="3" fill="#3B4643"/></g>
 <!-- carte SIM -->
 <g filter="url(#shs)" transform="rotate(-12 610 420)"><path d="M590 380 h54 l14 14 v56 h-68 z" fill="url(#gold)" stroke="#9C7424" stroke-width="2"/><rect x="604" y="404" width="34" height="28" rx="4" fill="#E3C47A" stroke="#9C7424" stroke-width="2"/></g>
 <!-- talkie -->
 <g filter="url(#sh)"><rect x="700" y="210" width="96" height="230" rx="22" fill="url(#dark)"/><rect x="712" y="100" width="16" height="120" rx="8" fill="#2A3331"/>
  <rect x="716" y="232" width="64" height="44" rx="8" fill="#9FD6B6"/><text x="748" y="262" font-family="Inter Display" font-weight="800" font-size="20" fill="#1F2B24" text-anchor="middle">CH 3</text>
  {''.join(f'<rect x="716" y="{296+i*16}" width="64" height="6" rx="3" fill="#525E5A"/>' for i in range(5))}
  <rect x="792" y="270" width="12" height="54" rx="6" fill="#F08A2E"/></g>
 <!-- satellite -->
 <g transform="translate(830 70) rotate(30)" filter="url(#shs)"><rect x="-18" y="-18" width="36" height="36" rx="6" fill="url(#steel)"/><rect x="-80" y="-14" width="56" height="28" rx="3" fill="#2F5F9E"/><rect x="24" y="-14" width="56" height="28" rx="3" fill="#2F5F9E"/>
  <line x1="-80" y1="0" x2="80" y2="0" stroke="#7FB1E6" stroke-width="2"/></g>
 <path d="M590 168 Q700 60 800 92" stroke="#2F5F9E" stroke-width="3" fill="none" stroke-dasharray="6 9"/>
 {callout(200, 260, "1", "Radio à piles", 40, 200)}
 {callout(495, 200, "2", "112 + carte SIM", 500, 80)}
 {callout(748, 330, "3", "Talkies PMR446", 940, 470, "end")}
 {callout(850, 120, "4", "SOS satellite", 940, 190, "end", "#2F5F9E")}
</svg>"""

# ------------------------------------------------------------------ 4. Appartement
ILL_APPART = f"""<svg viewBox="0 0 960 520" xmlns="http://www.w3.org/2000/svg">{DEFS}
 <rect width="960" height="520" fill="url(#wall)"/>
 <rect y="430" width="960" height="90" fill="#CDB89A"/>
 {''.join(f'<line x1="{x}" y1="430" x2="{x-40}" y2="520" stroke="#BCA585" stroke-width="2"/>' for x in range(60, 1000, 90))}
 <!-- porte + sac -->
 <g filter="url(#sh)"><rect x="40" y="70" width="170" height="362" rx="6" fill="#B98A5A"/><rect x="58" y="90" width="134" height="140" rx="4" fill="#C99A68"/><rect x="58" y="250" width="134" height="160" rx="4" fill="#C99A68"/>
  <circle cx="190" cy="262" r="8" fill="url(#brass)"/></g>
 <g filter="url(#sh)"><path d="M90 160 q34 -30 68 0" stroke="#2E5748" stroke-width="7" fill="none"/><rect x="74" y="160" width="100" height="130" rx="22" fill="url(#green)"/><rect x="92" y="196" width="64" height="44" rx="10" fill="#284C3F"/><rect x="92" y="252" width="64" height="8" rx="4" fill="#F08A2E"/></g>
 <!-- étagère haute -->
 <g filter="url(#shs)"><rect x="300" y="110" width="250" height="12" rx="4" fill="url(#wood)"/>
  <rect x="316" y="74" width="70" height="36" rx="6" fill="url(#gold)"/><rect x="398" y="58" width="44" height="52" rx="8" fill="#3F6F5E"/><circle cx="420" cy="74" r="10" fill="#FCE9A8"/>
  <rect x="456" y="80" width="80" height="30" rx="4" fill="#F4F6F0" stroke="#C9D2DA" stroke-width="2"/><text x="496" y="100" font-family="Inter" font-weight="800" font-size="14" fill="#52655A" text-anchor="middle">PAPIERS</text></g>
 <!-- lit + bacs -->
 <g filter="url(#sh)"><rect x="300" y="260" width="420" height="80" rx="16" fill="#E9EEE3"/><rect x="300" y="240" width="420" height="40" rx="16" fill="#FFFFFF"/>
  <rect x="300" y="190" width="30" height="240" rx="8" fill="url(#wood)"/><rect x="690" y="230" width="30" height="200" rx="8" fill="url(#wood)"/>
  <rect x="330" y="340" width="360" height="12" fill="url(#wood)"/></g>
 <g filter="url(#shs)"><rect x="346" y="362" width="150" height="66" rx="10" fill="#D5E6F2" stroke="#9DBBD1" stroke-width="2"/>
  {''.join(f'<rect x="{358+i*34}" y="374" width="24" height="48" rx="8" fill="url(#water)"/>' for i in range(4))}
  <rect x="512" y="362" width="160" height="66" rx="10" fill="#EFE6D2" stroke="#CDBF9F" stroke-width="2"/>
  {''.join(f'<rect x="{524+i*36}" y="384" width="28" height="36" rx="5" fill="url(#steel)"/>' for i in range(4))}</g>
 <!-- organiseur de porte (droite) -->
 <g filter="url(#sh)"><rect x="770" y="60" width="160" height="372" rx="6" fill="#FAFAF7" stroke="#D5DCD1" stroke-width="3"/>
  <rect x="786" y="90" width="128" height="200" rx="8" fill="#E9EEE3"/>
  {''.join(f'<rect x="{794+(i%2)*62}" y="{100+(i//2)*48}" width="54" height="40" rx="6" fill="#fff" stroke="#C9D2DA" stroke-width="2"/>' for i in range(8))}
  <rect x="804" y="108" width="16" height="26" rx="3" fill="#F08A2E"/><rect x="866" y="112" width="30" height="20" rx="4" fill="#A3452F"/><rect x="812" y="158" width="26" height="20" rx="3" fill="url(#gold)"/></g>
 {callout(124, 200, "1", "Sac près de l'entrée", 236, 40)}
 {callout(420, 400, "2", "Eau au sol", 300, 478 - 6)}
 {callout(560, 395, "3", "Conserves sous le lit", 940, 478 - 6, "end")}
 {callout(420, 90, "4", "Le léger en hauteur", 560, 196)}
</svg>"""

# ------------------------------------------------------------------ 5. Objets
def lab(x, y, n):
    return f'<circle cx="{x}" cy="{y}" r="17" fill="#2E5748"/><text x="{x}" y="{y+7}" font-family="Inter Display" font-weight="800" font-size="19" fill="#fff" text-anchor="middle">{n}</text>'
ILL_OBJETS = f"""<svg viewBox="0 0 960 520" xmlns="http://www.w3.org/2000/svg">{DEFS}
 <rect x="30" y="20" width="900" height="480" rx="28" fill="#EFE9DD"/>
 <g filter="url(#sh)"><!-- sifflet -->
  <rect x="80" y="90" width="130" height="56" rx="16" fill="#F08A2E"/><circle cx="110" cy="150" r="42" fill="#F08A2E"/><circle cx="110" cy="150" r="16" fill="#C9631C"/><rect x="190" y="98" width="30" height="40" rx="6" fill="#C9631C"/>
  <path d="M74 118 q-30 -10 -34 -40" stroke="#3B4643" stroke-width="4" fill="none"/></g>
 {lab(200, 186, "1")}
 <g filter="url(#sh)"><!-- ruban -->
  <circle cx="340" cy="130" r="70" fill="url(#steel)"/><circle cx="340" cy="130" r="34" fill="#EFE9DD"/><circle cx="340" cy="130" r="34" fill="none" stroke="#B8C1C8" stroke-width="6"/>
  <path d="M400 168 l60 28 l-8 14 l-62 -26 z" fill="#B8C1C8"/></g>
 {lab(410, 76, "2")}
 <g filter="url(#sh)"><!-- sacs poubelle -->
  <rect x="520" y="70" width="140" height="120" rx="24" fill="url(#dark)"/><rect x="520" y="118" width="140" height="12" fill="#55615D"/><ellipse cx="590" cy="70" rx="70" ry="16" fill="#3B4643"/><ellipse cx="590" cy="70" rx="22" ry="6" fill="#1A201F"/></g>
 {lab(668, 72, "3")}
 <g filter="url(#sh)"><!-- couverture de survie -->
  <path d="M720 70 L880 60 L892 186 L730 198 Z" fill="url(#gold)"/><path d="M724 110 L886 100 M727 150 L889 140" stroke="#B8862B" stroke-width="2" opacity=".7"/>
  <path d="M760 66 L770 194 M820 62 L832 190" stroke="#FFF2C6" stroke-width="3" opacity=".6"/></g>
 {lab(890, 200, "4")}
 <g filter="url(#sh)"><!-- gants de travail -->
  <g transform="translate(70 342) scale(.9)">
   <path d="M20 40 Q16 -20 30 -40 L30 -90 Q30 -104 43 -104 Q56 -104 56 -90 L56 -46 L60 -110 Q60 -124 73 -124 Q86 -124 86 -110 L86 -46 L90 -104 Q90 -118 103 -118 Q116 -118 116 -104 L116 -42 L120 -86 Q120 -98 132 -98 Q144 -98 144 -86 L144 20 Q144 60 110 74 L52 74 Q20 70 20 40 Z" fill="#E7B84F"/>
   <path d="M20 10 Q-10 -6 -18 -34 Q-22 -48 -8 -52 Q4 -54 12 -40 L30 -10" fill="#D9A73A"/>
   <rect x="34" y="72" width="104" height="44" rx="10" fill="#2E5748"/><rect x="34" y="84" width="104" height="8" fill="#4E8670"/>
   <path d="M56 -46 L56 10 M86 -46 L86 10 M116 -42 L116 10" stroke="#C99A30" stroke-width="3" opacity=".6"/>
  </g>
  <g transform="translate(188 356) scale(.84)">
   <path d="M20 40 Q16 -20 30 -40 L30 -90 Q30 -104 43 -104 Q56 -104 56 -90 L56 -46 L60 -110 Q60 -124 73 -124 Q86 -124 86 -110 L86 -46 L90 -104 Q90 -118 103 -118 Q116 -118 116 -104 L116 -42 L120 -86 Q120 -98 132 -98 Q144 -98 144 -86 L144 20 Q144 60 110 74 L52 74 Q20 70 20 40 Z" fill="#D4A23A"/>
   <path d="M20 10 Q-10 -6 -18 -34 Q-22 -48 -8 -52 Q4 -54 12 -40 L30 -10" fill="#C4922E"/>
   <rect x="34" y="72" width="104" height="44" rx="10" fill="#284C3F"/><rect x="34" y="84" width="104" height="8" fill="#4E8670"/>
  </g></g>
 {lab(60, 470, "5")}
 <g filter="url(#sh)"><!-- gel -->
  <rect x="360" y="290" width="76" height="150" rx="18" fill="#BFE3F2"/><rect x="360" y="330" width="76" height="70" fill="#fff" opacity=".85"/>
  <text x="398" y="372" font-family="Inter" font-weight="800" font-size="14" fill="#2F5F9E" text-anchor="middle">GEL</text>
  <rect x="384" y="262" width="28" height="30" rx="4" fill="#2F5F9E"/><rect x="384" y="252" width="52" height="12" rx="6" fill="#2F5F9E"/></g>
 {lab(450, 290, "6")}
 <g filter="url(#sh)"><!-- multi-outil -->
  <path d="M600 336 L742 296 Q752 300 748 310 L612 372 Z" fill="url(#steel)"/><path d="M620 350 L742 304" stroke="#fff" stroke-width="3" opacity=".6"/><rect x="480" y="330" width="150" height="50" rx="22" fill="#A3452F"/><rect x="480" y="330" width="150" height="16" rx="8" fill="#C45A44" opacity=".7"/><circle cx="604" cy="355" r="9" fill="url(#steel)"/><path d="M500 345 h12 v20 h-12 z M519 345 h12 v20 h-12 z" fill="#fff" opacity=".9"/></g>
 {lab(600, 412, "7")}
 <g filter="url(#sh)"><!-- piles -->
  {''.join(f'<rect x="{770+i*34}" y="290" width="28" height="120" rx="8" fill="url(#dark)"/><rect x="{770+i*34}" y="290" width="28" height="36" rx="8" fill="#F08A2E"/><rect x="{779+i*34}" y="282" width="10" height="10" rx="2" fill="url(#steel)"/>' for i in range(4))}</g>
 {lab(840, 440, "8")}
</svg>"""

# ------------------------------------------------------------------ gabarit
CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{width:1080px;height:1350px;background:#F6F3EC;font-family:Inter,sans-serif;color:#1F2B24;display:flex;flex-direction:column;-webkit-font-smoothing:antialiased}
.top{display:flex;align-items:center;gap:16px;padding:40px 60px 0}
.top img{width:52px;height:52px;border-radius:14px;box-shadow:0 4px 10px rgba(31,43,36,.15)}
.top .b{font-family:'Inter Display';font-weight:800;font-size:28px;letter-spacing:-.4px}
.top .f{margin-left:auto;font-weight:700;font-size:18px;letter-spacing:2.5px;color:#52655A;text-transform:uppercase;border:2px solid #D5DCD1;border-radius:30px;padding:8px 18px}
.title{padding:30px 60px 0}
.kick{font-weight:800;font-size:21px;letter-spacing:3px;text-transform:uppercase;color:VAR_ACC}
h1{font-family:'Inter Display';font-weight:900;font-size:72px;line-height:.98;letter-spacing:-2.2px;margin-top:12px}
h1 em{font-style:normal;color:VAR_ACC}
.ill{margin:26px 40px 0;height:520px;border-radius:40px;background:VAR_BG;overflow:hidden;position:relative}
.ill svg{width:100%;height:100%;display:block}
.steps{display:grid;grid-template-columns:1fr 1fr;gap:14px;padding:22px 40px 0}
.st{background:#fff;border-radius:24px;padding:18px 22px;display:flex;gap:16px;align-items:flex-start;box-shadow:0 2px 0 #E6E1D6}
.st .n{font-family:'Inter Display';font-weight:900;font-size:40px;line-height:1;color:VAR_ACC;min-width:30px}
.st b{display:block;font-size:23px;line-height:1.15;letter-spacing:-.2px}
.st span{display:block;font-size:18px;line-height:1.3;color:#52655A;margin-top:4px}
.note{margin:14px 40px 0;font-size:19px;line-height:1.35;color:#5A2A20;background:#F8E3DC;border-radius:18px;padding:12px 20px}
.note b{color:#A3452F}
.foot{margin-top:auto;background:#1F3B31;color:#fff;padding:26px 60px;display:flex;align-items:center;gap:26px}
.foot .u{font-family:'Inter Display';font-weight:900;font-size:50px;letter-spacing:-1px;line-height:1}
.foot .t{font-size:19px;opacity:.82;margin-top:8px}
.foot .s{font-size:14px;opacity:.6;margin-top:6px}
.qr{margin-left:auto;background:#fff;border-radius:16px;padding:12px;display:flex;flex-direction:column;align-items:center;gap:6px}
.qr svg{width:104px;height:104px}
.qr small{font-size:12px;color:#1F2B24;font-weight:700}
"""

def page(num, kicker, title, ill, steps, src, acc="#2E5748", bg="#E4ECE6", note="", ill_h=520):
    css = CSS.replace("VAR_ACC", acc).replace("VAR_BG", bg).replace("height:520px", f"height:{ill_h}px")
    st = "".join(f'<div class="st"><div class="n">{i}</div><div><b>{t}</b><span>{d}</span></div></div>' for i, (t, d) in enumerate(steps, 1))
    nt = f'<div class="note">{note}</div>' if note else ""
    return f"""<!doctype html><html lang="fr"><head><meta charset="utf-8"><style>{css}</style></head><body>
<div class="top"><img src="data:image/png;base64,{ICON}" alt=""><span class="b">Tous prêts</span><span class="f">Fiche pratique {num:02d}</span></div>
<div class="title"><div class="kick">{kicker}</div><h1>{title}</h1></div>
<div class="ill">{ill}</div>
<div class="steps">{st}</div>{nt}
<div class="foot"><div><div class="u">tousprets.fr</div><div class="t">Kit d'urgence 72 h · checklist gratuite, sans pub</div><div class="s">{src}</div></div>
<div class="qr">{qr_svg(PAGE)}<small>La fiche complète</small></div></div>
</body></html>"""

FICHES = {
 "toilettes-seches-seau": page(1, "Eau coupée", "Toilettes sèches<br><em>avec un seau</em>", ILL_TOILETTES,
   [("Seau stable 15–20 L", "avec couvercle, pièce aérée"), ("Deux sacs épais", "l'un dans l'autre, rabattus"),
    ("Assise fixée", "frite fendue + ruban adhésif"), ("Sciure à chaque fois", "1 à 2 poignées, ou litière végétale")],
   "Sources : protection civile, guide « Tous responsables » (SGDSN, 2025)", "#C85612", "#FBE9D7",
   "<b>Sac à moitié plein :</b> le nouer, bac fermé, au frais, loin des points d'eau. Égouts en état ? Un seau d'eau versé d'un coup suffit."),
 "chauffe-eau-reserve-eau": page(2, "Réserve d'eau cachée", "Votre chauffe-eau,<br><em>une réserve d'eau</em>", ILL_CHAUFFE,
   [("Couper le courant", "au disjoncteur (ou le gaz)"), ("Fermer l'eau froide", "vanne d'arrivée du ballon"),
    ("Ouvrir l'eau chaude", "un robinet, pour l'air"), ("Refroidir, puis vidanger", "dans un récipient, via la vidange")],
   "Sources : Croix-Rouge, FEMA, notices fabricants", "#2F5F9E", "#E3EDF6",
   "<b>À repérer dès aujourd'hui :</b> la vanne et la vidange. Hygiène d'abord ; à boire en dernier recours, bouillie. Jamais pour les biberons."),
 "communiquer-sans-reseau": page(3, "Plus de réseau", "Communiquer<br><em>sans réseau</em>", ILL_COMM,
   [("Radio à piles", "les consignes officielles"), ("112 avec une carte SIM", "passe par un autre opérateur"),
    ("Talkies PMR446", "sans licence, canal ouvert"), ("Point de rendez-vous", "décidé avant, numéros sur papier")],
   "Sources : service-public.fr, Arcep, Apple, guide « Tous responsables »", "#2E5748", "#E4ECE6",
   "<b>En France :</b> 15 Samu · 17 police · 18 pompiers · 112 partout en Europe · 114 par SMS."),
 "rangement-petit-appartement": page(4, "Petit logement", "Ranger son kit <em>sans cave</em>", ILL_APPART,
   [("Sac près de l'entrée", "prêt à partir en 1 minute"), ("L'eau au sol", "lourde : jamais en hauteur"),
    ("Sous le lit", "conserves dans des bacs plats"), ("Le léger en hauteur", "lampe, papiers, couverture")],
   "Source : guide « Tous responsables » (SGDSN, 2025)", "#A87A32", "#F4ECDD",
   "<b>À éviter :</b> la cave en zone inondable, près du four ou d'un radiateur.", 600),
 "objets-oublies-kit-urgence": page(5, "Petit budget", "8 objets <em>qu'on oublie</em>", ILL_OBJETS,
   [("Sifflet · ruban adhésif", "se signaler, réparer"), ("Sacs épais · couverture", "toilettes, pluie, chaleur"),
    ("Gants · gel", "déblayer, mains propres"), ("Multi-outil · piles", "ouvrir, éclairer, écouter")],
   "Source : guide « Tous responsables » (SGDSN, 2025)", "#2E5748", "#EFE9DD",
   "<b>Petit budget :</b> la plupart se trouvent pour quelques euros en grande surface.", 600),
}

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        pg = await b.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=2)
        for name, html in FICHES.items():
            await pg.set_content(html, wait_until="load")
            await pg.evaluate("document.fonts.ready")
            h = await pg.evaluate("document.body.scrollHeight")
            hd = OUT / f"{name}.png"
            await pg.screenshot(path=str(hd))
            im = Image.open(hd)
            im.save(hd, optimize=True)  # 2160x2700, téléchargement
            im.resize((1080, 1350), Image.LANCZOS).save(OUT / f"{name}.webp", "WEBP", quality=88, method=6)
            print(name, "h", h, im.size)
        await b.close()

asyncio.run(main())

# --- métadonnées IPTC/XMP (droits, crédit, licence) après chaque rendu
import pyexiv2
pyexiv2.registerNs('http://ns.useplus.org/ldf/xmp/1.0/', 'plus')
TITRES = {"toilettes-seches-seau":"Toilettes sèches avec un seau","chauffe-eau-reserve-eau":"Le chauffe-eau, une réserve d'eau",
 "communiquer-sans-reseau":"Communiquer sans réseau","rangement-petit-appartement":"Ranger son kit d'urgence sans cave",
 "objets-oublies-kit-urgence":"8 objets qu'on oublie dans le kit d'urgence"}
for slug, titre in TITRES.items():
    for ext in ("png", "webp"):
        im = pyexiv2.Image(str(OUT / f"{slug}.{ext}"))
        im.modify_xmp({'Xmp.dc.title': {'lang="x-default"': titre}, 'Xmp.dc.creator': ['Tous prêts (tousprets.fr)'],
          'Xmp.dc.rights': {'lang="x-default"': '© 2026 Tous prêts (tousprets.fr) — licence CC BY 4.0'},
          'Xmp.photoshop.Credit': 'Tous prêts — tousprets.fr', 'Xmp.xmpRights.Marked': 'True',
          'Xmp.xmpRights.WebStatement': 'https://creativecommons.org/licenses/by/4.0/',
          'Xmp.plus.Licensor': 'type="Seq"', 'Xmp.plus.Licensor[1]/plus:LicensorName': 'Tous prêts',
          'Xmp.plus.Licensor[1]/plus:LicensorURL': 'https://tousprets.fr/licence-visuels.html',
          'Xmp.iptcExt.DigitalSourceType': 'http://cv.iptc.org/newscodes/digitalsourcetype/digitalCreation'})
        im.close()
print("métadonnées IPTC/XMP écrites")
