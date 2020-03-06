"""
    The complete actigamma package

    ```
    import actigamma as ag

    db = ag.Decay2012Database()

    ...
    ```
"""
from .database import *
from .decorators import *
from .core import *
from .exceptions import *
from .identifier import *
from .inventory import *
from .util import *

# version in two places - here and .VERSION file
__version__ = "0.1.3"
