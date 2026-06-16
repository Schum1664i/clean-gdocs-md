#!/usr/bin/env python3
"""
clean_gdocs_md.py — Nettoyeur de fichiers .md exportés depuis Google Docs
Auteur : EB MEDIAS / Jarvis RAG Workflow
Usage  : python clean_gdocs_md.py fichier.md
         python clean_gdocs_md.py dossier/       ← traite tous les .md du dossier
"""

import re
import sys
import os
from pathlib import Path


# ──────────────────────────────────────────────
# RÈGLES DE NETTOYAGE
# ──────────────────────────────────────────────

def clean_content(text: str) -> str:

    # 1. Supprimer les backslashs devant les caractères spéciaux Markdown
    #    Google Docs échappe : _ * [ ] ( ) # + - . ! { } | \ < > `
    text = re.sub(r'\\([_\*\[\]\(\)#\+\-\.!\{\}\|\\<>`])', r'\1', text)

    # 2. Nettoyer les balises XML/HTML échappées
    #    \<tag\> → <tag>   et   \</tag\> → </tag>
    text = re.sub(r'\\<', '<', text)
    text = re.sub(r'\\>', '>', text)

    # 2b. Guillemets échappés dans les attributs XML : version\="3.1" → version="3.1"
    text = re.sub(r'\\"', '"', text)

    # 2c. Signe = échappé dans les attributs XML : id\="1" → id="1"
    text = re.sub(r'\\=', '=', text)

    # 2d. Séquences === dans les commentaires XML : \=== → ===
    text = re.sub(r'\\=', '=', text)

    # 3. Nettoyer les underscores dans les noms de balises XML
    #    <meta\_prompt\_orchestrator> → <meta_prompt_orchestrator>
    #    (déjà couvert par règle 1, mais on double-check)
    text = re.sub(r'(<[^>]*?)\\_(.*?>)', lambda m: m.group(0).replace('\\_', '_'), text)

    # 4. Nettoyer les blocs de code — préfixes de langage parasites
    #    "XML\n" ou "YAML\n" ou "JSON\n" sans les triple backticks → on les encapsule
    text = re.sub(r'^(XML|YAML|JSON|PYTHON|BASH|SQL)\n', r'```\1\n', text, flags=re.MULTILINE)

    # 5. Nettoyer les séparateurs YAML mal échappés
    #    \--- → ---
    text = re.sub(r'^\\\-\-\-', '---', text, flags=re.MULTILINE)

    # 6. Supprimer les espaces insécables (U+00A0) parasites
    text = text.replace('\u00a0', ' ')

    # 7. Normaliser les fins de ligne Windows → Unix
    text = text.replace('\r\n', '\n').replace('\r', '\n')

    # 8. Supprimer les lignes blanches triples ou plus → max 2
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text


# ──────────────────────────────────────────────
# TRAITEMENT FICHIER / DOSSIER
# ──────────────────────────────────────────────

def process_file(path: Path) -> None:
    original = path.read_text(encoding='utf-8')
    cleaned  = clean_content(original)

    if cleaned == original:
        print(f"  ✓ Déjà propre : {path.name}")
        return

    # Sauvegarde .bak avant écrasement
    backup = path.with_suffix('.md.bak')
    backup.write_text(original, encoding='utf-8')

    path.write_text(cleaned, encoding='utf-8')
    
    # Stats
    before = len(re.findall(r'\\[_\*\[\]\(\)#\+\-\.!\{\}\|\\<>`]', original))
    print(f"  ✅ Nettoyé : {path.name}  ({before} échappements supprimés) → backup : {backup.name}")


def process_target(target: str) -> None:
    p = Path(target)

    if p.is_file() and p.suffix == '.md':
        process_file(p)

    elif p.is_dir():
        md_files = list(p.glob('**/*.md'))
        if not md_files:
            print(f"  ⚠ Aucun fichier .md trouvé dans {p}")
            return
        print(f"  📁 {len(md_files)} fichier(s) .md trouvé(s) dans {p}\n")
        for f in md_files:
            process_file(f)

    else:
        print(f"  ❌ Cible invalide ou non-.md : {target}")


# ──────────────────────────────────────────────
# ENTRÉE PRINCIPALE
# ──────────────────────────────────────────────

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    print("\n🧹 clean_gdocs_md.py — démarrage\n")
    for arg in sys.argv[1:]:
        process_target(arg)
    print("\n✅ Terminé.\n")
