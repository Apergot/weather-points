### Weather-Points

Execute next command to create needed .env file and remember to update it with your own weatherapi api key:
```
make init
```
Once you have created your own env file, you'll need to build and start your docker containers
```
make build
```
You'll need also to upgrade your database schema using Alembic running the following command:
```
make upgrade_migrations
```
