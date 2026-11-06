#!/usr/bin/env python3
"""card.json 하나만 고치고 `python3 make.py` 를 실행하면
config.js / contact.vcf / qr.svg / qr.png 가 모두 다시 만들어집니다.
(QR 생성에 segno 필요: pip install segno)"""
import json, pathlib

root = pathlib.Path(__file__).parent
c = json.loads((root / "card.json").read_text(encoding="utf-8"))

def esc(s):
    return str(s).replace("\\", "\\\\").replace(",", "\\,").replace(";", "\\;").replace("\n", "\\n")

lines = [
    "BEGIN:VCARD", "VERSION:3.0",
    f"N;CHARSET=UTF-8:{esc(c['lastName'])};{esc(c['firstName'])};;;",
    f"FN;CHARSET=UTF-8:{esc(c['name'])}",
]
if c.get("company"): lines.append(f"ORG;CHARSET=UTF-8:{esc(c['company'])}")
if c.get("title"):   lines.append(f"TITLE;CHARSET=UTF-8:{esc(c['title'])}")
if c.get("phone"):   lines.append(f"TEL;TYPE=CELL,VOICE:{c['phone']}")
if c.get("email"):   lines.append(f"EMAIL;TYPE=INTERNET,WORK:{c['email']}")
if c.get("website"): lines.append(f"URL:{c['website']}")
if c.get("instagram"):
    lines.append(f"URL;TYPE=Instagram:https://instagram.com/{c['instagram']}")
    lines.append(f"X-SOCIALPROFILE;TYPE=instagram:https://instagram.com/{c['instagram']}")
if c.get("address"): lines.append(f"ADR;TYPE=WORK;CHARSET=UTF-8:;;{esc(c['address'])};;;;")
if c.get("note"):    lines.append(f"NOTE;CHARSET=UTF-8:{esc(c['note'])}")
lines.append("END:VCARD")
(root / "contact.vcf").write_bytes(("\r\n".join(lines) + "\r\n").encode("utf-8"))

(root / "config.js").write_text(
    "// 자동 생성 파일입니다. card.json 을 고친 뒤 make.py 를 실행하세요.\n"
    "window.CARD = " + json.dumps(c, ensure_ascii=False, indent=2) + ";\n",
    encoding="utf-8")

try:
    import segno
    qr = segno.make(c["siteUrl"], error="m")
    qr.save(str(root / "qr.svg"), scale=10, border=2)
    qr.save(str(root / "qr.png"), scale=20, border=2)
    print("QR ->", c["siteUrl"])
except ImportError:
    print("segno 가 없어 QR은 건너뜀 (pip install segno)")
print("done: config.js, contact.vcf")
