kubelet
=======

This role configures the Kubelet and CRI-O runtime on target nodes.

Requirements
------------

- Kubelet must be installed.
- CRI-O must be installed and configured.

Role Variables
--------------

### Role-Specific Variables (`vars/main.yml`)

| Variable                  | Type   | Default Value                  | Description |
|---------------------------|--------|--------------------------------|-------------|
| `kubelet_config_path`     | string | `/etc/default/kubelet`         | Path to the Kubelet extra arguments configuration. |
| `kubelet_runtime_config_path` | string | `/var/lib/kubelet/config.yaml` | Path to the Kubelet runtime configuration file. |
| `kubelet_runtime_socket`  | string | `unix:///var/run/crio/crio.sock` | Path to the CRI socket used by Kubelet. |

Tasks
-----

- Configures the Kubelet to use the CRI-O runtime by setting `containerRuntimeEndpoint`.
- Sets `--node-ip` in `KUBELET_EXTRA_ARGS` based on the default interface IP.
- Ensures proper CRI-O runtime configuration:
  - Removes duplicate `[crio.runtime]` sections in `10-crio.conf`.
  - Inserts a managed block with required runtime capabilities (`NET_RAW`, etc.).

Handlers
--------

- `Restart Kubelet service`
- `Restart CRI-O service`

Dependencies
------------

None.

Example Playbook
----------------
```
- name: Configure kubelet and CRI-O
  hosts: all
  become: true
  roles:
    - role: kubelet
```
