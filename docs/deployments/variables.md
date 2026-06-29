[Superguitartab.com](../../README.md) >
[Developer documentation](../README.md) >
Variables


# Environment variables

**Superguitartab.com** uses a .env called `.env.tabs-api` file on its virtual machine for storing environment variables and secrets for the API server.

## Deploying environment variables

We use ansible to update our .env file. The playbook is in `infrastructure/ansible/playbooks/environment_variables.yml`. This pushes or updates a `.env.tabs-api` file in our virtual machine.

We run this command in `ansible` root using `ansible-playbook -i hosts.ini playbooks/environment_variables.yml`

This playbook reads `infrastructure/ansible/group_vars/vm01.yml`. This is NOT pushed to the code base as it contains production keys. You must ask team for this file if you wish to edit production environment variables
