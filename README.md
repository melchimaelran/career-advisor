# Conseiller Carrière Tech — outil personnel

Outil personnel basé sur Claude Code. Vision complète et décisions : PRD.md.
Contexte chargé automatiquement par Claude Code à chaque session : CLAUDE.md.

## Pour reprendre le travail

Ouvrir ce dossier dans Claude Code, puis lancer :

    /spec:status

Ça affiche où en est chaque spec (voir la roadmap dans PRD.md, section 13) et la
prochaine action recommandée.

## Démarrer la première spec

    /spec:new fondations

Puis suivre le cycle habituel : /spec:requirements → /spec:approve requirements
→ /spec:design → /spec:approve design → /spec:tasks → /spec:approve tasks
→ /spec:implement

## Méthode

Ce projet suit un workflow Spec-Driven Development, repris sans modification de
https://github.com/papaoloba/spec-based-claude-code (commandes dans
.claude/commands/spec/).
