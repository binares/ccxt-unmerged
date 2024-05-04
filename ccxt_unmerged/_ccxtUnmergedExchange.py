import re
import functools
import ccxt


# Use the old rest api definer, as the new one has ditched camelCase, and it'd be too troublesome
# to edit the individual exchanges here to use snake_case
class ccxtUnmergedExchange:
    @classmethod
    def define_rest_api(cls, api, method_name, paths=[]):
        delimiters = re.compile("[^a-zA-Z0-9]")
        entry = getattr(
            cls, method_name
        )  # returns a function (instead of a bound method)
        """
        {
            'public': {
                'get': {
                    'public/currency': 10,
                    'public/currency/{currency}': 10,
                    ...
                }, 
                ...
            },
            ...
        }
        """
        for key, value in api.items():
            # check if is the deepest level
            if (
                isinstance(value, dict)
                and value
                and not isinstance(list(value.values())[0], (dict, list))
            ):
                value = list(value.keys())
            if isinstance(value, list):
                uppercase_method = key.upper()
                lowercase_method = key.lower()
                camelcase_method = lowercase_method.capitalize()
                for path in value:
                    path = path.strip()
                    split_path = delimiters.split(path)
                    lowercase_path = [x.strip().lower() for x in split_path]
                    camelcase_suffix = "".join(
                        [ccxt.Exchange.capitalize(x) for x in split_path]
                    )
                    underscore_suffix = "_".join([x for x in lowercase_path if len(x)])
                    camelcase_prefix = ""
                    underscore_prefix = ""
                    if len(paths):
                        camelcase_prefix = paths[0]
                        underscore_prefix = paths[0]
                        if len(paths) > 1:
                            camelcase_prefix += "".join(
                                [ccxt.Exchange.capitalize(x) for x in paths[1:]]
                            )
                            underscore_prefix += "_" + "_".join(
                                [
                                    x.strip()
                                    for p in paths[1:]
                                    for x in delimiters.split(p)
                                ]
                            )
                            api_argument = paths
                        else:
                            api_argument = paths[0]
                    camelcase = (
                        camelcase_prefix
                        + camelcase_method
                        + ccxt.Exchange.capitalize(camelcase_suffix)
                    )
                    underscore = (
                        underscore_prefix
                        + "_"
                        + lowercase_method
                        + "_"
                        + underscore_suffix.lower()
                    )

                    def partialer():
                        outer_kwargs = {
                            "path": path,
                            "api": api_argument,
                            "method": uppercase_method,
                        }

                        @functools.wraps(entry)
                        def inner(_self, params=None):
                            """
                            Inner is called when a generated method (publicGetX) is called.
                            _self is a reference to self created by function.__get__(exchange, type(exchange))
                            https://en.wikipedia.org/wiki/Closure_(computer_programming) equivalent to functools.partial
                            """
                            inner_kwargs = dict(outer_kwargs)  # avoid mutation
                            if params is not None:
                                inner_kwargs["params"] = params
                            return entry(_self, **inner_kwargs)

                        return inner

                    to_bind = partialer()
                    setattr(cls, camelcase, to_bind)
                    setattr(cls, underscore, to_bind)
            elif isinstance(value, dict):
                cls.define_rest_api(value, method_name, paths + [key])

    def __init__(self, config={}):
        descr = self.deep_extend(self.describe(), config)
        if descr.get("api"):
            # print("defining rest api")
            self.define_rest_api(descr["api"], "request")
        super(ccxtUnmergedExchange, self).__init__(config)
