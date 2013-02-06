import parsnip

CONFIG = {
    'REDIS_USER': lambda url: url.username or None,
    'REDIS_PASSWORD': lambda url: url.password or None,
    'REDIS_HOST': lambda url: url.hostname,
    'REDIS_PORT': lambda url: url.port,
}

parser = parsnip.Parser(config=CONFIG, schemes=['redis'])