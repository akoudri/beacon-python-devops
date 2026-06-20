#!/usr/bin/python
"""Module Ansible custom : exécute `beacon check` et renvoie son verdict.

C'est le point de jonction réel entre Python et Ansible : un module est un
programme Python qui lit des arguments (via `AnsibleModule`) et renvoie un
résultat JSON (`exit_json` / `fail_json`). Il ne modifie rien — `changed`
reste à `false` (une sonde est une lecture).

Usage dans un playbook :

    - name: Lire l'état des cibles
      beacon_status:
        beacon_bin: "{{ beacon_venv }}/bin/beacon"
        config: "{{ beacon_config_dir }}/targets.yaml"
      register: result
"""

from __future__ import annotations

from ansible.module_utils.basic import AnsibleModule


def main() -> None:
    module = AnsibleModule(
        argument_spec={
            "beacon_bin": {"type": "str", "required": True},
            "config": {"type": "str", "required": True},
        },
        supports_check_mode=True,
    )

    beacon_bin = module.params["beacon_bin"]
    config = module.params["config"]

    # En check mode, ne rien exécuter : on déclare juste l'absence de changement.
    if module.check_mode:
        module.exit_json(changed=False, skipped=True)

    rc, stdout, stderr = module.run_command(
        [beacon_bin, "check", "--config", config, "--format", "json"]
    )

    # Convention CLI de Beacon : 0 = tout up, 1 = au moins une down, 2 = erreur.
    # NB : on n'expose pas la clé top-level `rc` (Ansible la traite spécialement
    # et ferait échouer la tâche sur un code non nul) ; on la nomme `exit_code`.
    if rc == 2:
        module.fail_json(msg=f"beacon a échoué : {stderr.strip()}", exit_code=rc)

    module.exit_json(changed=False, exit_code=rc, all_up=(rc == 0), report=stdout)


if __name__ == "__main__":
    main()
