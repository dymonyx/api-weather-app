crio
=========

This Ansible role installs and configures CRI-O, a lightweight container runtime for Kubernetes.

Requirements
------------

None.

Role Variables
--------------

### Default Variables (`defaults/main.yml`)
These variables have default values but can be overridden if needed.

| Variable       | Type   | Default Value | Description |
|---------------|--------|--------------|-------------|
| `crio_version` | string | `v1.32` | Defines the version of CRI-O to install. |

### Role-Specific Variables (`vars/main.yml`)
These variables are predefined and typically should not be changed unless customization is required.

| Variable                     | Type   | Default Value | Description |
|------------------------------|--------|--------------|-------------|
| `crio_gpg_key`               | string | `"https://download.opensuse.org/repositories/isv:/cri-o:/stable:/{{ crio_version }}/deb/Release.key"` | URL of the GPG key used to verify the CRI-O package. |
| `crio_keyrings_path`         | string | `/etc/apt/keyrings` | Directory path where keyrings are stored. |
| `crio_apt_key_asc_path`      | string | `/etc/apt/keyrings/cri-o-apt-keyring.asc` | Path to the ASCII-format GPG key for CRI-O. |
| `crio_apt_key_gpg_path`      | string | `/etc/apt/keyrings/cri-o-apt-keyring.gpg` | Path to the binary-format GPG key for CRI-O. |
| `crio_repo`                  | string | `"https://download.opensuse.org/repositories/isv:/cri-o:/stable:/{{ crio_version }}/deb/"` | Repository URL for installing CRI-O packages. |
| `crio_config_path`           | string | `/etc/crio/crio.conf` | Path to the CRI-O configuration file. |

Dependencies
------------

None.

Example Playbook
----------------
```
- name: Install CRI-O on Ubuntu hosts
  hosts: kube_servers
  roles:
    - role: crio
      become: true
```
