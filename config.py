import os

base_dir = os.path.dirname(os.path.abspath(__file__))

# default env file
env_file = '.env.example'

# check if user provided env file exists and update if necessary
if os.path.isfile('.env'):
    env_file = '.env'

# read configs from file
with open(env_file, 'r') as fh:
    configs = dict(
        tuple(line.replace('\n', '').replace('\"', '').split('='))
        for line in fh.readlines() if not line.startswith('#')
    )


class Config():
    DATABASE = os.path.join(base_dir, configs["DATABASE_FILE"])

    @staticmethod
    def init_app(app):
        pass


class TestingConfig(Config):
    TESTING = True


config = {
    'testing': TestingConfig,
    'default': Config
}
