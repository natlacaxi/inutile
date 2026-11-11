#!/usr/bin/env bash
IFS=$'\t' read -r v t
printf '%s\t%s>Shell\n' "$v" "$t"
