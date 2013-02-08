# -*- coding: utf-8 -*-
import os
import unittest

import parsnip


class BaseTestCase(unittest.TestCase):
    parser = None

class MemcacheTestCase(BaseTestCase):
    pass

class MongoDBTestCase(BaseTestCase):
    parser = parsnip.mongodb.parser

    def test_mongodb(self):
        url = 'mongodb://uname:pword@mongodb.com:27017/test'
        config = self.parser.parse(url)

        self.assertEqual(config['MONGODB_USER'], 'uname')
        self.assertEqual(config['MONGODB_PASSWORD'], 'pword')
        self.assertEqual(config['MONGODB_HOST'], 'mongodb.com')
        self.assertEqual(config['MONGODB_PORT'], 27017)
        self.assertEqual(config['MONGODB_DB'], 'test')

    def test_mongodb_unauthenticated(self):
        url = 'mongodb://@mongodb.com:27017/test'
        config = self.parser.parse(url)
        
        self.assertEqual(config['MONGODB_USER'], None)
        self.assertEqual(config['MONGODB_PASSWORD'], None)
        self.assertEqual(config['MONGODB_HOST'], 'mongodb.com')
        self.assertEqual(config['MONGODB_PORT'], 27017)
        self.assertEqual(config['MONGODB_DB'], 'test')

    def test_mongo(self):
        url = 'mongo://uname:pword@mongodb.com:27017/test'
        config = self.parser.parse(url)

        self.assertEqual(config['MONGODB_USER'], 'uname')
        self.assertEqual(config['MONGODB_PASSWORD'], 'pword')
        self.assertEqual(config['MONGODB_HOST'], 'mongodb.com')
        self.assertEqual(config['MONGODB_PORT'], 27017)
        self.assertEqual(config['MONGODB_DB'], 'test')

    def test_mongo_unauthenticated(self):
        url = 'mongo://@mongodb.com:27017/test'
        config = self.parser.parse(url)
        
        self.assertEqual(config['MONGODB_USER'], None)
        self.assertEqual(config['MONGODB_PASSWORD'], None)
        self.assertEqual(config['MONGODB_HOST'], 'mongodb.com')
        self.assertEqual(config['MONGODB_PORT'], 27017)
        self.assertEqual(config['MONGODB_DB'], 'test')



class ParsnipTestCase(BaseTestCase):
    pass


