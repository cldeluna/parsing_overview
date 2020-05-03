
Python Environment



Ansible Environment

In order to run the Ansible play book you will need an Ansible Control Server.

Ansible Documentation - Installing Ansible
https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html

Once you have your ansible control server, you will need to install the network-engine role and the python textfsm mdoule

ansible-galaxy install ansible-network.network-engine

pip2 install textfsm
pip3 install textfsm

pip2 list | grep textfms
pip3 list | grep textfms

While in the repository directory:

Clone the Network to code TextFSM Template repository so that the path to a template is
./ntc-templates/templates/cisco_nxos_show_ip_route.textfsm
git clone https://github.com/networktocode/ntc-templates.git


ansible-playbook -i hosts get_vrfs.yml --ask-vault-pass -vvvv
