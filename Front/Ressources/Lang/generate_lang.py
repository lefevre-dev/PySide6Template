import os
import subprocess
import sys
# https://doc.qt.io/qt-6/linguist-lupdate.html

# génération d’une ligne de commande pour création du fichier de traduction pour chaque langue

ui_files = [os.path.join("../../Front/UI", fichier) for fichier in os.listdir("../../Front/UI") if fichier.endswith(".ui")]
print(ui_files)
py_files_window = [os.path.join("../../Front/Window", "MainWindow.py")]
print(py_files_window)
py_files_widget = [os.path.join("../../Front/Widget", fichier) for fichier in os.listdir("../../Front/Widget") if fichier.endswith("Widget.py")]
print(py_files_widget)
py_files_widget_2 = [os.path.join("../../Front/Widget/Measurement", fichier) for fichier in os.listdir("../../Front/Widget/Measurement") if fichier.endswith("Widget.py")]
print(py_files_widget_2)

error_file = os.path.join("../../Front/ErrorToString.py")


languages = ("English", "Français", "Deutsch")

cmd = [r"C:\Program Files (x86)\Qt Linguist\bin\lupdate.exe"]
#
# if len(sys.argv) > 1 and sys.argv[1] == "-noobsolete":
#     cmd.append("-noobsolete")

cmd.append("-noobsolete")

for uif in ui_files:
    cmd.append(uif)
for pyf in py_files_window:
    cmd.append(pyf)
for pyf in py_files_widget:
    cmd.append(pyf)
for pyf in py_files_widget_2:
    cmd.append(pyf)

cmd.append(error_file)

cmd.append("-ts")

for l in languages:
    cmd.append(f"{l}.ts")

cmd.append("-verbose")

# execution de la commande
try:
    print(cmd)
    subprocess.run(cmd, stderr=subprocess.STDOUT)
except Exception as e:
    print(e)