class DjangoDatabaseTestCase(BaseTestCase):
    parser = parsnip.django.db

    def test_postgres(self):
        url = 'postgres://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722r2kuvn'
        config = self.parser.parse(url)

        self.assertEqual(config['ENGINE'], 'django.db.backends.postgresql_psycopg2')
        self.assertEqual(config['NAME'], 'd8r82722r2kuvn')
        self.assertEqual(config['HOST'], 'ec2-107-21-253-135.compute-1.amazonaws.com')
        self.assertEqual(config['USER'], 'uf07k1i6d8ia0v')
        self.assertEqual(config['PASSWORD'], 'wegauwhgeuioweg')
        self.assertEqual(config['PORT'], 5431)

    def test_postgresql(self):
        url = 'postgresql://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722r2kuvn'
        config = self.parser.parse(url)

        self.assertEqual(config['ENGINE'], 'django.db.backends.postgresql_psycopg2')
        self.assertEqual(config['NAME'], 'd8r82722r2kuvn')
        self.assertEqual(config['HOST'], 'ec2-107-21-253-135.compute-1.amazonaws.com')
        self.assertEqual(config['USER'], 'uf07k1i6d8ia0v')
        self.assertEqual(config['PASSWORD'], 'wegauwhgeuioweg')
        self.assertEqual(config['PORT'], 5431)

    def test_postgis(self):
        url = 'postgis://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722r2kuvn'
        config = self.parser.parse(url)

        self.assertEqual(config['ENGINE'], 'django.contrib.gis.db.backends.postgis')
        self.assertEqual(config['NAME'], 'd8r82722r2kuvn')
        self.assertEqual(config['HOST'], 'ec2-107-21-253-135.compute-1.amazonaws.com')
        self.assertEqual(config['USER'], 'uf07k1i6d8ia0v')
        self.assertEqual(config['PASSWORD'], 'wegauwhgeuioweg')
        self.assertEqual(config['PORT'], 5431)

    def test_mysql(self):
        url = 'mysql://bea6eb025ca0d8:69772142@us-cdbr-east.cleardb.com/heroku_97681db3eff7580?reconnect=true'
        config = self.parser.parse(url)

        self.assertEqual(config['ENGINE'], 'django.db.backends.mysql')
        self.assertEqual(config['NAME'], 'heroku_97681db3eff7580')
        self.assertEqual(config['HOST'], 'us-cdbr-east.cleardb.com')
        self.assertEqual(config['USER'], 'bea6eb025ca0d8')
        self.assertEqual(config['PASSWORD'], '69772142')
        self.assertEqual(config['PORT'], None)

    def test_mysql2(self):
        url = 'mysql2://bea6eb025ca0d8:69772142@us-cdbr-east.cleardb.com/heroku_97681db3eff7580?reconnect=true'
        config = self.parser.parse(url)

        self.assertEqual(config['ENGINE'], 'django.db.backends.mysql')
        self.assertEqual(config['NAME'], 'heroku_97681db3eff7580')
        self.assertEqual(config['HOST'], 'us-cdbr-east.cleardb.com')
        self.assertEqual(config['USER'], 'bea6eb025ca0d8')
        self.assertEqual(config['PASSWORD'], '69772142')
        self.assertEqual(config['PORT'], None)

    def test_sqlite_relative(self):
        url = 'sqlite:///default.db'
        config = self.parser.parse(url)

        self.assertEqual(config['ENGINE'], 'django.db.backends.sqlite3')
        self.assertEqual(config['NAME'], 'default.db')
        self.assertEqual(config['HOST'], None)
        self.assertEqual(config['USER'], None)
        self.assertEqual(config['PASSWORD'], None)
        self.assertEqual(config['PORT'], None)

    def test_sqlite_absolute(self):
        url = 'sqlite:////home/user/Desktop/default.db'
        config = self.parser.parse(url)

        self.assertEqual(config['ENGINE'], 'django.db.backends.sqlite3')
        self.assertEqual(config['NAME'], '/home/user/Desktop/default.db')
        self.assertEqual(config['HOST'], None)
        self.assertEqual(config['USER'], None)
        self.assertEqual(config['PASSWORD'], None)
        self.assertEqual(config['PORT'], None)

    def test_parse_from(self):
        config = self.parser.parse_from()
        self.assertTrue(not config)

        os.environ['DATABASE_URL'] = 'postgres://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722r2kuvn'

        config = self.parser.parse_from()

        self.assertEqual(config['ENGINE'], 'django.db.backends.postgresql_psycopg2')
        self.assertEqual(config['NAME'], 'd8r82722r2kuvn')
        self.assertEqual(config['HOST'], 'ec2-107-21-253-135.compute-1.amazonaws.com')
        self.assertEqual(config['USER'], 'uf07k1i6d8ia0v')
        self.assertEqual(config['PASSWORD'], 'wegauwhgeuioweg')
        self.assertEqual(config['PORT'], 5431)


