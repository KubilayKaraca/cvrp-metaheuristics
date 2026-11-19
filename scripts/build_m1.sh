#!/usr/bin/env bash
# Origin: written by Claude (AI). See ai_usage.md, Section 5.
# Rebuild everything for Milestone 1 from team.json:
# seed -> instance -> metric check -> figure -> report values -> PDF
set -euo pipefail
cd "$(dirname "$0")/.."
python3 src/team_seed.py team.json
rm -f instances/medidrone_s*
python3 src/generate_medidrone.py team.json instances
python3 src/check_metric.py instances
python3 src/plot_instance.py instances figures
python3 src/m1_values.py team.json instances report/m1/values.tex
cd report/m1
latexmk -pdf -interaction=nonstopmode -halt-on-error m1.tex > /dev/null
latexmk -c > /dev/null
echo "done: report/m1/m1.pdf"
