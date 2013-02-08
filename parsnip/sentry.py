import parsnip

CONFIG = {
    'SENTRY': lambda url: url.username or None,
    'REDIS_PASSWORD': lambda url: url.password or None,
    'REDIS_HOST': lambda url: url.hostname,
    'REDIS_PORT': lambda url: url.port,
}




class Parser(parsnip.Parser):
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

parser = Parser(config=CONFIG)