class DjangoCacheTestCase(BaseTestCase):
    parser = parsnip.django.cache

    def test_db(self):
        url = 'db://super_caching_table'
        config = self.parser.parse(url)

        self.assertEquals(config['BACKEND'], 'django.core.cache.backends.db.DatabaseCache')
        self.assertEquals(config['LOCATION'], 'super_caching_table')

    def test_dummy(self):
        url = 'dummy://'
        config = self.parser.parse(url)

        self.assertEquals(config['BACKEND'], 'django.core.cache.backends.dummy.DummyCache')

    def test_file(self):
        url = 'file:///herp'
        config = self.parser.parse(url)

        self.assertEquals(config['BACKEND'], 'django.core.cache.backends.filebased.FileBasedCache')
        self.assertEquals(config['LOCATION'], '/herp')

    def test_locmem(self):
        url = 'locmem://'
        config = self.parser.parse(url)

        self.assertEquals(config['BACKEND'], 'django.core.cache.backends.locmem.LocMemCache')

    def test_memcached(self):
        url = 'memcached://127.0.0.1:11211/prefix'
        config = self.parser.parse(url)

        self.assertEquals(config['BACKEND'], 'django.core.cache.backends.memcached.MemcachedCache')
        self.assertEquals(config['LOCATION'], ['127.0.0.1:11211'])
        self.assertEquals(config['KEY_PREFIX'], 'prefix')

    def test_memcached_multiserver(self):
        os.environ['MEMCACHED_USERNAME'] = 'mchammer'
        os.environ['MEMCACHED_PASSWORD'] = 'pword'
        os.environ['MEMCACHED_SERVERS'] = '127.0.0.1:11211 127.0.0.1:11212 127.0.0.1:11213'

        config = self.parser.config()

        self.assertEquals(config['BACKEND'], 'django.core.cache.backends.memcached.PyLibMCCache')
        self.assertIsInstance(config['LOCATION'], list)
        self.assertEquals(config['LOCATION'], ['127.0.0.1:11211', '127.0.0.1:11212', '127.0.0.1:11213'])
        # self.assertEquals(config['KEY_PREFIX'], 'prefix')

    def test_pymemcached(self):
        url = 'pymemcached://127.0.0.1:11211/prefix'
        config = self.parser.parse(url)

        self.assertEquals(config['BACKEND'], 'django.core.cache.backends.memcached.PyLibMCCache')
        self.assertEquals(config['LOCATION'], ['127.0.0.1:11211'])
        self.assertEquals(config['KEY_PREFIX'], 'prefix')

    def test_djangopylibmc(self):
        url = 'djangopylibmc://127.0.0.1:11211/prefix'
        config = self.parser.parse(url)

        self.assertEquals(config['BACKEND'], 'django_pylibmc.memcached.PyLibMCCache')
        self.assertEquals(config['LOCATION'], ['127.0.0.1:11211'])
        self.assertEquals(config['KEY_PREFIX'], 'prefix')


class MongoHQTestCase(BaseTestCase):
    parser = parsnip.mongodb.parser

    def setUp(self):
        os.environ['MONGOHQ_URL'] = 'mongodb://heroku:pword@alex.mongohq.com:10037/app000000'

    def test_parse_from(self):
        config = self.parser.parse_from('MONGOHQ_URL')

        self.assertEqual(config['MONGODB_USER'], 'heroku')
        self.assertEqual(config['MONGODB_PASSWORD'], 'pword')
        self.assertEqual(config['MONGODB_HOST'], 'alex.mongohq.com')
        self.assertEqual(config['MONGODB_PORT'], 10037)
        self.assertEqual(config['MONGODB_DB'], 'app000000')


class MongoLabTestCase(BaseTestCase):
    parser = parsnip.mongodb.parser

    def setUp(self):
        os.environ['MONGOLAB_URI'] = 'mongodb://heroku_app1234:random_password@ds029017.mongolab.com:29017/heroku_app1234'

    def test_parse_from(self):
        config = self.parser.parse_from('MONGOLAB_URI')

        self.assertEqual(config['MONGODB_USER'], 'heroku_app1234')
        self.assertEqual(config['MONGODB_PASSWORD'], 'random_password')
        self.assertEqual(config['MONGODB_HOST'], 'ds029017.mongolab.com')
        self.assertEqual(config['MONGODB_PORT'], 29017)
        self.assertEqual(config['MONGODB_DB'], 'heroku_app1234')

class RedisTestCase(BaseTestCase):
    parser = parsnip.redis.parser

    def test(self):
        url = 'redis://redis:12346456456@127.0.0.1:9092/'
        config = self.parser.parse(url)

        self.assertEqual(config['REDIS_HOST'], '127.0.0.1')
        self.assertEqual(config['REDIS_PORT'], 9092)
        self.assertEqual(config['REDIS_USER'], 'redis')
        self.assertEqual(config['REDIS_PASSWORD'], '12346456456')

    def test_unauthenticated(self):
        url = 'redis://@127.0.0.1:9092/'
        config = self.parser.parse(url)

        self.assertEqual(config['REDIS_HOST'], '127.0.0.1')
        self.assertEqual(config['REDIS_PORT'], 9092)
        self.assertEqual(config['REDIS_USER'], None)
        self.assertEqual(config['REDIS_PASSWORD'], None)


