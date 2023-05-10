import openai
from langchain import PromptTemplate, FewShotPromptTemplate

objective_fn_template  = PromptTemplate(template="""
I want you to create a formalization of {preference} preference as a single objective function which has criteria related to the following opinions: {opinions}.
""", input_variables=["preference", "opinions"])


def ask_obj_fn(preference_target: str, opinions: list[str]):
	prompt = objective_fn_template.format(preference=preference_target, opinions="\n".join(opinions))
	return openai.ChatCompletion.create(
	    model="gpt-3.5-turbo",
	    messages=[
	        {"role": "system", "content": "You formalize preferences into a single, concrete objective functions and return only a single function, nothing else."},
					{"role": "user", "content": prompt},
	    ]
	)

print(ask_obj_fn("food choice", opinions=["I like to eat healthy food.", "I like to eat meat.", "I like Korean food.", "I am allergic to wheat."]))