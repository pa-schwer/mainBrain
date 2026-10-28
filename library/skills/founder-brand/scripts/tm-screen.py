#!/usr/bin/env python3
# LOCAL CHANGE (mainBrain): this script is not upstream. Strip it before
# updating from Jakeschincariol/founder-skill.
"""Knockout screen of name candidates against the USPTO trademark index.

    python3 tm-screen.py NAME [NAME ...] [--classes 009,035,042] [--json out.json]

Queries the same index the USPTO's Trademark Search reads (one POST per
name, no key, no browser). For each name it reports the live marks that
contain the word, those in the classes of interest, the exact-word marks
in any class, the marks in those classes whose goods name the product's
field (the --probe words), and the one-letter neighbours that do. A name
with an exact live mark in the classes of interest, or a neighbour whose
goods match the probe, is not clean; a name with none is a candidate for
the real search, which a trademark attorney runs before filing. This is
a first pass by a machine: it does not weigh design marks, state
registrations or unregistered use, and it is not legal advice.

Standard library only. Classes to start from: 009 downloadable software,
035 business and answering services, 038 telecommunications, 042 software
as a service, 045 legal services.
"""
import argparse
import json
import re
import sys
import urllib.request

URL = "https://tmsearch.uspto.gov/prod-stage-v1-0-0/tmsearch"
FIELDS = ["wordmark", "id", "registrationId", "alive", "statusDescription", "ownerName",
          "internationalClass", "goodsAndServices", "filedDate", "registrationDate"]
PROBE = (r"artificial intelligence|\bAI\b|assistant|chatbot|chat bot|receptionist|intake|legal|law firm|attorney"
         r"|answering|virtual agent|conversation|messaging|scheduling|appointment")
SOFTWARE = {"009", "042"}


def search(query, size):
    body = json.dumps({"query": query, "size": size, "track_total_hits": True, "_source": FIELDS}).encode()
    req = urllib.request.Request(URL, data=body, headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.load(resp)
    return data["hits"]["totalValue"], [h.get("source") or h.get("_source") for h in data["hits"]["hits"]]


def live(words, size):
    return search({"bool": {"must": [{"query_string": {"query": words, "fields": ["wordmark", "wordmarkPseudoText"]}}],
                            "filter": [{"term": {"alive": True}}]}}, size)


def classes(hit):
    return {re.sub(r"\D", "", c) for c in (hit.get("internationalClass") or [])}


def goods(hit):
    return " | ".join(hit.get("goodsAndServices") or [])


def is_exact(hit, name):
    return (hit.get("wordmark") or "").strip().upper() == name.upper()


def record(hit):
    return {"wordmark": hit.get("wordmark"), "serial": hit.get("id"), "registration": hit.get("registrationId"),
            "status": hit.get("statusDescription"), "owner": (hit.get("ownerName") or [None])[0],
            "classes": sorted(classes(hit)), "filed": (hit.get("filedDate") or "")[:10], "goods": goods(hit)[:300]}


def screen(name, ours, probe, size):
    total, hits = live(f'"{name}"', size)
    in_ours = [h for h in hits if classes(h) & ours]
    exact = [h for h in hits if is_exact(h, name)]
    related = [h for h in in_ours if probe.search(goods(h))]
    _, near_hits = live(f"{name}~1", size)
    near = [h for h in near_hits if classes(h) & ours and probe.search(goods(h)) and not is_exact(h, name)]
    return {"name": name, "live_containing": total, "in_classes": [record(h) for h in in_ours],
            "exact_any_class": [record(h) for h in exact], "related_goods": [record(h) for h in related],
            "near_related": [record(h) for h in near]}


def verdict(r, ours):
    """BLOCKED: an exact-word live mark in the classes of interest with goods in
    the product's field, or in a software class. WATCH: other marks in those
    classes with such goods, or a one-letter neighbour with them. OPEN: none."""
    exact_ours = [e for e in r["exact_any_class"] if set(e["classes"]) & ours]
    if any(e in r["related_goods"] or set(e["classes"]) & SOFTWARE for e in exact_ours):
        return "BLOCKED"
    if r["related_goods"] or r["near_related"]:
        return "WATCH"
    return "OPEN"


def show(r, ours):
    print(f"\n{r['name']}: {r['verdict']}. {r['live_containing']} live marks contain it, {len(r['in_classes'])} in classes "
          f"{','.join(sorted(ours))}, {len(r['exact_any_class'])} exact in any class, {len(r['related_goods'])} with related goods, "
          f"{len(r['near_related'])} one-letter neighbours with related goods")
    for label, rows in (("related goods", r["related_goods"]), ("neighbour", r["near_related"])):
        for e in rows[:12]:
            print(f"  {label}: {e['wordmark']!r} #{e['serial']} reg {e['registration'] or '-'} | {e['status']} | "
                  f"{(e['owner'] or '?')[:40]} | {','.join(e['classes'])} | {e['goods'][:120]}")
    for e in r["exact_any_class"]:
        print(f"  exact: #{e['serial']} {','.join(e['classes'])} | {(e['owner'] or '?')[:40]} | {e['goods'][:90]}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("names", nargs="+")
    ap.add_argument("--classes", default="009,035,038,042,045")
    ap.add_argument("--probe", default=PROBE, help="regex for the product's field in the goods and services")
    ap.add_argument("--size", type=int, default=300)
    ap.add_argument("--json", help="write every record read to this file")
    a = ap.parse_args()
    ours = set(a.classes.split(","))
    probe = re.compile(a.probe, re.I)
    results = [screen(n.upper(), ours, probe, a.size) for n in a.names]
    for r in results:
        r["verdict"] = verdict(r, ours)
        show(r, ours)
    if a.json:
        with open(a.json, "w", encoding="utf-8") as fh:
            json.dump({"endpoint": URL, "classes": sorted(ours), "probe": a.probe, "results": results}, fh, indent=1, ensure_ascii=False)
        print(f"\nwrote {a.json}")


if __name__ == "__main__":
    sys.exit(main())
