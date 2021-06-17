Prérequis :
-Une carte graphique NVIDIA CUDA compatible
-les drivers NVIDIA et CUDA à jour
-une distribution Linux
-Python 3.8
-un routeur avec les ports 443 et 80 ouvert en TCP
-une adresse locale statique pour votre machine/serveur
-un NOM_DE_DOMAINE associé à l'addresse IP de votre serveur
-un compte sur wandb.ai
-le paquet Nginx à jours
-le paquet python3-certbot-nginx à jours
-le navigateur Chrome ou Brave
-adapter les arborescences de fichiers dans les fichiers de conf à votre environnement d'exécution
-adapter le nom de domaines dans les fichiers de l'extension et les fichiers de configuration
-adapter le nom de votre environnement python dans el fichier de configuration de urlwatcher.service

-Afin de faire fonctionner ce projet voici les différentes démarches :
-Installer les packets du fichier "requirements.txt" avec la commande : $ pip install requirements.txt
-exécuter le code du fichier data_preprocessing.ipynb
-exécuter le code des fichiers suivants pour obtenir les modèles :
	-training_combined.ipynb
	-training_history.ipynb
	-training_small_kaggle.ipynb
	-URL-detection_Ashish_Arya.ipynb

-Pour trouver le meilleur modèle combiné, executer le code du script suivant:
	-training_combined_for_best_model_wandb.ipynb
-Après plusieurs cycles, stopper le script, aller dans l'espace projet dans wandb.ai, trier par Test Error Rate et sélectionner le réseaux avec la plus petite valeur.
-Cliquer sur le modèle correspondant, aller dans l'onglet "files" et télécharger dans le dossier "IA_models" votre fichier "model-best.h5"

-Pour obtenir les résultats du modèle inspirer de kaggle et de votre meilleur modèle trouvé à l'étape précédente, exécuter le code des fichiers suivants:
	-Test_Ashish_Arya.ipynb
	-check_best_model.ipynb

-Ajouter dans le dossier /etc/systemd/system/ le fichier conf/urlwatcher.service
-Exécuter la commande : $ sudo systemctl start urlwatcher
-Exécuter la commande : $ sudo systemctl enable urlwatcher

-Ajouter dans le dossier /etc/nginx/sites-available/ le fichier conf/urlwatcher
-Exécuter la commande : $ sudo ln -s /etc/nginx/sites-available/urlwatcher /etc/nginx/sites-enabled
-Exécuter la commande : $ sudo certbot --nginx -d NOM_DE_DOMAINE
-Exécuter la commande : $ sudo ufw allow 'Nginx Full'
-Exécuter la commande : $ sudo systemctl restart nginx

-Attendre quelque instant que l'IA se charge (on peut vérifier si le serveur gunicorn réalise des actions avec la commande : $ sudo journalctl -u urlwatcher -f)

-Aller dans l'onglet Extension de votre navigateur
-Activer le "Developer mode"
-Ajouter l'extension en cliquant sur le bouton "Load unpacked" et en sélectionnant le dossier "url_watcher_extension"

-L'extension et le serveur sont alors fonctionnels

