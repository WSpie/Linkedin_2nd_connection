import logging

class Log:
    def __init__(self, config):
        self.logger = logging.getLogger(config.username)
        self.logger.setLevel(logging.DEBUG)
        file_handler = logging.FileHandler('summary.log')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)
    
    def record(self, name):
        self.logger.info(f'Sent request to {name}')
    
    def unable_parse_page(self, page):
        self.logger.error(f'Unable to parse the page {page}')
    
    def no_next_page(self, page):
        self.logger.error(f'Current page {page}, no next page')
