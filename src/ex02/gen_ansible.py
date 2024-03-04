# /usr/local/bin/python3.11 -m pip install ansible
# /Users/pickling/Library/Python/3.11/bin/ansible-playbook deploy.yml
import yaml

if __name__ == "__main__":
    todo = "../../materials/todo.yml"

    with open(todo) as f:
        templates = yaml.safe_load(f)

    install_packages = templates['server']['install_packages']
    # exploit_files = templates['server']['exploit_files']
    bad_guys = templates["bad_guys"]



    info = {"hosts" : "localhost"}
    info["connection"] = "local"


    install = {"name": "Install a list of packages"}
    install["apt"] = {"name":"{{ packages }}"};
    packages = {"packages": install_packages}
    install["vars"] = packages


    consumer = {"name": "Execute Python Script consumer.py"}
    exploit = {"name": "Execute Python Script exploit.py"}

    python_start = "python3"

    argv_consumer = {"argv": [python_start, "../ex01/consumer.py", "-e", *bad_guys]}
    argv_exploit = {"argv": [python_start, "../ex00/exploit.py"]}

    consumer["ansible.builtin.command"] = argv_consumer

    exploit["ansible.builtin.shell"] = argv_exploit


    tasks = []
    tasks.append(install)
    tasks.append(exploit)
    tasks.append(consumer)

    info["tasks"] = tasks

    to_yaml = []
    to_yaml.append(info)

    with open('deploy.yml', 'w') as f:
        yaml.dump(to_yaml, f, sort_keys=False)

