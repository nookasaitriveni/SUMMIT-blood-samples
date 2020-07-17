# SUMMIT-blood-samples 

## Deploy

### Requirements
* [docker-engine](https://docs.docker.com/engine/install/centos/)
* [docker-compose](https://docs.docker.com/compose/install/)

### Source
Deploy from **master** branch 

### Configuration
Application configuration files:  

`$ mkdir -p summit_blood_samples/.envs/.production`  
`$ vim summit_blood_samples/.envs/.production/.django`  

      # General
      # -----------------------------------------------
      USE_DOCKER=yes
      IPYTHONDIR=/app/.ipython

`$ vim summit_blood_samples/.envs/production/.postgres`  

    # PostgreSQL
    # ------------------------------------------------
    POSTGRES_HOST=postgres
    POSTGRES_PORT=5432
    POSTGRES_DB=summit_blood_samples
    POSTGRES_USER=<secret-username>
    POSTGRES_PASSWORD=<secret-password>

### Build & Run
`$ docker-compose -f production.yml up --build`

### Stop
`$ docker-compose -f production.yml down`

-----
### Clean up
**NB: the *-v* option will remove all volumes as well**  
`$ docker-compose -f production.yml down --remove-orphans  -v`
