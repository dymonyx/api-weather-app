k8s_prepare_join
================

This role generates or reuses a valid `kubeadm join` command for worker nodes to join the Kubernetes cluster.

Requirements
------------

- This role should run on the control-plane (master) node.
- The Kubernetes control plane should already be initialized using `kubeadm init`.

Role Variables
--------------

None.

Internal Facts (set during execution):
---------------------------------------

| Variable                 | Description |
|--------------------------|-------------|
| `master_ip`              | IP address of the control-plane node. |
| `existing_token`         | First valid bootstrap token, if any exist. |
| `valid_tokens`           | List of all valid bootstrap tokens. |
| `has_valid_token`        | Boolean indicating if there are any reusable tokens. |
| `ca_cert_hash`           | Hash of the CA certificate used for secure node joining. |
| `kubeadm_join_cmd_final` | Full `kubeadm join` command constructed or retrieved. |

Tasks
-----

- Verifies if reusable `kubeadm` tokens exist.
- Generates a new token and full `kubeadm join` command if none found.
- Extracts CA certificate hash.
- Assembles the final `kubeadm join` command and exposes it via a fact (`kubeadm_join_cmd_final`).
- Optionally prints the join command for debugging.

Dependencies
------------

- Role must run after the Kubernetes control plane has been initialized.

Example Playbook
----------------
```
- name: Prepare kubeadm join command
  hosts: master
  become: true
  roles:
    - role: k8s_prepare_join
```
