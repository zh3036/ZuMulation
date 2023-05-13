import re
import json
from langchain.memory import ConversationBufferMemory
from langchain.output_parsers import CommaSeparatedListOutputParser
from langchain.llms import OpenAI
from langchain.chains import ConversationChain
from langchain.prompts import (
    PromptTemplate,
)
import openai
from common.templates import StructStateBuilder
import os
import sys
parent_dir_name = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent_dir_name)


class LLMStateBuilder(StructStateBuilder):
    def __init__(self, natural_problem_statement: str, llm=None) -> None:
        self.llm = llm if llm is not None else OpenAI(temperature=0)
        self.prob_statement = natural_problem_statement

    def build_options_schema(self, user_inputs: list[str], options: list[str], user_schema):
        """
        Return the exact user schema for this case
        """
        return user_schema
        pass

    def build_user_schema(self, user_inputs: str, options: list[str]):
        """
        We will extract what the users "value" in relation to making a choice about the problem statement
        """
        conversation = ConversationChain(
            llm=self.llm,
            memory=ConversationBufferMemory(),
            verbose=True
        )
        prompt = PromptTemplate(template="""
I want to find a solution to {problem}. Given a group of people and things that they said or wrote, can you tell me a list of criteria related to the described problem? Try to return a list.
A few example solutions to {problem} are {options}.

Here is the list of people and things they said:
{user_input}
        """, input_variables=["problem", "user_input", "options"])
        # user_input_joined = "\n".join(
        #     [f"Person {i}: {user_input}" for i, user_input in enumerate(user_inputs)])
        user_input_joined = user_inputs
        prompt_text = prompt.format(problem=self.prob_statement,
                                    user_input=user_input_joined, options=", ".join(options))

        conversation.predict(input=prompt_text)
        output_parser = CommaSeparatedListOutputParser()
        format_instructions = output_parser.get_format_instructions()

        py_raw = conversation.predict(
            input=f"Can you simplify the above to a list of simple criteria only. If any criteria are similar, merge them into one. Each criteria should be no more than 4 words?\n{format_instructions}")
        parsed_list = output_parser.parse(py_raw)
        return {
            "criteria": parsed_list
        }

    def build_user_struct_state(self, user_input, schema):
        """
        Returns a dictionary mapping criteria to a number between 0 and 1. 0 meaning the criteria is irrelvant to the person
        1 meaning the criteria is relevant.
        """
        criteria = schema["criteria"]
        conversation = ConversationChain(
            llm=self.llm,
            memory=ConversationBufferMemory(),
            verbose=True
        )
        crit = ", ".join(criteria)
        prompt = """Given a person and things that they said or wrote, can you assign a number between 0 and 1 for a set of criteria, 1 meaning the criteria is important to this person and 0 being the criteria is not important to the person?
The person: {}
The criteria: {}""".format(user_input, crit) +\
            """Your response should be a JSON object with keys being the criteria and values being the number, eg: `{"foo": 0.1, "bar": 0.9, "baz": 0.6}`"""
        conversation.predict(input=prompt)
        s = conversation.predict(
            input="Can you make sure that the above JSON is formatted correctly? Please print out the correctly formatted JSON").replace("\n", " ")

        s = re.findall(r'\{(.*)\}', s)[-1].replace("“", "\"").replace("”", "\"")
        print("Going with", s)
        j = json.loads("{" + s.lower() + "}")

        # TODO: format validation
        return j

    def build_option_struct_state(self, option, schema):
        criteria = schema["criteria"]
        conversation = ConversationChain(
            llm=self.llm,
            memory=ConversationBufferMemory(),
            verbose=True
        )
        crit = ", ".join(criteria)
        prompt = """Given a potential action for the problem of {} and a set of criteria related to the problem, can you assign a number between -1 and 1 for how positively this option each individual criteria? 1 meaning the criteria is very positively impacted, 0 meaning the criteria is not impacted, -1 meaning the criteria is very negatively impacted. Make sure to assign a value to each criteria, do not leave any out and write out the complete JSON.
The option: {}
The criteria: {}""".format(self.prob_statement, option, crit) +\
            """Your response should be a JSON object with keys being the criteria and values being the number, eg: `{"foo": 0.1, "bar": 0.9, "baz": 0.6}`"""

        conversation.predict(input=prompt)
        s = conversation.predict(
            input="Can you make sure that the above JSON is formatted correctly? Please print out the correctly formatted JSON").replace("\n", " ")
        print("QQ", s)
        s = "{" + re.findall(r'\{(.*)\}', s)[-1].replace("“", "\"").replace("”", "\"") + "}"
        print(s)
        j = json.loads(s.lower())
        # TODO: format validation, check between -1 and 1 etc
        print(j)
        return j


