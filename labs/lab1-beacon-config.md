# Lab 1 — Beacon lit sa config

**Durée :** ~40 min · **Mode :** auto-rythmé
**Module Beacon visé :** `config.py`

---

## Contexte

Beacon a besoin de savoir *quoi* surveiller. Cette information vit dans un fichier de
configuration, hors du code. Ce premier lab construit la brique qui lit et valide ce
fichier — proprement, avec une gestion d'erreur explicite.

À la fin, vous exposez une fonction :

```python
def load_config(path: Path) -> list[Target]:
    ...
```

## Prérequis

- Environnement Python 3.12+ opérationnel (fait au J0).
- `pip install pyyaml` (et `tomli`/`pydantic` seulement si vous attaquez l'extension).
- Un répertoire de projet `beacon/`.

---

## SOCLE — à réaliser par tous

### Énoncé

1. Créez un fichier `config/targets.yaml` décrivant quelques cibles :

   ```yaml
   targets:
     - name: api
       host: 127.0.0.1
       port: 8080
     - name: db
       host: 127.0.0.1
       port: 5432
   ```

2. Dans `beacon/config.py`, écrivez `load_config(path)` qui :
   - lit le fichier avec `pathlib` et un encodage explicite (`utf-8`) ;
   - le parse avec `yaml.safe_load` (**jamais** `yaml.load`) ;
   - valide la structure minimale : présence de `targets`, et pour chaque entrée
     des champs `name`, `host`, `port` ;
   - renvoie une liste d'objets `Target` (une `@dataclass` à trois champs suffit).

3. Gèrez les deux erreurs attendues avec un message **clair** :
   - fichier absent → lève une `ConfigError` explicite ;
   - YAML invalide → lève une `ConfigError`, en chaînant l'exception d'origine
     (`raise ConfigError(...) from e`).

### Critères de réussite (socle)

- [ ] `load_config(Path("config/targets.yaml"))` renvoie 2 `Target`.
- [ ] Un chemin inexistant produit une erreur lisible, pas un *stack trace* brut.
- [ ] Un YAML malformé produit une `ConfigError`, pas une `yaml.YAMLError` nue.
- [ ] `config.py` ne contient **que** la logique de configuration (pas de réseau, pas de CLI).

---

## EXTENSION — si vous avancez

Choisissez une ou plusieurs pistes, dans l'ordre que vous voulez :

1. **Multi-format.** Détectez l'extension (`.yaml` / `.toml`) et parsez en conséquence
   (`tomllib` est dans la stdlib en 3.11+). La signature publique ne change pas.
2. **Validation par schéma.** Remplacez la validation manuelle par un modèle `pydantic`
   (`Target(BaseModel)`). Observez la qualité des messages d'erreur générés.
3. **Valeurs par défaut.** Rendez `port` optionnel avec un défaut sensé selon un champ
   `type` (`http` → 80, `https` → 443).
4. **Erreur localisée.** Sur YAML invalide, faites remonter la ligne fautive dans le message.

---

## Pièges & indices

- `Path.read_text(encoding="utf-8")` vous donne le contenu en une ligne — inutile d'ouvrir
  un *file handle* à la main pour ce besoin.
- `yaml.safe_load` d'un fichier vide renvoie `None`, pas `{}`. Traitez ce cas.
- N'attrapez pas `Exception` : vous masqueriez des bugs réels. Cible `FileNotFoundError`
  et `yaml.YAMLError`.
- Définissez votre propre exception : `class ConfigError(Exception): ...`. C'est elle que la CLI saura présenter proprement.

## Livrable

- `beacon/config.py` + `config/targets.yaml`.
- Gardez ce code : le Lab 2 s'appuie dessus, et y ajoute CLI et tests.
