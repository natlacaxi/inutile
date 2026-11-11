#!/usr/bin/env python3
"""Serveur inutile : sert le site et fait circuler "1+1" à travers tous les langages,
reliés par de vrais tubes Unix (stdout de l'un -> stdin du suivant).
Usage : python3 server.py          # le site sur http://localhost:8000
        python3 server.py --cli    # le relais seul, dans le terminal
"""
import json, os, random, datetime, shutil, subprocess, sys
from urllib.parse import urlparse, parse_qs
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ICI = os.path.dirname(os.path.abspath(__file__))
os.chdir(ICI)
PORT = 8000
R = "relais/"

def java_ok():
    if not shutil.which("java"):
        return False
    out = subprocess.run(["java", "--list-modules"], capture_output=True, text=True).stdout
    return "jdk.compiler" in out

# nom, programme requis, commande de compilation (ou None), commande d'exécution
ETAPES = [
    dict(nom="Shell",   req="bash",   run=["bash", R + "bash.sh"]),
    dict(nom="bc",      req="bc",     run=["bash", R + "bc.sh"]),
    dict(nom="awk",     req="awk",    run=["awk", "-f", R + "relais.awk"]),
    dict(nom="sed",     req="sed",    run=["sed", "-f", R + "relais.sed"]),
    dict(nom="Perl",    req="perl",   run=["perl", R + "relais.pl"]),
    dict(nom="C",       req="gcc",    build=["gcc", "-O2", "-o", "build/relais_c", R + "relais.c"], run=["build/relais_c"]),
    dict(nom="C++",     req="g++",    build=["g++", "-O2", "-o", "build/relais_cpp", R + "relais.cpp"], run=["build/relais_cpp"]),
    dict(nom="Node.js", req="node",   run=["node", R + "relais.js"]),
    dict(nom="Java",    req="java",   sonde=java_ok, run=["java", R + "Relais.java"]),
    dict(nom="Ruby",    req="ruby",   run=["ruby", R + "relais.rb"]),
    dict(nom="PHP",     req="php",    run=["php", R + "relais.php"]),
    dict(nom="Lua",     req="lua",    run=["lua", R + "relais.lua"]),
    dict(nom="Go",      req="go",     run=["go", "run", R + "relais.go"]),
    dict(nom="Rust",    req="rustc",  build=["rustc", "-O", "-o", "build/relais_rs", R + "relais.rs"], run=["build/relais_rs"]),
    dict(nom="Kotlin",  req="kotlinc", run=["kotlinc", "-script", R + "relais.kts"]),
    dict(nom="Swift",   req="swift",  run=["swift", R + "relais.swift"]),
    dict(nom="Tcl",     req="tclsh",  run=["tclsh", R + "relais.tcl"]),
    dict(nom="Julia",   req="julia",  run=["julia", R + "relais.jl"]),
    dict(nom="R",       req="Rscript", run=["Rscript", R + "relais.R"]),
    dict(nom="Haskell", req="runghc", run=["runghc", R + "relais.hs"]),
]

def dispo(e):
    return bool(shutil.which(e["req"])) and e.get("sonde", lambda: True)()

def preparer():
    """Compile les étages qui en ont besoin. Renvoie les étages inutilisables."""
    os.makedirs("build", exist_ok=True)
    ko = {}
    for e in ETAPES:
        if not dispo(e):
            ko[e["nom"]] = "programme absent (" + e["req"] + ")"
        elif "build" in e:
            r = subprocess.run(e["build"], capture_output=True, text=True)
            if r.returncode:
                ko[e["nom"]] = "compilation échouée : " + r.stderr.strip()[:120]
    return ko

def circuler(depart):
    """Fait passer la ligne 'valeur<TAB>chemin' dans tous les langages, reliés par des tubes."""
    ignores = dict(preparer())
    while True:
        etapes = [e for e in ETAPES if e["nom"] not in ignores]
        procs, prev, rate = [], None, None
        for e in etapes:
            try:
                p = subprocess.Popen(e["run"], stdin=subprocess.PIPE if prev is None else prev.stdout,
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except OSError as err:
                rate = (e["nom"], "impossible à lancer : " + str(err)[:100])
                break
            if prev is not None:
                prev.stdout.close()
            procs.append(p)
            prev = p
        if rate:
            for p in procs:
                p.kill()
            ignores[rate[0]] = rate[1]
            continue
        procs[0].stdin.write(f"1+1\t{depart}>Python\n".encode())
        procs[0].stdin.close()
        try:
            sortie = procs[-1].stdout.read().decode().strip()
            for p in procs:
                p.wait(timeout=120)
        except subprocess.TimeoutExpired:
            for p in procs:
                p.kill()
            sortie = ""
        fautifs = [(e, p) for e, p in zip(etapes, procs) if p.returncode not in (0, None)]
        if not fautifs and sortie:
            valeur, chemin = sortie.split("\t", 1)
            return dict(valeur=valeur, chemin=(chemin + ">Python").split(">"),
                        ignores=[dict(nom=n, raison=r) for n, r in ignores.items()])
        if not fautifs:
            fautifs = [(etapes[-1], procs[-1])]
        for e, p in fautifs[:1]:  # on écarte le premier fautif et on recommence
            err = p.stderr.read().decode().strip()[:120] if p.stderr else ""
            ignores[e["nom"]] = "a planté : " + (err or "sans message")

PY_REPONSES = ["1 + 1 = 2, j'ai vérifié deux fois.", "Python indente, donc il pense.",
               "Réponse : 2. Temps de calcul : trop long pour ce que c'est.", "import antigravity, sans succès."]

def excuse_kotlin():
    try:
        with open("data/rien.json", encoding="utf-8") as f:
            return random.choice(json.load(f)["excuses"])
    except (OSError, ValueError, KeyError):
        return "Fichier data/rien.json introuvable : Kotlin n'a pas encore travaillé."

class Handler(SimpleHTTPRequestHandler):
    def envoyer(self, obj):
        body = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        u = urlparse(self.path)
        if u.path == "/api/py":
            self.envoyer({"message": random.choice(PY_REPONSES) + " (" + datetime.datetime.now().strftime("%H:%M:%S") + ")"})
        elif u.path == "/api/kt":
            self.envoyer({"message": excuse_kotlin()})
        elif u.path == "/api/relais":
            depart = parse_qs(u.query).get("depart", ["HTML>CSS>JavaScript"])[0][:200].replace("\t", " ").replace("\n", " ")
            self.envoyer(circuler(depart))
        else:
            super().do_GET()

if __name__ == "__main__":
    if "--cli" in sys.argv:
        r = circuler("terminal")
        print(" > ".join(r["chemin"]), "=", r["valeur"])
        for i in r["ignores"]:
            print("  ignoré :", i["nom"], "-", i["raison"])
    else:
        print(f"Site inutile sur http://localhost:{PORT}")
        ThreadingHTTPServer(("", PORT), Handler).serve_forever()
