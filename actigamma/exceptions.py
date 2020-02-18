class ActiGammaException(Exception):
    pass

class UnphysicalValueException(ActiGammaException):
    pass

class UnknownOrUnstableNuclideException(ActiGammaException):
    pass

class NoDataException(ActiGammaException):
    pass