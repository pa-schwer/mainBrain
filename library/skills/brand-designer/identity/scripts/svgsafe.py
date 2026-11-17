"""LOCAL CHANGE (mainBrain): this file is not upstream. Delete it, and the marked calls to it in site_palette.py and
site_preview.py, before updating from fatihaydost/brand-identity-skill.

An SVG read from a website, or handed over as a kept logo, is untrusted: it gets inlined into pages a headless
browser renders on this machine. Upstream removes <script> and <style> with a regular expression, which leaves event
handlers, foreignObject, external references and animations in place. sanitize_svg() keeps an allowlist instead:
drawing elements, their presentation attributes, and references that stay inside the file.

public_host() is the matching guard for downloads: a logo URL taken from a page must not point this machine at
itself, its private network or a cloud metadata address.
"""
import http.client
import ipaddress
import re
import socket
import urllib.request
import xml.etree.ElementTree as ET

SVG_NS = "http://www.w3.org/2000/svg"
XLINK_NS = "http://www.w3.org/1999/xlink"
ELEMENTS = {
    "svg", "g", "defs", "symbol", "use", "title", "desc", "path", "rect", "circle", "ellipse", "line", "polyline",
    "polygon", "linearGradient", "radialGradient", "stop", "clipPath", "mask", "pattern",
}
# Geometry, structure and presentation. No style, no class, no xml:base, no event handler: an attribute that is not
# listed here is dropped, so a new way to load a resource has no name to hide under.
ATTRIBUTES = {
    "id", "viewBox", "width", "height", "x", "y", "x1", "y1", "x2", "y2", "cx", "cy", "r", "rx", "ry", "d", "points",
    "transform", "preserveAspectRatio", "fill", "fill-rule", "fill-opacity", "stroke", "stroke-width",
    "stroke-linecap", "stroke-linejoin", "stroke-miterlimit", "stroke-dasharray", "stroke-dashoffset",
    "stroke-opacity", "opacity", "clip-path", "clip-rule", "mask", "offset", "stop-color", "stop-opacity",
    "gradientUnits", "gradientTransform", "spreadMethod", "fx", "fy", "patternUnits", "patternTransform",
    "patternContentUnits", "clipPathUnits", "maskUnits", "maskContentUnits", "color", "vector-effect",
    "paint-order", "role", "aria-label", "aria-hidden", "aria-labelledby", "aria-describedby",
}
URL_ATTRS = {"href", "{%s}href" % XLINK_NS}
LOCAL_REF = re.compile(r"^#[A-Za-z_][\w.-]*$")
PAINT_REF = re.compile(r"^url\(#[A-Za-z_][\w.-]*\)(\s+[a-zA-Z#0-9]+)?$")
# The only functions a value may call: colours and transforms. Everything else with a bracket is refused.
FUNCTIONS = {"rgb", "rgba", "hsl", "hsla", "oklch", "oklab", "lab", "lch", "color", "matrix", "translate", "scale",
             "rotate", "skewx", "skewy"}
CALL = re.compile(r"([A-Za-z-]+)\s*\(")


def _local(tag):
    return tag.rsplit("}", 1)[-1] if isinstance(tag, str) else ""


def _safe_value(name, value):
    if name in URL_ATTRS:
        return bool(LOCAL_REF.match(value.strip()))
    if name not in ATTRIBUTES or "\\" in value or len(value) > 200000:
        return False
    stripped = value.strip()
    if stripped.lower().startswith("url("):
        return bool(PAINT_REF.match(stripped))
    return all(fn.lower() in FUNCTIONS for fn in CALL.findall(value))


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


def _proxied():
    proxies = urllib.request.getproxies()
    return bool(proxies.get("https") or proxies.get("http"))


def _checked_addresses(host):
    """Every address the host resolves to, or [] when one of them is not a public one, or none resolves."""
    host = (host or "").strip("[]").lower()
    if not host or host == "localhost" or host.endswith((".localhost", ".local", ".internal")):
        return []
    try:
        addresses = [ipaddress.ip_address(host)]
    except ValueError:
        try:
            addresses = [ipaddress.ip_address(info[4][0].split("%")[0])
                         for info in socket.getaddrinfo(host, None, type=socket.SOCK_STREAM)]
        except (socket.gaierror, UnicodeError, ValueError):
            return []
    return [str(a) for a in addresses] if addresses and all(a.is_global for a in addresses) else []


def public_host(host):
    """False for a host that names this machine, a private or link-local network, or a metadata service.

    With a proxy configured the proxy resolves the name, so a name that does not resolve here passes and the proxy
    fetches it; an address literal and a local name are still refused. With no proxy the answer fails closed, and
    guarded_handlers() makes the connection go to the address that was checked."""
    host = (host or "").strip("[]").lower()
    if _checked_addresses(host):
        return True
    if not _proxied() or not host or host == "localhost" or host.endswith((".localhost", ".local", ".internal")):
        return False
    try:
        ipaddress.ip_address(host)
        return False
    except ValueError:
        pass
    try:
        socket.getaddrinfo(host, None)
        return False      # it resolves here, to an address that is not public
    except (socket.gaierror, UnicodeError):
        return True       # only the proxy can resolve it


def _pinned(base):
    class Pinned(base):
        """Connects to an address checked at connect time, so a name cannot answer with a public address for the
        check and a private one for the connection. Host header and TLS server name stay the original name."""

        def connect(self):
            addresses = _checked_addresses(self.host)
            if not addresses:
                raise OSError(f"refused: {self.host} is not a public host")
            name, self.host = self.host, addresses[0]
            try:
                if isinstance(self, http.client.HTTPSConnection):
                    self.sock = self._create_connection((self.host, self.port), self.timeout, self.source_address)
                    self.sock = self._context.wrap_socket(self.sock, server_hostname=name)
                else:
                    super().connect()
            finally:
                self.host = name
    return Pinned


def guarded_handlers(context):
    """urllib handlers for a download named by an untrusted page. Behind a proxy: the stock handlers, the proxy
    connects. Direct: every connection, redirects included, is pinned to a checked public address."""
    if _proxied():
        return [urllib.request.HTTPSHandler(context=context)]
    https, plain = _pinned(http.client.HTTPSConnection), _pinned(http.client.HTTPConnection)

    class HTTPS(urllib.request.HTTPSHandler):
        def https_open(self, req):
            return self.do_open(https, req, context=context)

    class HTTP(urllib.request.HTTPHandler):
        def http_open(self, req):
            return self.do_open(plain, req)

    return [HTTPS(), HTTP()]
