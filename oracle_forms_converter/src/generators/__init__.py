"""
Generadores de código Angular a partir de Oracle Forms
"""
from .model_gen import ModelGenerator
from .service_gen import ServiceGenerator
from .component_gen import ComponentGenerator

__all__ = [
    'ModelGenerator',
    'ServiceGenerator',
    'ComponentGenerator',
]
