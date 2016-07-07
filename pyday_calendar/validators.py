from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


# As long as all of the arguments to your class’ constructor are themselves
# serializable, you can use the @deconstructible class decorator
@deconstructible
class validate_range(object):
    compare = lambda self, a, b, c: a > c or a < b
    message = ('Ensure this value is between'
               ' %(limit_min)s and %(limit_max)s (it is %(show_value)s).')
    code = 'limit_value'

    def __init__(self, limit_min, limit_max):
        self.limit_min = limit_min
        self.limit_max = limit_max

    def __call__(self, value):
        params = {'limit_min': self.limit_min,
                  'limit_max': self.limit_max, 'show_value': value}
        if value:
            if self.compare(value, self.limit_min, self.limit_max):
                raise ValidationError(self.message, code=self.code,
                                      params=params)

# You can let Django serialize your own custom class instances by giving
# the class a deconstruct() method. It takes no arguments, and should
# return a tuple of three things (path, args, kwargs):
