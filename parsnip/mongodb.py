import parsnip

DATABASE_CONFIG = {
    'MONGODB_USER': lambda url: url.username or None,
    'MONGODB_PASSWORD': lambda url: url.password or None,
    'MONGODB_HOST': lambda url: url.hostname,
    'MONGODB_PORT': lambda url: url.port,
    'MONGODB_DB': lambda url: url.path[1:],
}

parser = parsnip.Parser(config=DATABASE_CONFIG, schemes=['mongodb', 'mongo'])