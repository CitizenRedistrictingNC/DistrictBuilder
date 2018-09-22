Summary
=======

An [ansible](http://ansible.com) playbook to maintain districtbuilder on AWS.

Setup
-----

```
mkvirtualenv -p `which python3` districtbuilder

pip install -r requirements.txt
ansible-galaxy install -r requirements.yml
```

Setup
-----

Pre-requisites:

 * An EC2 Keypair: create one from the AWS console, and add it to vars/aws.yml
   -- share this with other developers that can setup dokku.
 * You will also need the vault password for some passwords stored in ansible.
   Ask another developer for it.

Run the provision.yml ansible script and setup docker-machine to point to the new
EC2 instance:

```
ansible-playbook provision.yml
```

You can modify the variables in `var/aws.yml` to access to the
server, its stack, and hostname.

Deploy
------

Once a server has been set up, you can use the following script to deploy the
districtbuilder application:

```
ansible-playbook deploy.yml
```

Teardown
--------

To remove the server and all the resources execute the teardown script:

```
ansible-playbook teardown.yml
```