if __name__ == '__main__':
    l = LLMStateBuilder(
        "allocating money to projects being built for a community of hackers")
    user_scheme = l.build_user_schema("""Citizen 1: Mary Green
Persona: Environmental enthusiast, age 32, single, yoga instructor
General Opinion on Zuzalu: Excited about the idea of living in an ecologically focused environment promoting a strong, healthy sense of community.
Attitudes towards projects: Highly interested in health and wellness, renewable energy, and ecosystem conservations. Appreciates access to shared resources, creative culture, and sustainable transportation methods.
Citizen 2: Tom Sanders
Persona: Entrepreneur, age 40, married, two kids, involved in the tech industry
General Opinion on Zuzalu: Sees it as a smart way of living, intrigued by innovation and creative opportunities offered in such a space.
Attitudes towards projects: Looks forward to collaborative workspaces, skill-sharing opportunities, and sustainable solutions in energy and food production. Appreciates health and wellness initiatives to achieve a better work-life balance.
Citizen 3: Rachel Thompson
Persona: Artist, age 29, in a relationship, mural artist
General Opinion on Zuzalu: Loves the idea of a creative and culturally thriving space with exciting opportunities for artists and creators.
Attitudes towards projects: Enthusiastic about art and culture projects, community garden programs, and anything related to enhancing creativity. Appreciates the community-based actions leading to the environmental stewardship of multiple projects.
Citizen 4: Carlos Diaz
Persona: Environmental engineer, age 37, married, interested in STEM subjects
General Opinion on Zuzalu: Extensively fascinated by the potential to contribute expertise to develop more sustainable living spaces
Attitudes towards projects: Highly keen on projects involving renewable energy infrastructure, waste management solutions, and technology-driven skill-sharing workshops. Wants to explore the world of art and culture for stress-relieving purposes.
Citizen 5: Angela Jenkins
Persona: Single mom, age 35, raising two children alone, works from home as a marketing specialist
General Opinion on Zuzalu: A potentially secure and supportive environment for her children to grow up and learn the importance of valuable community interaction.
Attitudes towards projects: Primarily focused on the health and wellness program, the educational initatives, and the transportation & mobility promoting projects, as well as supportive and inclusive spaces like the resource library and the collaborative work zones.
Citizen 6: Louisa Hernandez
Persona: Aspiring chef, age 25, just completed culinary education, co-living native since college
General Opinion on Zuzalu: Planning to adopt an all-practical, cutting-edge model for healthy, sustainable lifestyles
Attitudes towards projects: Extremely open to options that welcome her to innovate, actively participate, and contribute in new ways. Zones involving food production and transportation resonate, as well as the poised skill-sharing initiatives and health promotion activities at large.
Citizen 7: Samuel Wilson
Persona: Architect, age 46, separated, devoted father and amateur cyclist
General Opinion on Zuzalu: He’s hungry to join projects driving improvement in healthier urban landscape design, as it aligns with his worldview and principles.
Attitudes towards this matter are expressed through his deep interest to contribute to solid renewable energy schemes, enhancing transportation, promoting ecosystem conservation-centric activities, and securing enough Rec and Tech facilities triggering creative development amongst dwellers in these spaces.""", [
        "building a sauna", "making a full time bar", "buying art to place around the community"])
    print(user_scheme)
    user = l.build_user_struct_state("""Citizen 2: Tom Sanders
Persona: Entrepreneur, age 40, married, two kids, involved in the tech industry
General Opinion on Zuzalu: Sees it as a smart way of living, intrigued by innovation and creative opportunities offered in such a space.
Attitudes towards projects: Looks forward to collaborative workspaces, skill-sharing opportunities, and sustainable solutions in energy and food production. Appreciates health and wellness initiatives to achieve a better work-life balance.
""", user_scheme)
    print(user)
    o = l.build_option_struct_state("""Project 1 - Sustainable Food Production System (allocation: $30)
Explanation: As an aspiring chef with a culinary education, I am passionate about turning locally-grown and sustainably sourced ingredients into delicious culinary creations. I believe this project could provide valuable resources and inspire community residents, including myself, in innovative and sustainable cooking practices while also reducing our carbon footprint.""", user_scheme)
    print(o)


# TODODODODO: validate the json
