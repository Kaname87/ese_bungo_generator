import os

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ['SECRET_KEY']
    # Cache
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 2

class ProductionConfig(Config):
    DEBUG = False
    # Cache
    CACHE_TYPE = 'memcached'
    CACHE_DEFAULT_TIMEOUT = 180
    CACHE_MEMCACHED_SERVERS = os.environ['MEMCACHEDCLOUD_SERVERS']
    CACHE_MEMCACHED_USERNAME = os.environ['MEMCACHEDCLOUD_USERNAME']
    CACHE_MEMCACHED_PASSWORD = os.environ['MEMCACHEDCLOUD_PASSWORD']

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True