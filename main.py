import database_sql
import http_server
import os
import urlparse
import website
import traceback

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

app = http_server.http_server

if __name__ == "__main__":
    '''urlparse.uses_netloc.append("postgres")
    url = urlparse.urlparse('postgres://atpktzavrimtkk:Ae0yXoLQxGKyUW71aJPPRI9sYn@ec2-184-73-251-115.compute-1.amazonaws.com:5432/de284v11vmiva3')
    db = database_sql.database_sql()
    db.init_postgresql(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )'''

    '''    db = database_sql.database_sql()
    db.init_sqlite('temp/db')
    http_server.website.db = db
    api.db = db'''

    try:
        db = database_sql.database_sql()
        db.init_postgresql(
            database='ishopdb',
            user='user5',
            password='123',
            host='127.0.0.1',
            port='5432'
        )

        website.db = db
        http_server.db = db

        app.run(host = '0.0.0.0')
    except Exception as e:
        print traceback.format_exc()
    
else:
    #heroku config:
    try:
        urlparse.uses_netloc.append("postgres")
        url = urlparse.urlparse(os.environ["DATABASE_URL"])
        db = database_sql.database_sql()
        db.init_postgresql(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
        website.db = db
        http_server.db = db
    except Exception as e:
        print traceback.format_exc()
