# clean-gdocs-md 🧹

**Nettoyeur automatique de fichiers Markdown exportés depuis Google Docs.**

Supprime les backslashs parasites et normalise la structure pour garantir une compatibilité totale avec les LLMs : Gemini, GPT, Claude, Mistral, Copilot, Perplexity et tout pipeline RAG.

---

## Pourquoi ce script existe

Quand vous exportez un document Google Docs en `.md` (via l'add-on [Docs to Markdown](https://workspace.google.com/marketplace/app/docs_to_markdown/700168918607)), le fichier produit contient systématiquement des **caractères d'échappement parasites** :

```
# Avant nettoyage
\<meta\_prompt\_orchestrator version\="3.1"\>
\<rule id\="1"\>Analyser l\'intention\</rule\>
requires\_mcp: \["database\_schema\_read"\]
\---
```

```
# Après nettoyage
<meta_prompt_orchestrator version="3.1">
<rule id="1">Analyser l'intention</rule>
requires_mcp: ["database_schema_read"]
---
```

Ces artefacts sont **invisibles à l'œil** dans un éditeur avec rendu Markdown, mais ils **cassent le parsing XML**, **brisent les blocs YAML/JSON** et **dégradent la compréhension des LLMs** lors de l'injection dans un pipeline RAG ou un prompt système.

---

## Ce que le script corrige

| Problème | Exemple avant | Exemple après |
|---|---|---|
| Balises XML échappées | `\<system\_role\>` | `<system_role>` |
| Attributs XML échappés | `version\="3.1"` | `version="3.1"` |
| Signe `=` échappé | `id\="1"` | `id="1"` |
| Frontmatter YAML cassé | `\---` | `---` |
| Underscores échappés | `requires\_mcp` | `requires_mcp` |
| Crochets Markdown | `\[VARIABLE\]` | `[VARIABLE]` |
| Espaces insécables | `U+00A0` invisible | espace standard |
| Fins de ligne Windows | `\r\n` | `\n` |
| Lignes blanches multiples | `\n\n\n\n` | `\n\n` |

---

## Installation

Aucune dépendance externe. Python 3.7+ suffit.

```bash
git clone https://github.com/Schum1664i/clean-gdocs-md.git
cd clean-gdocs-md
```

---

## Utilisation

### Un seul fichier

```bash
python clean_gdocs_md.py mon_document.md
```

### Un dossier entier (récursif)

```bash
python clean_gdocs_md.py chemin/vers/dossier/
```

### Exemple de sortie

```
🧹 clean_gdocs_md.py — démarrage

  ✅ Nettoyé : rapport_sprint1.md  (388 échappements supprimés) → backup : rapport_sprint1.md.bak
  ✓ Déjà propre : notes.md

✅ Terminé.
```

> **Sécurité** : un fichier `.md.bak` est automatiquement créé avant chaque modification. Aucune donnée n'est perdue.

---

## Cas d'usage typiques

- **Pipeline RAG** : nettoyage des documents avant injection dans une base vectorielle (ChromaDB, Pinecone, Weaviate…)
- **Prompt engineering** : normalisation des Meta Prompts, Skills et Templates au format XML/Markdown hybride
- **Workflows multi-LLM** : préparation de documents compatibles GPT-5, Gemini 3.1 Pro, Claude 4.6, Mistral, Copilot
- **Knowledge base** : alimentation d'une base de connaissances documentaire (Obsidian, Notion, OneDrive…)
- **Automatisation** : intégration dans un script de post-traitement après export Google Docs

---

## FAQ

**Q : Est-ce que ce script modifie le contenu sémantique de mes documents ?**
Non. Il supprime uniquement les caractères d'échappement parasites introduits par Google Docs. Le sens, la structure et le contenu restent identiques.

**Q : Mon fichier `.bak` est-il nécessaire après vérification ?**
Non, vous pouvez le supprimer. Il est créé par précaution pour permettre un rollback immédiat si nécessaire.

**Q : Le script fonctionne-t-il sur des fichiers Markdown créés avec d'autres outils ?**
Il est optimisé pour la sortie de l'add-on Google Docs to Markdown. Il peut fonctionner sur d'autres sources, mais certains cas d'échappement spécifiques à d'autres exporteurs ne sont pas couverts.

**Q : Est-ce compatible avec un pipeline CI/CD ?**
Oui. Le script retourne un code de sortie `0` en cas de succès et peut être intégré dans un workflow GitHub Actions, un Makefile ou tout script de post-traitement automatisé.

**Q : Peut-on traiter des sous-dossiers imbriqués ?**
Oui. Le mode dossier utilise `glob('**/*.md')` — il traite tous les `.md` de manière récursive, quelle que soit la profondeur.

**Q : Le script gère-t-il les caractères accentués (UTF-8) ?**
Oui. Tous les fichiers sont lus et écrits en UTF-8 explicitement. Les caractères français (é, è, ç, à…) sont préservés.

**Q : Que se passe-t-il si le fichier est déjà propre ?**
Le script détecte qu'aucune modification n'est nécessaire, affiche `✓ Déjà propre` et ne touche pas au fichier (aucun `.bak` créé).

---

## Contribution

Les issues et PR sont les bienvenues. Si vous identifiez un cas d'échappement non couvert par votre exporteur Google Docs, ouvrez une issue avec un exemple `avant / après`.

---

## Licence

MIT — libre d'utilisation, de modification et de distribution.

---

## Soutien

Ce script est publié gratuitement par **Éric Boufflers**, consultant SEO et passionné d'industrialisation IA.

Si cet outil vous a fait gagner du temps, le meilleur moyen de le soutenir est de vous inscrire à la newsletter gratuite — pas de spam, 100 % conforme RGPD, juste du contenu utile sur le SEO, l'IA et l'automatisation :

👉 **[entreprendreautrementexpert.com](https://entreprendreautrementexpert.com/)**

Gratuit. Sans engagement. Et ça fait vraiment plaisir. 🙏
