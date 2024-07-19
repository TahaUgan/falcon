
import logging

e_logger = logging.getLogger('errors')
e_logger.setLevel(logging.DEBUG)

efh = logging.FileHandler('logs/error.log')
efh.setLevel(logging.DEBUG)

ech = logging.StreamHandler()
ech.setLevel(logging.ERROR)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ech.setFormatter(formatter)
efh.setFormatter(formatter)

e_logger.addHandler(ech)
e_logger.addHandler(efh)






s_logger = logging.getLogger('sessions')
s_logger.setLevel(logging.DEBUG)

sfh = logging.FileHandler('logs/log_in_out.log')
sfh.setLevel(logging.DEBUG)

sch = logging.StreamHandler()
sch.setLevel(logging.ERROR)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
sch.setFormatter(formatter)
sfh.setFormatter(formatter)

s_logger.addHandler(sch)
s_logger.addHandler(sfh)




r_logger = logging.getLogger('requests')
r_logger.setLevel(logging.DEBUG)

rfh = logging.FileHandler('logs/requests.log')
rfh.setLevel(logging.DEBUG)

rch = logging.StreamHandler()
rch.setLevel(logging.ERROR)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
rch.setFormatter(formatter)
rfh.setFormatter(formatter)

r_logger.addHandler(rch)
r_logger.addHandler(rfh)

