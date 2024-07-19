from Models.Loggers import e_logger, s_logger, r_logger
from Models.GetIP import get_ip

import random
import string

def generate_code(N):

    session_code = ''.join(random.choices(string.ascii_letters + string.digits, k = N))
    return session_code



    