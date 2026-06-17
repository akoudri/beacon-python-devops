# Lab 2 — Beacon sonde en local

**Durée :** ~40 min · **Mode :** auto-rythmé
**Module Beacon visé :** `probe.py`

---

## Contexte

Beacon sait désormais *quoi* surveiller (Lab 1). Il faut maintenant *sonder* : ouvrir une
connexion vers chaque cible, mesurer la latence, et traduire le résultat brut en un statut
exploitable. Le point clé du lab : ne **jamais** renvoyer une chaîne libre, mais un
**résultat structuré** que les modules suivants (report, métriques) pourront consommer.

À la fin, vous exposez :

```python
def probe(target: Target) -> ProbeResult:
    ...
```

## Prérequis

- Le `config.py` du Lab 1 qui fournit des objets `Target`.
- Une cible TCP joignable en local pour tester (un simple
  `python -m http.server 8080` fera l'affaire).

---

## SOCLE — à réaliser par tous

### Énoncé

1. Dans `beacon/probe.py`, définissez une `@dataclass ProbeResult` :

   ```python
   @dataclass
   class ProbeResult:
       target: str
       status: str        # "up" | "down"
       latency_ms: float
       checked_at: str    # horodatage ISO 8601
   ```

2. Écrivez `probe(target)` qui :
   - mesure le temps avec `time.perf_counter()` (départ avant la connexion) ;
   - tente une connexion TCP : `socket.create_connection((host, port), timeout=2)` ;
   - en cas de succès → `status = "up"` ; sur `OSError` → `status = "down"` ;
   - calcule `latency_ms` et renseigne `checked_at`
     (`datetime.now(timezone.utc).isoformat()`).

3. Vérifiez le comportement sur **deux cas** : une cible up (votre `http.server`) et une
   cible down (un port fermé).

### Critères de réussite (socle)

- [ ] `probe(target)` renvoie un `ProbeResult`, jamais une chaîne ni un tuple nu.
- [ ] Une cible joignable donne `status == "up"` avec une latence plausible.
- [ ] Une cible injoignable donne `status == "down"` **sans lever d'exception**.
- [ ] `probe.py` n'importe ni `config` (à part le type `Target`) ni la CLI : responsabilité unique.

---

## EXTENSION — si vous avancez

1. **Timeout par cible.** Ajoutez un champ `timeout` optionnel au `Target` et utilisez-le.
2. **Retries.** Réessayez une fois après un court délai (`time.sleep`) avant de conclure `down`.
3. **Sondage de toutes les cibles.** Écrivez `probe_all(targets) -> list[ProbeResult]` qui
   parcourt la config proprement (gestion individuelle des échecs : une cible down ne doit
   pas interrompre les autres).
4. **Mini-rapport.** Agrègez un résumé : `n up`, `n down`, latence médiane. (Ne formatez pas
   encore pour l'humain — ça, c'est pour `report.py`, plus tard.)

---

## Pièges & indices

- Démarrez le chrono **avant** le `try`, arrêtez-le dans les deux branches : vous voulez la latence
  même en échec rapide (refus immédiat ≠ timeout).
- `create_connection` lève `OSError` (dont `ConnectionRefusedError`, `socket.timeout`) :
  une seule clause `except OSError` couvre les cas réseau usuels.
- Pensez à **fermer** la socket en cas de succès (`with` ou `.close()`).
- Gardez `probe()` *pur* du point de vue I/O console : pas de `print`. Il renvoie une donnée ;
  l'affichage est la responsabilité d'un autre module.

## Livrable

- `beacon/probe.py` (avec `ProbeResult`).
- Conservez l'ensemble : lors des prochains labs, on emballe `config` + `probe` derrière une CLI
  (`argparse`), on package le tout, et on écrit les **tests** — en mockant précisément la
  socket pour ne pas dépendre du réseau réel.
