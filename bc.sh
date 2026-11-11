#!/usr/bin/env bash
# bc évalue l'expression "1+1" : c'est le seul vrai calcul de toute la chaîne.
IFS=$'\t' read -r v t
printf '%s\t%s>bc\n' "$(echo "$v" | bc)" "$t"
