#!/usr/bin/env python3
"""
Script pour convertir automatiquement les fichiers .ui de Qt Designer
en fichiers .py utilisables dans PySide6
"""

import os
import sys
import subprocess
import glob
from pathlib import Path
import argparse


def check_pyside6_uic():
    """Vérifie si pyside6-uic est disponible dans le système"""
    try:
        subprocess.run(['pyside6-uic', '--version'],
                       capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def convert_ui_to_py(ui_file, output_dir=None, prefix="ui_"):
    """
    Convertit un fichier .ui en fichier .py

    Args:
        ui_file (str): Chemin vers le fichier .ui
        output_dir (str): Répertoire de sortie (optionnel, sinon même dossier que le .ui)
        prefix (str): Préfixe pour le nom du fichier de sortie

    Returns:
        bool: True si la conversion a réussi, False sinon
    """
    ui_path = Path(ui_file)

    if not ui_path.exists():
        print(f"Erreur: Le fichier {ui_file} n'existe pas")
        return False

    # Déterminer le nom du fichier de sortie
    if output_dir:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        py_file = output_path / f"{prefix}{ui_path.stem}.py"
    else:
        # Par défaut, générer dans le même dossier que le fichier .ui
        py_file = ui_path.parent / f"{prefix}{ui_path.stem}.py"

    try:
        # Exécuter pyside6-uic pour convertir le fichier
        cmd = ['pyside6-uic', '-o', str(py_file), str(ui_file)]
        result = subprocess.run(cmd,
                                capture_output=True,
                                text=True,
                                check=True)

        print(f"✓ Converti: {ui_file} → {py_file}")
        return True

    except subprocess.CalledProcessError as e:
        print(f"✗ Erreur lors de la conversion de {ui_file}:")
        print(f"  {e.stderr}")
        return False


def convert_directory(directory, output_dir=None, prefix="ui_", recursive=False):
    """
    Convertit tous les fichiers .ui d'un répertoire

    Args:
        directory (str): Répertoire contenant les fichiers .ui
        output_dir (str): Répertoire de sortie (optionnel, sinon même dossier que chaque .ui)
        prefix (str): Préfixe pour les noms des fichiers de sortie
        recursive (bool): Recherche récursive dans les sous-dossiers

    Returns:
        tuple: (nombre_convertis, nombre_total)
    """
    search_pattern = "**/*.ui" if recursive else "*.ui"
    ui_files = list(Path(directory).glob(search_pattern))

    if not ui_files:
        print(f"Aucun fichier .ui trouvé dans {directory}")
        return 0, 0

    converted = 0
    total = len(ui_files)

    print(f"Traitement de {total} fichier(s) .ui...")

    for ui_file in ui_files:
        if convert_ui_to_py(str(ui_file), output_dir, prefix):
            converted += 1

    return converted, total


def main():
    parser = argparse.ArgumentParser(
        description="Convertit les fichiers .ui de Qt Designer en fichiers .py pour PySide6"
    )

    parser.add_argument(
        'input',
        nargs='?',
        help='Fichier .ui ou répertoire à traiter (défaut: répertoire courant)'
    )

    parser.add_argument(
        '-o', '--output',
        help='Répertoire de sortie pour les fichiers .py (défaut: même dossier que chaque .ui)'
    )

    parser.add_argument(
        '-p', '--prefix',
        default='ui_',
        help='Préfixe pour les noms des fichiers .py (défaut: ui_)'
    )

    parser.add_argument(
        '-r', '--recursive',
        action='store_true',
        help='Recherche récursive dans les sous-dossiers'
    )

    args = parser.parse_args()

    # Vérifier que pyside6-uic est disponible
    if not check_pyside6_uic():
        print("Erreur: pyside6-uic n'est pas disponible.")
        print("Installez PySide6 avec: pip install PySide6")
        sys.exit(1)

    # Déterminer l'entrée à traiter
    input_path = args.input if args.input else '.'

    if not os.path.exists(input_path):
        print(f"Erreur: {input_path} n'existe pas")
        sys.exit(1)

    # Traitement
    if os.path.isfile(input_path):
        # Traiter un seul fichier
        if input_path.endswith('.ui'):
            success = convert_ui_to_py(input_path, args.output, args.prefix)
            if success:
                print("Conversion terminée avec succès !")
            else:
                sys.exit(1)
        else:
            print("Erreur: Le fichier doit avoir l'extension .ui")
            sys.exit(1)
    else:
        # Traiter un répertoire
        converted, total = convert_directory(
            input_path,
            args.output,
            args.prefix,
            args.recursive
        )

        print(f"\nRésultat: {converted}/{total} fichiers convertis avec succès")

        if converted < total:
            sys.exit(1)


if __name__ == "__main__":
    main()