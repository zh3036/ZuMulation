from abc import ABC, abstractmethod


class StructStateBuilder(ABC):
    """
    Abstract class for state builders
    """
    @abstractmethod
    def __init__(self, natural_problem_statement: str, llm):
        pass

    @abstractmethod
    def build_options_schema(self, user_inputs: list, options: list, user_schema):
        pass

    @abstractmethod
    def build_user_schema(self, user_inputs: list, options: list):
        pass

    @abstractmethod
    def build_user_struct_state(self, user_input, schema):
        pass

    @abstractmethod
    def build_option_struct_state(self, option, schema):
        pass


class OptionsBuilder(ABC):
    """
    """
    @abstractmethod
    def get_options(self, user_inputs: list, external) -> list:
        pass


class Evaluator(ABC):
    """
    """
    @abstractmethod
    def get_best_option(self, user_scoring_functions: list, struct_user_states: list, user_schema, struct_option_states: list, option_schema):
        pass


class ScoringBuilder(ABC):
    """
		Returns a function which evaluates a user's preferences for an option.
    """
    @abstractmethod
    def build_scoring_model(self, struct_user_state, struct_option_states: list):
        pass


class Builder:
    def __init__(self, state_builder: StructStateBuilder, option_builder: OptionsBuilder, scoring_builder: ScoringBuilder, algorithmic_evaluator: Evaluator) -> None:
        pass
