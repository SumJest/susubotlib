import configparser


class Config:
    config: configparser.ConfigParser

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls._instance = super(Config, cls).__new__(cls)
            if args:
                cls.config = configparser.ConfigParser()
                cls.config.read(args[0])
            return cls._instance
