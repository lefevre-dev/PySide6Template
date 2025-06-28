import os
import subprocess
import sys


def check_pyside6_rcc():
    """Vérifie si pyside6-rcc est disponible dans le système"""
    try:
        subprocess.run(['pyside6-rcc', '--version'],
                       capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def generate_ressources():
    base_path = os.path.dirname(os.path.abspath(__file__))
    qrc_file = os.path.join(base_path, "ressources.qrc")
    output_file = os.path.join(base_path, "ressources_rc.py")

    # Vérifier que le fichier .qrc existe
    if not os.path.exists(qrc_file):
        print(f"Erreur: Le fichier {qrc_file} n'existe pas")
        return False

    # Vérifier que pyside6-rcc est disponible
    # if not check_pyside6_rcc():
    #     print("Erreur: pyside6-rcc n'est pas disponible.")
    #     print("Installez PySide6 avec: pip install PySide6")
    #     return False

    try:
        cmd = ["pyside6-rcc", qrc_file, "-o", output_file]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)

        print(f"✓ Ressources générées: {qrc_file} → {output_file}")
        return True

    except subprocess.CalledProcessError as e:
        print(f"✗ Erreur lors de la génération des ressources:")
        print(f"  {e.stderr}")
        return False


if __name__ == '__main__':
    success = generate_ressources()
    if not success:
        sys.exit(1)