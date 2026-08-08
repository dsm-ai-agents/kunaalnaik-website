#!/usr/bin/env python3
"""Dependency-free structural smoke test for the generated site."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
import json
import xml.etree.ElementTree as ET

ROOT = Path(__file__).parent
IGNORE = {"404.html"}


class Audit(HTMLParser):
    def __init__(self):
        super().__init__(); self.title=""; self.in_title=False; self.h1=0; self.description=None; self.canonical=None; self.links=[]; self.images=[]; self.jsonlds=[]; self.in_jsonld=False; self.jsonbuf=[]
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag=="title": self.in_title=True
        elif tag=="h1": self.h1+=1
        elif tag=="meta" and a.get("name")=="description": self.description=a.get("content")
        elif tag=="link" and a.get("rel")=="canonical": self.canonical=a.get("href")
        elif tag=="a" and a.get("href"): self.links.append(a["href"])
        elif tag=="img": self.images.append((a.get("src"),a.get("alt")))
        elif tag=="script" and a.get("type")=="application/ld+json": self.in_jsonld=True; self.jsonbuf=[]
    def handle_endtag(self, tag):
        if tag=="title": self.in_title=False
        elif tag=="script" and self.in_jsonld:
            self.in_jsonld=False; self.jsonlds.append("".join(self.jsonbuf))
    def handle_data(self, data):
        if self.in_title: self.title+=data
        if self.in_jsonld: self.jsonbuf.append(data)


def local_target(href):
    path=urlparse(href).path
    if path=="/": return ROOT/"index.html"
    if path.endswith("/"): return ROOT/path.lstrip("/")/"index.html"
    return ROOT/path.lstrip("/")


def main():
    errors=[]; titles={}; canonicals={}
    pages=sorted(p for p in ROOT.rglob("*.html") if ".vercel" not in p.parts)
    for path in pages:
        audit=Audit(); audit.feed(path.read_text(encoding="utf-8"))
        rel=str(path.relative_to(ROOT))
        if not audit.title.strip(): errors.append(f"{rel}: missing title")
        elif audit.title in titles: errors.append(f"{rel}: duplicate title with {titles[audit.title]}")
        else: titles[audit.title]=rel
        if audit.h1!=1: errors.append(f"{rel}: expected one H1, found {audit.h1}")
        if not audit.description: errors.append(f"{rel}: missing meta description")
        if not audit.canonical: errors.append(f"{rel}: missing canonical")
        elif audit.canonical in canonicals and rel not in IGNORE: errors.append(f"{rel}: duplicate canonical with {canonicals[audit.canonical]}")
        else: canonicals[audit.canonical]=rel
        if not audit.jsonlds: errors.append(f"{rel}: missing JSON-LD")
        for raw in audit.jsonlds:
            try: json.loads(raw)
            except json.JSONDecodeError as exc: errors.append(f"{rel}: invalid JSON-LD: {exc}")
        for href in audit.links:
            if href=="#" or href.startswith("javascript:"): errors.append(f"{rel}: placeholder link {href}")
            if href.startswith("/") and not local_target(href).exists(): errors.append(f"{rel}: broken internal link {href}")
        for src,alt in audit.images:
            if not alt: errors.append(f"{rel}: image missing alt text: {src}")
            if src and src.startswith("/") and not local_target(src).exists(): errors.append(f"{rel}: missing image {src}")
    tree=ET.parse(ROOT/"sitemap.xml")
    ns={"s":"http://www.sitemaps.org/schemas/sitemap/0.9"}
    sitemap_urls=[x.text for x in tree.findall("s:url/s:loc",ns)]
    public_pages=len([p for p in pages if p.name!="404.html"])
    if len(sitemap_urls)!=public_pages: errors.append(f"sitemap has {len(sitemap_urls)} URLs for {public_pages} public pages")
    for required in ["mailto:me@kunaalnaik.com","https://www.linkedin.com/in/kunaal-naik/","https://www.youtube.com/KunaalNaik"]:
        if not any(required in p.read_text(encoding="utf-8") for p in pages): errors.append(f"missing required link: {required}")
    if errors:
        print("FAIL")
        for error in errors: print("-",error)
        raise SystemExit(1)
    print(f"PASS: {len(pages)} pages, {len(sitemap_urls)} sitemap URLs, unique metadata, valid schema, no broken internal links")


if __name__=="__main__": main()
