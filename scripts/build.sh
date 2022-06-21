/usr/local/bin/alembic upgrade head & \
/usr/local/bin/python3.9 app/db/init_db.py & \
/usr/local/bin/gunicorn -c gunicorn_conf.py app.main:api
