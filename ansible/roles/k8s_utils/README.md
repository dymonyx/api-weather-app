k8s_utils
=========

This role installs and configures essential Kubernetes utilities: `kubelet`, `kubeadm`, and `kubectl`.

Requirements
------------

- Debian-based system with `apt`.
- Internet access to fetch GPG keys and packages.

Role Variables
--------------

### Default Variables (`defaults/main.yml`)

| Variable             | Type   | Default Value | Description |
|----------------------|--------|----------------|-------------|
| `k8s_utils_version` | string | `v1.32`        | Version of Kubernetes to install. |

### Role-Specific Variables (`vars/main.yml`)

| Variable                        | Type   | Description |
|---------------------------------|--------|-------------|
| `k8s_utils_gpg_key`            | string | URL to the Kubernetes apt GPG key. |
| `k8s_utils_keyrings_path`      | string | Directory where GPG keyrings are stored. |
| `k8s_utils_apt_key_asc_path`   | string | Temporary path to the downloaded ASCII GPG key. |
| `k8s_utils_apt_key_gpg_path`   | string | Path where the binary GPG key will be saved. |
| `k8s_utils_repo`               | string | Kubernetes apt repository URL. |

Tasks
-----

- Installs system dependencies required for apt-over-HTTPS.
- Downloads and installs the Kubernetes APT GPG key.
- Adds the official Kubernetes apt repository.
- Installs `kubelet`, `kubeadm`, and `kubectl`.
- Puts the packages on hold to prevent unexpected upgrades.
- Enables and starts the `kubelet` systemd service.
- Reloads systemd units to pick up changes.

Dependencies
------------

None.

Example Playbook
----------------
```
- name: Install Kubernetes utilities
  hosts: all
  become: true
  roles:
    - role: k8s_utils
```
