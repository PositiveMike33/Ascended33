try:
    import yaml
    print("[OK] Module yaml installe avec succes!")
    print("Version: " + yaml.__version__)
except ImportError as e:
    print("[ERREUR] " + str(e))
