def filter_by_name(name):
    def f(message):
        return message['name'] == name
    return f


def _find_func(func_str):
    return globals()[func_str]


def get_filter_func(func_args_str):
    func_str, *args = func_args_str.split(',')
    func_obj = _find_func(func_str)
    return func_obj(*args)