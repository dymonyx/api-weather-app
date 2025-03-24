k8s_master_init
===============

This role initializes the Kubernetes control plane on the master node using `kubeadm init`.

Requirements
------------

- This role must run on the node designated as the Kubernetes master.
- The CRI runtime (e.g., CRI-O or containerd) must be properly configured and running.
- The specified network interface (e.g., `ansible_ens3`) must be defined in Ansible facts.

Role Variables
--------------

### Default Variables (`defaults/main.yml`)
| Variable                       | Type   | Default Value     | Description |
|--------------------------------|--------|-------------------|-------------|
| `k8s_master_init_pod_cidr`     | string | `192.168.0.0/16`  | Pod network CIDR used by the CNI plugin. |
| `k8s_master_init_service_cidr` | string | `10.96.0.0/12`    | Kubernetes service CIDR. |

### Role-Specific Variables (`vars/main.yml`)
| Variable                            | Type   | Default Value                   | Description |
|-------------------------------------|--------|----------------------------------|-------------|
| `k8s_master_init_admin_config_path` | string | `/etc/kubernetes/admin.conf`    | Path to admin kubeconfig created by `kubeadm`. |
| `k8s_master_init_kubeconfig_dest`   | string | `/root/.kube/config`            | Destination for copied kubeconfig. |
| `k8s_master_init_log_path`          | string | `/root/kubeadm-init.log`        | Log file path for the output of `kubeadm init`. |
| `k8s_master_init_kube_dir`          | string | `/root/.kube`                   | Directory to store kubeconfig. |

Tasks
-----

- Initializes the Kubernetes control plane with specific pod and service CIDRs.
- Saves the initialization output to a log file.
- Configures admin kubeconfig for the root user.

Dependencies
------------

- Container runtime (e.g., CRI-O) must be configured and available.
- DNS resolution and internet access for image pulling (unless using a local registry).

Example Playbook
----------------
```
- name: Initialize Kubernetes master node
  hosts: master
  become: true
  roles:
    - role: k8s_master_init
```
