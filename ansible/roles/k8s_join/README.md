k8s_join
=========

This role joins worker nodes to an existing Kubernetes cluster using a shared `kubeadm join` command.

Requirements
------------

- Kubernetes master node must be already initialized and accessible.
- The variable `kubeadm_join_cmd_final` must be set on the master host.

Role Variables
--------------
### Default Variables (`defaults/main.yml`)
| Variable                  | Type   | Default Value                        | Description                                |
|---------------------------|--------|--------------------------------------|--------------------------------------------|
| `k8s_join_kubelet_config` | string | `/etc/kubernetes/kubelet.conf`       | Path used to determine if the node is already joined to the cluster. |

### Role-Specific Variables (`vars/main.yml`)
None.

Tasks
------

- **Share Join Command:** Sets `kubeadm_join_cmd_final` on worker nodes by reading it from the master node.
- **Join Worker Node:** Executes the join command to attach the node to the cluster (only if not already joined).

Dependencies
------------

- role: `k8s_master_init` (or any role that initializes the cluster and generates `kubeadm_join_cmd_final`)

Example Playbook
----------------
```
- name: Join worker nodes to Kubernetes cluster
  hosts: workers
  become: true
  roles:
    - role: k8s_join
```
