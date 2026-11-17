"""LOCAL CHANGE (mainBrain): this file is not upstream. Delete it, and the marked calls to it in site_palette.py and
site_preview.py, before updating from fatihaydost/brand-identity-skill.

An SVG read from a website, or handed over as a kept logo, is untrusted: it gets inlined into pages a headless
browser renders on this machine. Upstream removes <script> and <style> with a regular expression, which leaves event
handlers, foreignObject, external references and animations in place. sanitize_svg() keeps an allowlist instead:
drawing elements, their presentation attributes, and references that stay inside the file.

public_host() is the matching guard for downloads: a logo URL taken from a page must not point this machine at
itself, its private network or a cloud metadata address.
"""
import ipaddress
import re
import socket
import xml.etree.ElementTree as ET

SVG_NS = "http://www.w3.org/2000/svg"
XLINK_NS = "http://www.w3.org/1999/xlink"
ELEMENTS = {
    "svg", "g", "defs", "symbol", "use", "title", "desc", "path", "rect", "circle", "ellipse", "line", "polyline",
    "polygon", "linearGradient", "radialGradient", "stop", "clipPath", "mask", "pattern",
}
URL_ATTRS = {"href", "{%s}href" % XLINK_NS}
PAINT_URL = re.compile(r"url\(\s*['\"]?\s*([^)'\"]*)", re.I)


def _local(tag):
    return tag.rsplit("}", 1)[-1] if isinstance(tag, str) else ""


def _safe_value(name, value):
    if _local(name).lower().startswith("on"):
        return False
    if name in URL_ATTRS:
        return value.strip().startswith("#")
    low = value.lower()
    if "javascript:" in low or "expression(" in low or "@import" in low:
        return False
    return all(target.strip().startswith("#") for target in PAINT_URL.findall(value))


def _clean(el):
    for child in list(el):
        if not isinstance(child.tag, str) or _local(child.tag) not in ELEMENTS or (
                child.tag.startswith("{") and not child.tag.startswith("{%s}" % SVG_NS)):
            el.remove(child)
            continue
        _clean(child)
    for name in list(el.attrib):
        if not _safe_value(name, el.attrib[name]):
            del el.attrib[name]


def sanitize_svg(text):
    """The same drawing with nothing that can run or reach outside the file. '' when the text is not a parsable SVG:
    callers treat that as "no logo"."""
    if not isinstance(text, str) or "<!ENTITY" in text.upper():
        return ""
    try:
        root = ET.fromstring(re.sub(r"<!DOCTYPE[^>]*>", "", text, flags=re.I))
    except ET.ParseError:
        return ""
    if _local(root.tag) != "svg":
        return ""
    _clean(root)
    ET.register_namespace("", SVG_NS)
    ET.register_namespace("xlink", XLINK_NS)
    return ET.tostring(root, encoding="unicode")


def public_host(host):
    """False for a host that names this machine, a private or link-local network, or a metadata service. A name
    that does not resolve here (a session behind a proxy resolves nothing itself) passes: the proxy fetches it."""
    host = (host or "").strip("[]").lower()
    if not host or host == "localhost" or host.endswith((".localhost", ".local", ".internal")):
        return False
    try:
        addresses = [ipaddress.ip_address(host)]
    except ValueError:
        try:
            addresses = [ipaddress.ip_address(info[4][0].split("%")[0])
                         for info in socket.getaddrinfo(host, None)]
        except (socket.gaierror, UnicodeError, ValueError):
            return True
    return all(a.is_global for a in addresses)
