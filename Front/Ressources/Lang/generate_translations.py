import os
import subprocess
import sys
from pathlib import Path
import shutil


# https://doc.qt.io/qt-6/linguist-lupdate.html

def check_pyside6_lupdate():
    """Vérifie si pyside6-lupdate est disponible dans l'environnement Python actuel"""
    # Utiliser shutil.which pour trouver l'exécutable dans le PATH
    lupdate_path = shutil.which('pyside6-lupdate')
    if lupdate_path:
        try:
            result = subprocess.run([lupdate_path, '--version'],
                                    capture_output=True, check=True, text=True)
            return True
        except subprocess.CalledProcessError:
            pass

    # Essayer avec python -m comme alternative
    try:
        result = subprocess.run([sys.executable, '-m', 'PySide6.lupdate', '--version'],
                                capture_output=True, check=True, text=True)
        return True
    except subprocess.CalledProcessError:
        pass

    return False


def get_pyside6_lupdate_command():
    """Retourne la commande appropriée pour exécuter pyside6-lupdate"""
    # Essayer avec shutil.which en premier
    lupdate_path = shutil.which('pyside6-lupdate')
    if lupdate_path:
        return [lupdate_path]

    # Essayer avec python -m
    try:
        result = subprocess.run([sys.executable, '-m', 'PySide6.lupdate', '--version'],
                                capture_output=True, check=True, text=True)
        return [sys.executable, '-m', 'PySide6.lupdate']
    except subprocess.CalledProcessError:
        pass

    # Fallback vers la commande directe
    return ['pyside6-lupdate']


def get_files_safely(directory, extension, contains="", recursive=False):
    """Récupère les fichiers d'un répertoire de manière sécurisée"""
    try:
        if not os.path.exists(directory):
            print(f"Attention: Le répertoire {directory} n'existe pas")
            return []

        files = []

        if recursive:
            # Recherche récursive dans tous les sous-dossiers
            for root, dirs, filenames in os.walk(directory):
                for filename in filenames:
                    if filename.endswith(extension):
                        if not contains or contains in filename:
                            files.append(os.path.join(root, filename))
        else:
            # Recherche seulement dans le répertoire courant
            for filename in os.listdir(directory):
                if filename.endswith(extension):
                    if not contains or contains in filename:
                        files.append(os.path.join(directory, filename))

        return files
    except Exception as e:
        print(f"Erreur lors de la lecture du répertoire {directory}: {e}")
        return []


def generate_translations():
    """Génère les fichiers de traduction .ts"""

    # # Vérifier que pyside6-lupdate est disponible
    # if not check_pyside6_lupdate():
    #     print("Erreur: pyside6-lupdate n'est pas disponible dans cet environnement.")
    #     print("Installez PySide6 dans votre environnement avec: pip install PySide6")
    #     return False

    # Obtenir la commande appropriée
    lupdate_cmd = get_pyside6_lupdate_command()
    print(f"Utilisation de: {' '.join(lupdate_cmd)}")

    # Récupération des fichiers
    ui_files = get_files_safely("../../UI", ".ui", recursive=True)
    print(f"Fichiers UI trouvés: {ui_files}")

    py_files_widget = get_files_safely("../../Widget", ".py", "Widget")
    print(f"Fichiers Widget trouvés: {py_files_widget}")

    py_files_window = get_files_safely("../../Window", ".py", "Window")
    print(f"Fichiers Window trouvés: {py_files_window}")

    error_file = "../../Front/ErrorToString.py"
    if not os.path.exists(error_file):
        print(f"Attention: Le fichier {error_file} n'existe pas")
        error_file = None

    # Vérifier qu'on a au moins quelques fichiers
    all_source_files = ui_files + py_files_widget + py_files_window
    if error_file:
        all_source_files.append(error_file)

    if not all_source_files:
        print("Erreur: Aucun fichier source trouvé")
        return False

    # Langues supportées
    languages = ("English", "Français", "Deutsch")

    # Construction de la commande
    cmd = lupdate_cmd.copy()

    # Option pour ne pas inclure les traductions obsolètes
    if len(sys.argv) > 1 and sys.argv[1] == "-noobsolete":
        cmd.append("-noobsolete")
    else:
        cmd.append("-noobsolete")  # Par défaut

    # Ajout des fichiers sources
    for file in all_source_files:
        cmd.append(file)

    # Spécifier les fichiers de sortie .ts
    cmd.append("-ts")

    for lang in languages:
        cmd.append(f"{lang}.ts")

    # Mode verbose pour plus d'informations
    cmd.append("-verbose")

    # Exécution de la commande
    try:
        print(f"Commande exécutée: {' '.join(cmd)}")
        result = subprocess.run(cmd,
                                capture_output=True,
                                text=True,
                                check=True)

        print("✓ Fichiers de traduction générés avec succès!")
        if result.stdout:
            print("Sortie:")
            print(result.stdout)

        return True

    except subprocess.CalledProcessError as e:
        print(f"✗ Erreur lors de l'exécution de lupdate:")
        print(f"Code de retour: {e.returncode}")
        if e.stdout:
            print(f"Sortie: {e.stdout}")
        if e.stderr:
            print(f"Erreur: {e.stderr}")
        return False
    except Exception as e:
        print(f"✗ Erreur inattendue: {e}")
        return False


if __name__ == '__main__':
    success = generate_translations()
    if not success:
        sys.exit(1)