
# VNAAnalyzer

VNAAnalyzer est une application pour charger, visualiser et exporter des fichiers `.s2p` à l'aide d'un analyseur de réseaux vectoriels (VNA).

## Structure du Projet

```
VNAAnalyzer/
├── vna_analyzer/
│   ├── __init__.py
│   ├── main.py
│   ├── ui.py
│   ├── logic.py
│   ├── resources/
│   │   └── styles.qss
│   └── tests/
│       ├── __init__.py
│       ├── test_logic.py
│       └── test_ui.py
├── scripts/
│   └── create_executable.sh
├── setup.py
├── requirements.txt
└── README.md
```

## Installation

1. **Cloner le dépôt** :
    ```sh
    git clone https://github.com/touremahi/VNAAnalyzer.git
    cd VNAAnalyzer
    ```

2. **Créer un environnement virtuel** :
    ```sh
    python -m venv venv
    ```

3. **Activer l'environnement virtuel** :
    - Sur Windows :
        ```sh
        venv\Scripts\activate
        ```
    - Sur macOS et Linux :
        ```sh
        source venv/bin/activate
        ```

4. **Installer les dépendances** :
    ```sh
    pip install -r requirements.txt
    ```

## Utilisation

Pour lancer l'application, exécutez la commande suivante dans l'environnement virtuel :

```sh
python -m vna_analyzer.main
```

## Tests

Pour exécuter les tests unitaires :

```sh
python -m unittest discover -s vna_analyzer/tests
```

## Création de l'exécutable

### Prérequis

Assurez-vous que `nuitka` est installé :

```sh
pip install nuitka
```

### Utilisation du script shell

Pour créer un exécutable standalone en un seul fichier, utilisez le script shell fourni. Ce script inclut également les fichiers de ressources nécessaires.

1. **Rendre le script exécutable** (à faire une seule fois) :
    ```sh
    chmod +x scripts/create_executable.sh
    ```

2. **Exécuter le script** :
    ```sh
    ./scripts/create_executable.sh
    ```

L'exécutable sera généré dans le répertoire `dist`.

## Personnalisation des Styles

Les styles de l'application sont définis dans le fichier `styles.qss` situé dans `vna_analyzer/resources/`. Vous pouvez modifier ce fichier pour personnaliser l'apparence de l'application.

### Exemple de `styles.qss`

```css
QPushButton {
    background-color: #4CAF50;
    color: white;
    font-size: 16px;
    border-radius: 5px;
    padding: 10px;
}

QPushButton:hover {
    background-color: #45a049;
}

QMainWindow {
    background-color: #f0f0f0;
}
```

## Contribuer

Les contributions sont les bienvenues ! Veuillez suivre les étapes suivantes pour contribuer :

1. **Fork** le dépôt.
2. **Créez** une branche pour votre fonctionnalité (`git checkout -b feature/YourFeature`).
3. **Commit** vos modifications (`git commit -m 'Add some feature'`).
4. **Push** vers la branche (`git push origin feature/YourFeature`).
5. **Ouvrez** une Pull Request.

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.
