import inspect
from typing import Any, Dict, Iterable, List, Tuple


class FunctionSignature:
    def __init__(self, func):
        self._func_name = func.__name__
        fargs = inspect.getfullargspec(func)  # https://lightrun.com/answers/pyinvoke-invoke-attributeerror-module-inspect-has-no-attribute-getargspec-did-you-mean-getargs
        self._all_args = fargs.args
        kwargs_begin_ind = len(fargs.args) - len(fargs.defaults or [])
        self._pos_args = fargs.args[:kwargs_begin_ind]
        self._kwargs = {}
        for kw_arg_ind in range(len(fargs.args) - kwargs_begin_ind):
            key = fargs.args[kwargs_begin_ind + kw_arg_ind]
            value = fargs.defaults[kw_arg_ind]
            self._kwargs[key] = value
        self._module_name = inspect.getmodule(func).__name__

    @property
    def func_name(self) -> str:
        return self._func_name

    @property
    def args(self) -> List[str]:
        return self._pos_args

    @property
    def kwargs(self) -> Dict[str, Any]:
        return self._kwargs

    @property
    def pos_args(self) -> List[str]:
        return self._pos_args

    @property
    def all_args(self) -> List[str]:
        return self._all_args

    @property
    def module_name(self) -> str:
        return self._module_name

    def get_arguments_map(self, *args, **kwargs) -> Dict[str, Any]:
        arguments_map = {}
        for arg_ind, arg_name in enumerate(self.pos_args):
            if arg_ind < len(args):
                arguments_map[arg_name] = args[arg_ind]
            else:
                # positional argument can be specified by name (as keyword argument)
                arguments_map[arg_name] = kwargs[arg_name]
        for kwarg_name, kwarg_default_value in self.kwargs.items():
            arguments_map[kwarg_name] = kwargs.get(kwarg_name, kwarg_default_value)
        return arguments_map

    def __str__(self):
        kwargs_formatted = ['{}={}'.format(key, value) for key, value in self.kwargs.iteritems()]
        return '{}({})'.format(self.func_name, ', '.join(self.args + kwargs_formatted))


def inspect_class_attrs(cls) -> Iterable[Tuple[str, str]]:
    all_attrs = inspect.getmembers(cls, lambda member: not inspect.isroutine(member))
    isnt_builtin_attribute = lambda attribute: not (attribute[0].startswith('__') and attribute[0].endswith('__'))  # noqa
    attrs = filter(isnt_builtin_attribute, all_attrs)
    return attrs


def inspect_obj_attrs(obj) -> Iterable[str]:
    all_attrs = dir(obj)
    isnt_builtin_attribute = lambda attribute: not (attribute.startswith('__') and attribute.endswith('__'))  # noqa
    attrs = filter(isnt_builtin_attribute, all_attrs)
    return attrs
