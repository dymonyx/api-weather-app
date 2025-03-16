k8s
=========

This role installs and configures Kubernetes components (kubelet, kubeadm, and kubectl) on target nodes.

Requirements
------------

None.

Role Variables
--------------
### Default Variables (`defaults/main.yml`)
| Variable       | Type   | Default Value | Description |
|---------------|--------|--------------|-------------|
| `k8s_version` | string | `v1.32` | Defines the Kubernetes version to install. |

### Role-Specific Variables (`vars/main.yml`)
| Variable                     | Type   | Default Value | Description |
|------------------------------|--------|--------------|-------------|
| `k8s_gpg_key`               | string | `"https://pkgs.k8s.io/core:/stable:/{{ k8s_version }}/deb/Release.key"` | URL of the GPG key used to verify the Kubernetes package. |
| `k8s_keyrings_path`         | string | `/etc/apt/keyrings` | Directory path where keyrings are stored. |
| `k8s_apt_key_asc_path`      | string | `/etc/apt/keyrings/kubernetes-apt-keyring.asc` | Path to the ASCII-format GPG key for Kubernetes. |
| `k8s_apt_key_gpg_path`      | string | `/etc/apt/keyrings/kubernetes-apt-keyring.gpg` | Path to the binary-format GPG key for Kubernetes. |
| `k8s_repo`                  | string | `"https://pkgs.k8s.io/core:/stable:/{{ k8s_version }}/deb/"` | Repository URL for installing Kubernetes packages. |

Dependencies
------------

- role: prepare_k8s

Special Tasks
-------------

This role includes a task that runs kubeadm init only on the first node to initialize the Kubernetes cluster - `kubeadm_init`.

Example Playbook
----------------
```
- name: Install k8s on Ubuntu hosts
  hosts: kube_servers
  roles:
    - role: k8s
      become: true
```
