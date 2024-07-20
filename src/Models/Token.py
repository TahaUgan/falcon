
import configparser

config = configparser.ConfigParser()
config.read("authorization.ini")

token_info = config["tokens"]

class Token():

    def get_tokens():

        toks = token_info.get('token')
        return tuple(toks)

    def check_token(tok):
        tokens = Token.get_tokens()
        
        if(tok in tokens):
            return True
        else:
            return False