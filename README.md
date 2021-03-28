# Scraping :

Tous les fichiers nécessaires se trouvent dans le dossier scraping (les fichiers où se trouve le code que j'ai ajouté sont items.py et spiders/bougespider.py)
Les dépendances à installer sont :
- scrapy
- requests
- regex

L'exécution doit se faire en deux fois (une pour chaque méthode de scrapping) :
Depuis un terminal, se placer dans le dossier bougescraper/bougescraper/ puis exécuter les commandes suivantes :

scrapy crawl bouge -O data_from_treillieres_website.csv

scrapy crawl googlebouge -O data_from_googleAPI.csv

Il y aura donc 2 fichiers csv créés (à l'emplacement actuel), un pour chaque méthode de scraping.  