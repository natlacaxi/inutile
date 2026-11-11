# 1 + 1, par tous les moyens
Site volontairement inutile. HTML, CSS et JavaScript pour la page ; Python pour le serveur ;
Shell, bc, awk, sed, Perl, C, C++, Node.js, Java, Ruby, PHP, Lua, Go, Rust, Kotlin, Swift, Tcl, Julia, R et Haskell
pour le relais.

    ./run.sh          # site sur http://localhost:8000
    ./run.sh --cli    # le relais seul, dans le terminal

## Le relais
Chaque langage lit une ligne `valeur<TAB>chemin` sur son entrée, ajoute son nom au chemin et réécrit la ligne.
Python relie les programmes par de vrais tubes Unix. `bc` calcule `1+1` ; les autres transmettent.
Les langages absents de la machine, ou qui plantent, sont écartés et listés sur la page.
Pour en ajouter un : un fichier dans `relais/` et une ligne dans `ETAPES` (`server.py`).

Testés : Shell, bc, awk, sed, Perl, C, C++, Node.js, Java, Python.
Écrits mais non testés (interpréteurs absents ici) : Ruby, PHP, Lua, Go, Rust, Kotlin, Swift, Tcl, Julia, R, Haskell.

`favicon.svg` est à la racine du dépôt.
