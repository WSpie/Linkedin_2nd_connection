import logging

class Log:
    def __init__(self, config):
        self.logger = logging.getLogger(config.username)
        self.logger.setLevel(logging.DEBUG)
        file_handler = logging.FileHandler('logs/summary.log')
        formatter = logging.Formatter('%(name)s %(asctime)s %(levelname)s %(message)s')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)
    
    def record(self, name, cur_cnt, target_cnt):
        self.logger.info(f'[{cur_cnt}/{target_cnt}]: Sent request to {name}')
    
    def unable_parse_page(self, page):
        self.logger.error(f'Unable to parse the page {page}')
    
    def unable_connect(self, name, msg):
        self.logger.error(f'Unable to connect {name}: {msg}')

    def no_next_page(self, page):
        self.logger.error(f'Current page {page}, no next page')

    def no_free_connections(self):
        self.logger.error('No free connections left. Exit.')
    
    def msg(self, msg):
        self.logger.info(msg)
