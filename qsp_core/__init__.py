# -*- coding: utf-8 -*-
"""
QSP Core: High-Density Symbolic Communication Protocol for LLM Agents
© 2026 Kibong Jung. Licensed under the Apache License 2.0.
"""

from qsp_core.parser import QspFrame, QspParser
from qsp_core.injector import QspPromptInjector, FuzzyQspParser
from qsp_core.interpreter import QspInterpreter

__all__ = [
    "QspFrame",
    "QspParser",
    "QspPromptInjector",
    "FuzzyQspParser",
    "QspInterpreter",
]

__version__ = "1.0.0"
