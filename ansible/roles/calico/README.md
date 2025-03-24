calico
=========

This role deploys [Project Calico](https://www.tigera.io/project-calico/) as the Container Network Interface (CNI) for Kubernetes, including the Tigera Operator and custom resources configuration.

Requirements
------------

None.

Role Variables
--------------

### Default Variables (`defaults/main.yml`)

| Variable                      | Type   | Default Value              | Description                                     |
|-------------------------------|--------|-----------------------------|-------------------------------------------------|
| `calico_custom_resources_path` | string | `/root/custom-resources.yaml` | Path where Calico's `custom-resources.yaml` will be saved. |
| `calico_cidr`                 | string | `192.168.0.0/16`           | CIDR range for pod networking.                 |

### Role-Specific Variables (`vars/main.yml`)

| Variable                      | Type   | Default Value                                                                 | Description                                       |
|------------------------------|--------|------------------------------------------------------------------------------|---------------------------------------------------|
| `calico_tigera_operator_url` | string | `https://raw.githubusercontent.com/projectcalico/calico/v3.25.2/manifests/tigera-operator.yaml` | URL to the Tigera Operator manifest.              |
| `calico_custom_resources_url` | string | `https://raw.githubusercontent.com/projectcalico/calico/v3.25.2/manifests/custom-resources.yaml` | URL to the Calico custom resources manifest.      |

Dependencies
------------

None.

Special tasks
----------------

This role:
- Fetches and deploys the Tigera Operator
- Downloads and patches the Calico custom resources with the configured CIDR
- Deploys the custom resources to the Kubernetes cluster

Example Playbook
----------------

```
- name: Deploy Calico CNI
  hosts: master
  roles:
    - role: calico
      become: true
```