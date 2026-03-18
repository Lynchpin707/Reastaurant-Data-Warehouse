import os

data_dir = 'data'

# Vérifier si le dossier existe
print(os.path.exists(data_dir))  # True si le chemin est correct

# Lister les fichiers à l'intérieur
print(os.listdir(data_dir))