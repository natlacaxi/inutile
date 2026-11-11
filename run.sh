#!/usr/bin/env bash
# Génère les excuses en Kotlin (si dispo), puis lance le serveur Python,
# qui compile et chaîne tous les langages installés (voir "ETAPES" dans server.py).
set -euo pipefail
cd "$(dirname "$0")"

if command -v kotlinc >/dev/null 2>&1; then
  echo "→ Kotlin : génération des excuses"
  kotlinc Rien.kt -include-runtime -d rien.jar 2>/dev/null && java -jar rien.jar
else
  echo "→ kotlinc absent : on garde data/rien.json tel quel"
fi

command -v python3 >/dev/null 2>&1 || { echo "python3 est requis"; exit 1; }
exec python3 server.py "$@"
