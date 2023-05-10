from abc import ABC

class StructStateBuilder(ABC):
	"""
	Abstract class for state builders
	"""
	@abstractmethod
	def build_options_schema(self, user_inputs: list, options: list):
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
	"""
	@abstractmethod
	def build_scoring_model(self, struct_user_state, user_schema, struct_option_states: list, option_schema):
		pass



class Builder:
		"""
		"""
			# TODO: types
    def __init__(self, state_builder, option_builder, algorithmic_evaluator) -> None:
				pass