# 05 - Contre-mesures et rapport défensif

## Comment fonctionne l'attaque (point de vue de l'équipe rouge)

> Expliquez le vecteur d'attaque en langage clair afin qu'un ingénieur de l'équipe bleue puisse le comprendre sans avoir besoin d'une expertise en sécurité.
> le comprenne sans avoir besoin d'une expertise en sécurité. Soyez spécifique à
**th3-gemini** et les résultats dans 02_vulnerabilities.md.

## Mesures de remédiation

### Constatation : `nmap`

**Contre-mesure:** Restreignez les ports exposés via les règles du pare-feu (iptables/nftables). N'autorisez que les services nécessaires.

**Référence:** https://owasp.org/www-project-top-ten/

### Constatation : `gobuster`

**Contre-mesure:** Supprimez les points de terminaison debug/admin de la production. Retournez 404 (et non 403) pour les chemins sensibles afin d'éviter l'énumération.

**Référence:** https://owasp.org/www-project-top-ten/

## Règles concrètes à appliquer

```bash
# Exemple - remplacez par des commandes spécifiques pour cette recherche
# iptables -A INPUT -p tcp --dport <PORT> -j DROP
# systemctl disable <vulnerable-service>
# apt-get install --only-upgrade <package>
```

## Plan de validation

1. Appliquer les règles ci-dessus à `th3-gemini`.
2. Réexécutez le même scan HexStrike (même `operation_type` + options).
3. Confirmez que la découverte n'apparaît plus dans la sortie.
4. Documentez le résultat dans `06_validation.md`.
