import logging

def logging_config(level: int):
    logging.basicConfig(
        level=level,
        datefmt='%Y-%m-%d %H:%M:%S',
        format='[%(asctime)s.%(msecs)03d] %(module)s:%(lineno)d %(levelname)s - %(message)s'
    )

class UserExistsException(Exception):
    pass

class IsNotCorrectData(Exception):
    pass

class PhoneExists(Exception):
    pass

class TelegramExists(Exception):
    pass