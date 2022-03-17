from pipeline_step.pipeline_step import PipelineStep
from typing import Tuple
# We can parse in the String and return in the class
from importlib import import_module


def loaded(func):
    @wraps(func)
    def loading(*args, **kwargs):
        print(f'{func.__name__} was called')
        print(f'args: {args}')
        print(f'kwargs: {kwargs}')
        module_name, yaml_params = args
        # we can change the source folder to load the py scripts by reference the kwargs first
        # and if not available the we can default to pipeline_custom.
        # if kwargs.contains("custom_source"):
        # prefix = kwargs["custom_source"]
        # else prefix = "pipeline_custom"
        prefix = 'pipeline_custom'
        full_mod_name = f'{prefix}.{module_name}'
        cls_name = capwords(module_name, sep='_').replace('_', '')
        return func(full_mod_name, cls_name, yaml_params)
    return loading


class PipelineStepLoader:
    @staticmethod
    @loaded
    def get_class(*args) -> Tuple[PipelineStep, type()]:
        full_mod_name, cls_name, params = args
        # the module contains all bunch of stuff, but we only care of the class name that we will execute it.
        # file name of the object
        mod_obj = import_module(full_mod_name)
        return getattr(mod_obj, cls_name)(), params
