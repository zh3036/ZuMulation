from langchain import OpenAI
from natural_formal_translator import struct_state_builder

llm = OpenAI(model_name="gpt-4")
def simple_voting(problem_statement: str, user_inputs: list[str], options: list[str]):
	state_formalizer = struct_state_builder.LLMStateBuilder(problem_statement, llm=llm)
	user_schema = state_formalizer.build_user_schema(user_inputs, options)
	options_schema = state_formalizer.build_options_schema(user_inputs, options, user_schema)

	user_structs = [
		state_formalizer.build_user_struct_state(user_input, user_schema)
		for user_input in user_inputs
	]

	options_structs = [
		state_formalizer.build_option_struct_state(options, options_schema)
		for option in options
	]
	criteria = user_schema["criteria"].keys()
