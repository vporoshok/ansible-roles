ansible-roles
=============

Collection of ansible roles that I use.

## Install

```sh
git clone git@github.com:vporoshok/ansible-roles.git ~/ansible-roles
```

Edit `~/.ansible.cfg`:

```ini
[defaults]

roles_path = ~/ansible-roles
```

## Use

In project dir create two files:

* `ansible.inv`
```ini
[GROUP_NAME]
host:port
host:port
...

[GROUP_NAME:vars]
user=USER_NAME
hostname=HOST_NAME
```
* `ansible.yml` (just example)
```yaml
- hosts: all
  remote_user: USER_NAME
  sudo_user: SUDO_USER
  roles:
    - { role: default, tags: ['def'] }
  tasks:
    - name: project packages
      apt: pkg={{ item }}
      with_items:
        - nginx
      tags: pkg
```

After this just run in project dir:

```sh
ansible-playbook -i ansible.inv ansible.yaml
```
