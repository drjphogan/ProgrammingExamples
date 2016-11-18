class FactoryError(Exception):
    pass

class Factory:

    _name_class_map = dict()

    @staticmethod
    def register(functor):
        Factory._name_class_map[functor.__name__] = functor

    @staticmethod
    def make(func_name):
        try:
            functor = Factory._name_class_map[func_name]
        except KeyError as e:
            error_msg = ''.join([str(e), ' does not exist in factory.'])
            raise FactoryError(error_msg)
        return functor
