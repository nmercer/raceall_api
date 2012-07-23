import ConfigParser

class Config():
    def __init__(self):
        config = ConfigParser.ConfigParser()
        config.read('/home/nmercer/git/raceall_backend/config/config.ini')

        
        self.parser = {}
	for name in config.sections():
            items = {}
            for item, value in config.items(name):
                items[item] = value

            self.parser[name] = items
