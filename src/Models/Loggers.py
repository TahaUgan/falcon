
import logging

e_logger = logging.getLogger('errors')
e_logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('../logs/error.log')
fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)

e_logger.addHandler(ch)
e_logger.addHandler(fh)






s_logger = logging.getLogger('sessions')
s_logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('../logs/session.log')
fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)

s_logger.addHandler(ch)
s_logger.addHandler(fh)

