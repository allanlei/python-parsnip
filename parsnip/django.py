import parsnip
import os

DEFAULT_DATABASE_ENV = 'DATABASE_URL'

DATABASE_SCHEMES = {
    'postgres': 'django.db.backends.postgresql_psycopg2',
    'postgresql': 'django.db.backends.postgresql_psycopg2',
    'postgis': 'django.contrib.gis.db.backends.postgis',
    'mysql': 'django.db.backends.mysql',
    'mysql2': 'django.db.backends.mysql',
    'sqlite': 'django.db.backends.sqlite3'
}

DATABASE_CONFIG = {
    'ENGINE': lambda url: DATABASE_SCHEMES[url.scheme],
    'NAME': lambda url: url.path[1:].split('?', 2)[0],
    'USER': lambda url: url.username,
    'PASSWORD': lambda url: url.password,
    'HOST': lambda url: url.hostname,
    'PORT': lambda url: url.port,    
}


DEFAULT_CACHE_ENV = 'CACHE_URL'
DEFAULT_MEMCACHED_SERVERS = 'MEMCACHED_SERVERS'
DEFAULT_MEMCACHED_USERNAME = 'MEMCACHED_USERNAME'
DEFAULT_MEMCACHED_PASSWORD = 'MEMCACHED_PASSWORD'

CACHE_SCHEMES = {
    'db': 'django.core.cache.backends.db.DatabaseCache',
    'dummy': 'django.core.cache.backends.dummy.DummyCache',
    'file': 'django.core.cache.backends.filebased.FileBasedCache',
    'locmem': 'django.core.cache.backends.locmem.LocMemCache',
    'memcached': 'django.core.cache.backends.memcached.MemcachedCache',
    'djangopylibmc': 'django_pylibmc.memcached.PyLibMCCache',
    'pymemcached': 'django.core.cache.backends.memcached.PyLibMCCache',
}

CACHE_CONFIG = {
    'BACKEND': lambda url: CACHE_SCHEMES[url.scheme],
    'LOCATION': lambda url: {
        'file': lambda url: url.path,
        'memcached': lambda url: ['{hostname}:{port}'.format(hostname=url.hostname, port=url.port)],
        'djangopylibmc': lambda url: ['{hostname}:{port}'.format(hostname=url.hostname, port=url.port)],
        'pymemcached': lambda url: ['{hostname}:{port}'.format(hostname=url.hostname, port=url.port)],
    }.get(url.scheme, lambda url: url.netloc)(url),
    'KEY_PREFIX': lambda url: url.path[1:],
}

class DBParser(parsnip.Parser):
    def parse_from(self, env_var=DEFAULT_DATABASE_ENV, *args, **kwargs):
        return super(DBParser, self).parse_from(env_var=env_var, *args, **kwargs)

class CacheParser(parsnip.Parser):
    def parse_from(self, env_var=DEFAULT_CACHE_ENV, *args, **kwargs):
        return super(DBParser, self).parse_from(env_var=env_var, *args, **kwargs)

    def config(self, 
        servers_env=DEFAULT_MEMCACHED_SERVERS, 
        username_env=DEFAULT_MEMCACHED_USERNAME, 
        password_env=DEFAULT_MEMCACHED_PASSWORD, 
        backend='pymemcached',
        seperator=None):

        conf = super(CacheParser, self).config({
            'LOCATION': ('MEMCACHED_SERVERS', lambda val: val.split(seperator)),
            'USERNAME': 'MEMCACHED_USERNAME',
            'PASSWORD': 'MEMCACHED_PASSWORD',
        })
        conf['BACKEND'] = CACHE_SCHEMES[backend]
        return conf

db = DBParser(config=DATABASE_CONFIG, schemes=DATABASE_SCHEMES.keys())
cache = CacheParser(config=CACHE_CONFIG, schemes=CACHE_SCHEMES.keys())