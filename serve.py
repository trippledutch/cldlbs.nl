#!/usr/bin/env python3
"""CloudLabs · serve.py

De ontwikkelserver. Vervangt `python3 -m http.server 8000`.

    python3 serve.py            draait op http://127.0.0.1:8000
    python3 serve.py 8080       op een andere poort

Waarom niet gewoon http.server: die kent de site niet, en laat daardoor drie
dingen zien die op cldlbs.com anders gaan.

  1. Een adres dat niet bestaat gaf de kale foutmelding van Python, zwart op
     wit, zonder kopbalk of weg terug. Deze server toont /404.html, en
     /en/404.html zodra het pad met /en/ begint, met een echte 404 erbij.
  2. De omleidingen uit redirects.conf deden lokaal niets. Wie /about.html
     opvroeg kreeg de oude pagina te zien in plaats van de 301 naar
     /over-ons/, dus een gebroken omleiding viel pas op de server op. Dit
     bestand leest hetzelfde conf-bestand en voert de regels uit.
  3. Een adres zonder .html, zoals /vragen, was een 404 terwijl nginx daar
     /vragen.html of /vragen/ serveert.

De server zet Cache-Control: no-store. Tijdens het werk wil je de laatste
versie zien en niet die van vijf minuten terug; op de echte server staat die
regel er niet.
"""
import http.server
import os
import pathlib
import re
import socketserver
import sys
import urllib.parse

WORTEL = pathlib.Path(__file__).resolve().parent

# Alleen de regels die aanstaan. Een uitgezette regel begint met een #, en die
# haalt het patroon hieronder niet, precies zoals nginx hem overslaat.
OMLEIDING = re.compile(r'^\s*location\s*=\s*(\S+)\s*\{\s*return\s+(30[12])\s+(\S+?)\s*;')


def omleidingen():
    conf = WORTEL / 'redirects.conf'
    if not conf.exists():
        return {}
    regels = {}
    for regel in conf.read_text(encoding='utf-8').splitlines():
        m = OMLEIDING.match(regel)
        if m:
            regels[m.group(1)] = (int(m.group(2)), m.group(3))
    return regels


class Handler(http.server.SimpleHTTPRequestHandler):
    regels = {}

    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(WORTEL), **kw)

    # ---- de omleidingen uit redirects.conf ---------------------------------
    def do_GET(self):
        if not self.omgeleid():
            super().do_GET()

    def do_HEAD(self):
        if not self.omgeleid():
            super().do_HEAD()

    def omgeleid(self):
        doel = self.regels.get(urllib.parse.urlsplit(self.path).path)
        if not doel:
            return False
        code, naar = doel
        self.send_response(code)
        self.send_header('Location', naar)
        self.send_header('Content-Length', '0')
        self.end_headers()
        return True

    # ---- /vragen serveren als /vragen.html ---------------------------------
    def translate_path(self, path):
        pad = super().translate_path(path)
        if not os.path.exists(pad) and not pad.endswith(os.sep):
            if os.path.isfile(pad + '.html'):
                return pad + '.html'
        return pad

    # ---- de foutpagina in de huisstijl -------------------------------------
    def send_error(self, code, message=None, explain=None):
        if code == 404:
            pagina = self.foutpagina()
            if pagina is not None:
                self.send_response(404, message)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.send_header('Content-Length', str(len(pagina)))
                self.end_headers()
                if self.command != 'HEAD':
                    self.wfile.write(pagina)
                return
        super().send_error(code, message, explain)

    def foutpagina(self):
        engels = urllib.parse.urlsplit(self.path).path.startswith('/en/')
        bestand = WORTEL / ('en/404.html' if engels else '404.html')
        if not bestand.is_file():
            bestand = WORTEL / '404.html'
        return bestand.read_bytes() if bestand.is_file() else None

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


def main():
    poort = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    Handler.regels = omleidingen()
    with Server(('127.0.0.1', poort), Handler) as srv:
        print(f"  CloudLabs op http://127.0.0.1:{poort}/")
        print(f"  {len(Handler.regels)} omleidingen uit redirects.conf, "
              f"foutpagina 404.html en en/404.html")
        print("  stoppen met ctrl+c")
        try:
            srv.serve_forever()
        except KeyboardInterrupt:
            print("\n  gestopt")


if __name__ == '__main__':
    main()
