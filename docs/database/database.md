[Superguitartab.com](../../README.md) >
[Developer documentation](../README.md) >
Database

# Database

We use PostgreSQL for our relational database 

## Production database

Our production database runs on Azure Database for Postgres.

## Migrations

Migrations are ran using `alembic`. These run [here](../../tabs-api/run.sh) using commands:
- alembic -c app/db/migrations/alembic.ini revision --autogenerate (makes migrations)
- alembic -c app/db/migrations/alembic.ini upgrade head (migrates changes)

We leave `alembic -c app/db/migrations/alembic.ini revision --autogenerate (makes migrations)` commented out as we make our migration files outside of docker.

To make a migration

1. Ensure you set up your own local postgres database on your local machine using psql.
2. Run `docker compose down` in compose folder so docker app isn't running
3. Change `.env` file so your `DATABASE_HOST=localhost`
4. At tabs-api run migration commands (should successfully run and create new migration version file in `tabs-api/app/db/migrations/versions`)
5. Change `.env` file back so your `DATABASE_HOST=guitartabsdb`
6. Start app up using Docker with `alembic -c app/db/migrations/alembic.ini upgrade head (migrates changes)` uncommented in `run.sh`.

Migration should be applied!