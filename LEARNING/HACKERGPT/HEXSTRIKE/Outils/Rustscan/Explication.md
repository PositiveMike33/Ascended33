### Qu'est-ce que RustScan ?

RustScan est un scanner de ports ultra-rapide écrit en Rust. Sa philosophie est simple : **Faire une seule chose, mais la faire plus vite que n'importe qui.** Contrairement à Nmap, qui tente de tout faire (détection d'OS, scripts NSE, etc.) simultanément, RustScan se concentre sur la découverte brute des ports ouverts pour ensuite passer le relais à Nmap pour l'analyse détaillée.

---

### 1. La Vitesse : Le moteur de RustScan
Grâce à l'asynchronisme de Rust, RustScan peut scanner les **65 535 ports** d'une cible en moins de 3 secondes. 

#### Optimisation de la performance :
*   **`--ulimit`** : C'est le paramètre critique. Il définit le nombre de descripteurs de fichiers (sockets) que le programme peut ouvrir simultanément. Si ton système le permet, augmente-le pour booster la vitesse.
*   **`-b` (Batch size)** : Définit le nombre de ports scannés par lot.

```bash
# Exemple de scan ultra-rapide avec ulimit élevé
rustscan -a 192.168.1.100 --ulimit 5000 -b 1000
```

---

### 2. Le Pipeline : L'intégration Nmap
C'est ici que RustScan brille. Au lieu de lancer un scan Nmap complet (très lent), RustScan identifie les ports ouverts et les injecte automatiquement dans Nmap.

**Syntaxe :** Tout ce qui suit le double tiret `--` est interprété comme une commande Nmap.

```bash
# Détecte les ports avec RustScan, puis lance une détection de service (-sV) et des scripts par défaut (-sC) avec Nmap
rustscan -a 192.168.1.100 -- -sV -sC
```

*Pourquoi c'est efficace ?* Nmap ne scannera que les ports spécifiques trouvés par RustScan (ex: 22, 80, 443), évitant ainsi de perdre du temps sur les 65 000 autres ports fermés.

---

### 3. Paramétrage Précis (Timeout & Tries)
Dans des environnements réseau instables ou face à des pare-feux restrictifs, tu dois ajuster la sensibilité :

*   **`--timeout`** : Temps d'attente (en ms) pour une réponse du port.
*   **`--tries`** : Nombre de tentatives avant de considérer un port comme fermé.

```bash
# Scan plus prudent sur un réseau instable
rustscan -a 10.10.10.5 --timeout 1500 --tries 3
```

---

### 4. Perspective Défensive : Le revers de la médaille
En tant qu'expert, je dois t'avertir : **RustScan est extrêmement bruyant.**

*   **Détection SYN Flood** : Sa vitesse repose sur l'envoi massif de paquets SYN. Un IDS (Intrusion Detection System) ou un IPS moderne détectera immédiatement ce pic de volume de connexions et bannira ton IP.
*   **Utilisation recommandée** : À utiliser lors de tests d'intrusion internes ("Red Team") où la vitesse prime sur la discrétion, ou sur des cibles dont tu sais que la protection périmétrique est faible.

---

### Résumé de la commande "Expert"
Si tu dois retenir une seule commande pour un engagement de pentest standard :

```bash
rustscan -a <IP_CIBLE> -r 1-65535 --ulimit 5000 -- -sV -A
```
*   `-r 1-65535` : Scan toute la plage de ports.
*   `--ulimit 5000` : Optimise les ressources système.
*   `-- -sV -A` : Demande à Nmap de faire une détection de version et une analyse agressive uniquement sur les ports trouvés.

As-tu une cible spécifique ou un environnement réseau particulier sur lequel tu souhaites appliquer RustScan ?

#### 📋 Quick Commands

`rustscan -a target`
`rustscan -a target -- -sC -sV`