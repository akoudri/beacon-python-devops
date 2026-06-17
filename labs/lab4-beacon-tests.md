# Lab 4 — Beacon testé

**Durée :** ~45 min · **Mode :** auto-rythmé
**Module Beacon visé :** `tests/`

---

## Contexte

Beacon est installable (Lab 3) mais non protégé : la moindre modification peut introduire
une régression silencieuse. Ce lab installe le filet — une suite de tests rapides et
déterministes, qui ne dépendent **pas** du réseau réel. C'est la condition d'une CI utile.

Principe directeur : **mocker la frontière système** (la socket), **tester la logique**
(parsing, mapping up/down, codes de sortie).

## Prérequis

- Le projet installable du Lab 3.
- `pip install pytest` (et `pytest-cov` seulement pour l'extension).

---

## SOCLE — à réaliser par tous

### Énoncé

1. Créer `tests/test_config.py` :
   - un test du cas nominal, en écrivant un YAML valide dans `tmp_path` ;
   - un test du cas d'échec : chemin inexistant → `ConfigError`
     (via `pytest.raises(ConfigError)`).

2. Créer `tests/test_probe.py` :
   - `test_probe_up` : mocker `socket.create_connection` (avec `monkeypatch.setattr`)
     pour qu'elle réussisse, puis vérifier `status == "up"` ;
   - `test_probe_down` : mocker la même fonction pour qu'elle lève `OSError`, puis
     vérifier `status == "down"` **sans exception remontée**.

3. Lancer la suite : `pytest` doit passer intégralement, en quelques dizaines de
   millisecondes, sans accès réseau.

### Critères de réussite (socle)

- [ ] `pytest` est vert, sans aucune connexion réseau réelle.
- [ ] Le cas nominal et le cas d'échec de `load_config` sont couverts.
- [ ] `probe()` est testé sur `up` et `down` via mocking.
- [ ] Les tests sont rapides et reproductibles (relançables à l'identique).

---

## EXTENSION — pour aller plus loin

1. **Couverture.** Mesurer avec `pytest-cov` (`pytest --cov=beacon`) et identifier les
   branches non couvertes.
2. **Fixtures paramétrées.** Utiliser `@pytest.mark.parametrize` pour tester plusieurs
   configurations (1 cible, plusieurs, champs manquants).
3. **YAML invalide.** Vérifier qu'un contenu YAML malformé produit bien une `ConfigError`.
4. **Tester la CLI.** Vérifier les codes de sortie de `main()` (0 / 1 / 2) selon l'état
   simulé des cibles.

---

## Pièges & indices

- Le point délicat du mocking : substituer la fonction **là où elle est utilisée**
  (`beacon.probe.socket.create_connection`), pas à l'endroit où elle est définie.
- Pour `test_probe_down`, faire en sorte que le faux lève `OSError` : c'est le scénario
  que `probe()` doit absorber pour renvoyer `"down"`.
- Ne pas mocker ce que l'on cherche justement à vérifier. Le mapping up/down est la
  logique testée ; il ne doit pas être contourné.
- `tmp_path` fournit un répertoire propre par test : aucun fichier de config réel n'est requis.

## Livrable

- `tests/test_config.py` + `tests/test_probe.py`, suite verte.
- Beacon est désormais structuré, packagé **et** testé : socle solide pour la suite (réseau,
  cloud, infrastructure), où la frontière mockée aujourd'hui deviendra HTTP réel et SDK cloud.
