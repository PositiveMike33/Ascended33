#!/usr/bin/env python
# -*- coding: utf-8 -*-
import shutil
import os
import sys
import io

# Force UTF-8 output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

src = r'C:\Users\th3th\OneDrive\Documents\Obsidian Vault'
dst = r'D:\Vault\Vault\EXTERNAL\External Vault'

print(f"Source: {src}")
print(f"Source existe: {os.path.exists(src)}")
print(f"Destination: {dst}")
print(f"Destination existe: {os.path.exists(dst)}")
print()

try:
    # Copy all files and directories from source to destination
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)
        
        if os.path.isdir(src_path):
            if os.path.exists(dst_path):
                shutil.rmtree(dst_path)
            shutil.copytree(src_path, dst_path)
            print(f"[OK] Dossier copié: {item}")
        else:
            shutil.copy2(src_path, dst_path)
            print(f"[OK] Fichier copié: {item}")
    
    # Calculate statistics
    total_files = 0
    total_size = 0
    for root, dirs, files in os.walk(dst):
        total_files += len(files)
        for f in files:
            filepath = os.path.join(root, f)
            total_size += os.path.getsize(filepath)
    
    print()
    print(f"[OK] Copie terminée avec succès")
    print(f"Fichiers total: {total_files}")
    print(f"Taille totale: {total_size / (1024*1024):.2f} MB")
    
except Exception as e:
    print(f"[ERR] Erreur: {e}")
    sys.exit(1)
