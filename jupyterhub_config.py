# Configuration file for Jupyter Hub
c = get_config()

import os

# Base configuration
c.JupyterHub.log_level = "INFO"
c.JupyterHub.db_url = 'sqlite:////srv/jupyterhub_db/jupyterhub.sqlite'
c.JupyterHub.admin_access = True

# Configure the authenticator
c.JupyterHub.authenticator_class = 'docker_oauth.DockerOAuthenticator'
c.GoogleOAuthenticator.oauth_callback_url = os.environ['OAUTH_CALLBACK_URL']
c.GoogleOAuthenticator.oauth_client_id = os.environ['OAUTH_CLIENT_ID']
c.GoogleOAuthenticator.oauth_client_secret = os.environ['OAUTH_CLIENT_SECRET']
c.GoogleOAuthenticator.hosted_domain = os.environ['HOSTED_DOMAIN']
c.LocalAuthenticator.create_system_users = True
c.Authenticator.admin_users = admin = set()
c.Authenticator.whitelist = whitelist = set()

# Configure the spawner
c.JupyterHub.spawner_class = 'swarmspawner.SwarmSpawner'
c.DockerSpawner.container_image = 'compmodels/systemuser'
c.DockerSpawner.tls_cert = os.environ['DOCKER_TLS_CERT']
c.DockerSpawner.tls_key = os.environ['DOCKER_TLS_KEY']
c.DockerSpawner.remove_containers = True
c.DockerSpawner.volumes = {'/srv/nbgrader': '/srv/nbgrader'}

# The docker instances need access to the Hub, so the default loopback port
# doesn't work:
c.JupyterHub.hub_ip = os.environ['HUB_IP']

# Add users to the admin list, the whitelist, and also record their user ids
with open('/srv/jupyterhub_users/userlist') as f:
    for line in f:
        if line.isspace():
            continue
        parts = line.split()
        name = parts[0]
        whitelist.add(name)
        if len(parts) > 1 and parts[1] == 'admin':
            admin.add(name)
