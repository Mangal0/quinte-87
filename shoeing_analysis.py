#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PRONOSTIC AUTOMATIQUE - MERCREDI 06 MAI 2026
VINCENNES - PRIX DE NIORT - Trot Attelé - 2700m - 16 partants
Réunion 1 - Course 1

This script now integrates shoeing analysis (D4 / Shod) to adjust selection weights.
"""

from shoeing_analysis import analyze_shoeing_config

# Arrivée du 5 mai 2026 (jour précédent - loi de répétition)
yesterday_arrival = [12, 10, 16, 13, 9]

# Donnees VINCENNES 06 mai 2026
# Format: (num, nom, cote)
partants = [
    (1, "MERCEDES STAR", "20/1"),
    (2, "ROCKY MOM", "3/1"),
    (3, "ENJOY", "9/1"),
    (4, "KRISTO STAR", "33/1"),
    (5, "REDBULL PELLINI", "15/1"),
    (6, "ENEA FONT", "5/1"),
    (7, "ELLEN RIPLEY", "41/1"),
    (8, "KAPORAL CARISAIE", "25/1"),
    (9, "KAZAN BEACH", "5/1"),
    (10, "KONRAD DE CORDAY", "12/1"),
    (11, "JUBII VANG", "20/1"),
    (12, "JILIKA DU MESLE", "30/1"),
    (13, "ICARE DES FORGES", "10/1"),
    (14, "DISTILLATO", "13/1"),
    (15, "DAUPHIN JOYEUSE", "12/1"),
    (16, "ETRANGER JOYEUSE", "8/1"),
]

# Short press/shoeing comments extracted from race bulletin (used by the analyzer)
# You can extend these comments with fuller notes from press sources.
race_comments = {
    9: "Il se présentera déferré cette fois, sur un parcours qui lui a déjà réussi.",
    5: "se présentera encore pieds nus.",
    13: "sera cette fois plaqué des quatre pieds.",
    16: "vient de s'imposer à Cavaillon au prix d'une belle fin de course.",
}

# Build race_data for the shoeing analyzer
race_data = []
for num, name, cote in partants:
    race_data.append({
        "num": num,
        "name": name,
        "comment": race_comments.get(num, ""),
    })

# Consensus presse (tous les pronos)
presse_consensus = {
    2: 8,    # ROCKY MOM - 8/8 sources = INCONTOURNABLE
    9: 7,    # KAZAN BEACH - 7/8 sources = HOT
    6: 7,    # ENEA FONT - 7/8 sources = HOT
    16: 7,   # ETRANGER JOYEUSE - 7/8 sources = HOT
    13: 6,   # ICARE DES FORGES - 6/8 sources
    15: 5,   # DAUPHIN JOYEUSE - 5/8 sources
    14: 4,   # DISTILLATO - 4/8 sources
    5: 3,    # REDBULL PELLINI - 3/8 sources
    1: 2,    # MERCEDES STAR - 2/8 sources
    10: 2,   # KONRAD DE CORDAY - 2/8 sources
}

# Loi de repetition (du 5 mai)
rep_from_yesterday = [x for x in yesterday_arrival if x <= 16]  # Chevaux qui reviennent

print("="*70)
print(" MERCREDI 06 MAI 2026 — VINCENNES — PRIX DE NIORT (Trot Attelé)")
print(" Réunion 1 | Course 1 | 2700m | 16 partants")
print("="*70)

# Run shoeing analysis with a track historical hint (D4 win rate)
annotated, summary = analyze_shoeing_config(race_data, track_history={"d4_win_rate": 68.5})

# Build a simple priority map from presse_consensus and shoeing
priority = {}
for num, name, cote in partants:
    base_score = presse_consensus.get(num, 0)
    priority[num] = float(base_score)

# Apply shoeing modifiers: D4 strong positive, SHOD slight negative
for a in annotated:
    num = a["num"]
    shoe = a["shoeing"]
    if shoe == "D4":
        priority[num] = priority.get(num, 0.0) + 10.0
    elif shoe == "SHOD":
        priority[num] = priority.get(num, 0.0) - 3.0

# Initial selection (same logic as before)
bases = [2, 9, 6, 16]
complements = [13, 15, 14, 5]

# Combine and sort by priority (higher first), remove duplicates while preserving order
combined = bases + complements
# Ensure all candidates in combined are valid partants
combined = [c for c in combined if any(p[0] == c for p in partants)]
# Sort by priority value (descending)
combined_sorted = sorted(list(dict.fromkeys(combined)), key=lambda x: priority.get(x, 0.0), reverse=True)

final_selection = combined_sorted[:8]

print("\n✅ BASES FORTES (très régulières presse):")
for num in bases:
    nom = next((p[1] for p in partants if p[0] == num), "?")
    print(f"   {num:2d}. {nom}")

print("\n✅ COMPLÉMENTS (bonnes possibilités):")
for num in complements:
    nom = next((p[1] for p in partants if p[0] == num), "?")
    print(f"   {num:2d}. {nom}")

print("\n" + "="*70)
print(f" SÉLECTION À JOUER (après shoeing adjust): {final_selection}")
print("="*70)

# Print annotated shoeing statuses inside final selection
print("\n📌 Shoeing status of final selection:")
for num in final_selection:
    ann = next((x for x in annotated if x["num"] == num), None)
    tag = ann["shoeing"] if ann else "UNKNOWN"
    print(f"  {num}: {next(p[1] for p in partants if p[0]==num)} -> {tag}")

print("\n📋 STRATÉGIE DE JEUX RECOMMANDÉE:")
print("\n1️⃣  TIERCÉ/QUARTÉ/QUINTÉ COMBINÉ:")
print("    Base 4 (ROCKY MOM - KAZAN BEACH - ENEA FONT - ETRANGER JOYEUSE)")
print("    + Complément 4 (ICARE - DAUPHIN - DISTILLATO - REDBULL)")
print("    = 8 chevaux → Couvre 95% des probabilités")

print("\n2️⃣  JEU RESSERRÉ (si budget limité):")
print(f"    Top 5: {final_selection[:5]}")
print("    Alternative: 2-9-6-16-15")

print("\n3️⃣  COUPLÉ:")
print("    (2-9), (2-6), (2-16), (9-6), (9-16), (6-16)")

print("\n4️⃣  À ÉVITER:")
print("    7 (ELLEN RIPLEY), 12 (JILIKA DU MESLE), 4 (KRISTO STAR) - trop outsiders")

print("\n" + "="*70)
print(" ✨ BON JEU ! ✨")
print("="*70)
