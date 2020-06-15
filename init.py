import os, jinja2
hostIP = os.environ['HOST_IP']
namespace = os.environ['NAMESPACE']
temploader = jinja2.FileSystemLoader(searchpath="./")
env = jinja2.Environment(loader=temploader)
template = env.get_template('oc-agent-config.yaml')
out = template.render(namespace=namespace, host_ip=hostIP)
print(out)
