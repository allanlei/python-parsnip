#!/usr/bin/env python
import urlparse
import os

class Parser(object):
    def __init__(self, config={}, schemes=[], allow_fragments=False):
        self.allow_fragments = allow_fragments
        self._config = config
        self._netloc = schemes
        for scheme in self._netloc:
            urlparse.uses_netloc.append(scheme)

    def parse(self, url, config=None):
        """
        Parses a URI into components
        """
        if not self.allow_fragments:
            url, fragment = urlparse.urldefrag(url)
        url = urlparse.urlparse(url)
        config = config or self._config
        return dict([(key, fn(url)) for key, fn in config.items()])

    def parse_from(self, env_var, default=None, *args, **kwargs):
        """
        Parses the string return from environ lookup
        """
        url = os.environ.get(env_var, default)
        config = {}
        if url:
            config = self.parse(url, *args, **kwargs)
        return config

    def config(self, in_config):
        """
        Config mapping
        """
        conf = {}

        for key, actions in in_config.items():
            if isinstance(actions, str):
                env_key = actions
                conf[key] = os.environ.get(env_key, None)
            elif isinstance(actions, tuple):
                env_key, fn = actions
                conf[key] = fn(os.environ.get(env_key, None))
        return conf

parser = Parser()
from . import django
from . import mongodb
from . import redis
from . import sentry