class RedisToGoTestCase(RedisTestCase):
    def setUp(self):
        os.environ['REDISTOGO_URL'] = 'redis://redistogo:44ec0bc04dd4a5afe77a649acee7a8f3@drum.redistogo.com:9092/'

    def test_parse_from(self):
        config = self.parser.parse_from('REDISTOGO_URL')

        self.assertEqual(config['REDIS_HOST'], 'drum.redistogo.com')
        self.assertEqual(config['REDIS_PORT'], 9092)
        self.assertEqual(config['REDIS_USER'], 'redistogo')
        self.assertEqual(config['REDIS_PASSWORD'], '44ec0bc04dd4a5afe77a649acee7a8f3')


class SentryTestCase(BaseTestCase):
    parser = parsnip.sentry.parser
    
    def setUp(self):
        os.environ['SENTRY_DSN'] = 'https://random_key:random_password@getsentry.com/1'

    def test(self):
        config = self.parser.config()
        ig.setdefault('SENTRY_DSN', environ.get('SENTRY_DSN'))

# class SQLAlchemyTestCase(BaseTestCase):
#     def test(self):
#         app.config.setdefault('SQLALCHEMY_DATABASE_URI', environ.get('DATABASE_URL'))

# class ExceptionalTestCase(BaseTestCase):
#     def test(self):
#         app.config.setdefault('EXCEPTIONAL_API_KEY', environ.get('EXCEPTIONAL_API_KEY'))

# class GoogleFedTestCase(BaseTestCase):
#     def test(self):
#         app.config.setdefault('GOOGLE_DOMAIN', environ.get('GOOGLE_DOMAIN'))

# class CeleryTestCase(BaseTestCase):
#     def test(self):
#         app.config.setdefault('BROKER_URL', environ.get('RABBITMQ_URL'))

# class MailgunTestCase(BaseTestCase):
#     def test(self):
#         if 'MAILGUN_SMTP_SERVER' in environ:
#         app.config.setdefault('SMTP_SERVER', environ.get('MAILGUN_SMTP_SERVER'))
#         app.config.setdefault('SMTP_LOGIN', environ.get('MAILGUN_SMTP_LOGIN'))
#         app.config.setdefault('SMTP_PASSWORD', environ.get('MAILGUN_SMTP_PASSWORD'))
#         app.config.setdefault('MAIL_SERVER', environ.get('MAILGUN_SMTP_SERVER'))
#         app.config.setdefault('MAIL_USERNAME', environ.get('MAILGUN_SMTP_LOGIN'))
#         app.config.setdefault('MAIL_PASSWORD', environ.get('MAILGUN_SMTP_PASSWORD'))
#         app.config.setdefault('MAIL_USE_TLS', True)

# class SendGridTestCase(BaseTestCase):
#     def test(self):
#         if 'SENDGRID_USERNAME' in environ:
#             app.config.setdefault('SMTP_SERVER', 'smtp.sendgrid.net')
#             app.config.setdefault('SMTP_LOGIN', environ.get('SENDGRID_USERNAME'))
#             app.config.setdefault('SMTP_PASSWORD', environ.get('SENDGRID_PASSWORD'))
#             app.config.setdefault('MAIL_SERVER', 'smtp.sendgrid.net')
#             app.config.setdefault('MAIL_USERNAME', environ.get('SENDGRID_USERNAME'))
#             app.config.setdefault('MAIL_PASSWORD', environ.get('SENDGRID_PASSWORD'))
#             app.config.setdefault('MAIL_USE_TLS', True)

# class CloudantTestCase(BaseTestCase):
#     def test(self):
#         cloudant_uri = environ.get('CLOUDANT_URL')
#         if cloudant_uri:
#             app.config.setdefault('COUCHDB_SERVER', cloudant_uri)

# class MemcachierTestCase(BaseTestCase):
#     def test(self):
#         app.config.setdefault('CACHE_MEMCACHED_SERVERS', environ.get('MEMCACHIER_SERVERS'))
#         app.config.setdefault('CACHE_MEMCACHED_USERNAME', environ.get('MEMCACHIER_USERNAME'))
#         app.config.setdefault('CACHE_MEMCACHED_PASSWORD', environ.get('MEMCACHIER_PASSWORD'))



if __name__ == '__main__':
    unittest.main()