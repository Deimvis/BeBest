import wrapt
import logging

from .inspect import FunctionSignature, inspect_obj_attrs


def logging_on_call(msg, level, logger=None, **format_variables_init):
    @wrapt.decorator  # preserve information about arguments of decorated function
    def decorator(func, instance, args, kwargs):
        attributes = {}
        if instance is not None:
            for attr in inspect_obj_attrs(instance):
                attributes[attr] = getattr(instance, attr)

        func_sig = FunctionSignature(func)
        all_args = args
        if instance is not None:
            all_args = (instance,) + args
        arguments_map = func_sig.get_arguments_map(*all_args, **kwargs)

        format_variables = {}
        for format_variable_name, format_variable_init in format_variables_init.items():
            format_variables[format_variable_name] = format_variable_init(**arguments_map)

        nonlocal logger
        logger = logger or logging
        logger.log(level, msg.format(**(attributes | arguments_map | format_variables)))
        return func(*args, **kwargs)
    return decorator


def logging_on_return(msg, level, **format_variables_init):
    @wrapt.decorator  # preserve information about arguments of decorated function
    def decorator(func, instance, args, kwargs):
        func_sig = FunctionSignature(func)
        arguments_map = func_sig.get_arguments_map(*args, **kwargs)
        format_variables = {}
        for format_variable_name, format_variable_init in format_variables_init.items():
            format_variables[format_variable_name] = format_variable_init(**arguments_map)
        result = func(*args, **kwargs)
        logging.log(level, msg.format(**(arguments_map | format_variables)))
        return result
    return decorator
