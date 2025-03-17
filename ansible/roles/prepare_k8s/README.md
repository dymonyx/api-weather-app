prepare_k8s
===========

This role prepares nodes for Kubernetes installation by setting up necessary dependencies and configurations.

Requirements
------------

collections:
  - name: community.general


Role Variables
--------------

None.

Dependencies
------------

None.

Tasks Performed
---------------

Enables IP forwarding.

Loads the `br_netfilter` kernel module.

Removes swap entry from `/etc/fstab`.

Checks if swap is enabled and disables it if necessary.

Example Playbook
----------------
```
- name: Preparing for k8s on Ubuntu hosts
  hosts: kube_servers
  roles:
    - role: prepare_k8s
      become: true
```
