### Weather-Points

First of all you need to create your own .env file which should looks like the .env.dist file given.

Once you have created your own env file, you'll need to build and start your docker containers
```
docker-compose up -d --build
```
You'll need also to upgrade your database schema using Alembic running the following command:
```
docker-compose exec api alembic upgrade head
```
