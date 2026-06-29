[Superguitartab.com](../../README.md) >
[Developer documentation](../README.md) >
CI/CD (Github Actions)


# CI/CD (Github Actions)

**Superguitartab.com** uses Github Actions for its CI/CD pipelines. The pipelines for superguitartab.com can be found [here](https://github.com/sgmselli/superguitartab.com/actions).

## Our pipelines 

### Deploy pipeline

This pipeline tests, builds, and deploys the application to our production environment when a push is made to the `main` branch

**What this pipeline does (step by step)**:
- Runs tests
- Builds all our docker containers 
- Pushes the docker containers to our Azure Container Registry
- Uses Ansible to:
  - SSH into our virtual machine where our app runs.
  - Push our `docker-compose.production.yml` file
  - Pull our Docker images from our container registry 
  - Rebuild and run our `docker-compose.production.yml` file
 


