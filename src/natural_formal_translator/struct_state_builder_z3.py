import os
import sys

parent_dir_name = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent_dir_name)

import numpy as np
import re
from data import user_inputs_2, options
import ast
from langchain import Anthropic
from z3.z3 import BoolRef, And, Or, Not, Int, Real, String, Solver, Implies
from langchain.chains import ConversationChain
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory

from common.templates import StructStateBuilder


def generate_constraints_prompt(problem: str, nat_lang_constraint: str, aux_variables: dict) -> str:
    aux_variables_str = "".join(
        [f"{key} : {value}\n" for key, value in aux_variables.items()])

    return f"""
        We're trying to decide on the problem of {problem}.
        To do that, we're going to use a few constraints to generate a plan.
        Please think about the issue, and my constraint: {nat_lang_constraint}, and return a Z3 python oneliner constraint.
        The constraint should be representable with the following variables:
          # A list of properties that the data we're seeking to constrain has
	  		{aux_variables_str}
        
          Examples:
		   The constraint `I want to eat Mexican food` would return `type == "Mexican"``
		   The constraint `I want to eat at a restaurant that's less than 2 miles away` would return `distance < 2`
		   The constraint `I want to eat at a restaurant that's cheap` will return `price == 1`
		  Only return one constraint at a time, in the format `variable operator value`
    """
    # TODO: examples **specific to the problem** would be helpful here


def z3_parser(self, text: str, auxiliary_variables: dict) -> BoolRef:
    """Return a Z3 constraint from a given text completion."""

    class ConstraintNodeVisitor(ast.NodeVisitor):
        def visit_BoolOp(self, node: ast.BoolOp) -> BoolRef:
            constraints = [self.visit(value) for value in node.values]

            if isinstance(node.op, ast.And):
                return And(constraints)
            elif isinstance(node.op, ast.Or):
                return Or(constraints)
            else:
                raise ValueError(f"Unsupported boolean operator: {node.op}")

        def visit_Compare(self, node: ast.Compare) -> BoolRef:
            left = auxiliary_variables[node.left.id]
            op = node.ops[0]
            right = node.comparators[0]

            if isinstance(op, ast.Eq):
                if isinstance(right, ast.Str):
                    return left == right.s
                else:
                    return left == right.n
            elif isinstance(op, ast.NotEq):
                if isinstance(right, ast.Str):
                    return left != right.s
                else:
                    return left != right.n
            elif isinstance(op, ast.Lt):
                return left < right.n
            elif isinstance(op, ast.LtE):
                return left <= right.n
            elif isinstance(op, ast.Gt):
                return left > right.n
            elif isinstance(op, ast.GtE):
                return left >= right.n
            else:
                raise ValueError(f"Unsupported comparison operator: {op}")

    tree = ast.parse(text, mode="eval")
    visitor = ConstraintNodeVisitor()
    z3_constraint = visitor.visit(tree.body)

    return z3_constraint

def build_z3_user_auxiliary_variables_prompt(problem: str, user_inputs: list, options: list) -> str:
    """Build auxiliary variables for Z3 constraint generation."""
    u = "\n".join(user_inputs)
    o = "\n".join(options)
    constr_ex = "[String('type'), Real('distance'),  Int('price')]"
    return f"""Your acting as a program which extracts out Z3 constraints from natural language. Given the problem of {problem}, user personas/ inputs, and possible solutions, please synthesize which Z3 variables should be considered for all user such that the constraints can check whether the solutions satisfy a user's priorities relative to the given solutions. Please use only `Int`, `Bool`, `String`, and `Real` variables and do not have any constraints directly related to the solutions. Also, the constraints should not be specific to a user. I.e. do not use a user's name in the constraint.
Please return a python list of Z3 variables.
For example: ```python
{constr_ex}
``` would be a valid return value

Users:
{u}

Solutions:
{o}    
"""
# TODO: variable types?

class Z3LLMStateBuilder(StructStateBuilder):
    def __init__(self, natural_problem_statement: str, llm=None):
        self.llm = llm if llm is not None else OpenAI(
            temperature=0, model_name="gpt-4")
        self.prob_statement = natural_problem_statement

    def _natural_to_z3_str(self, nat_lang_text: str, auxiliary_variables: dict) -> str:
        """
        Parse natural language text into a potentially invalid Z3 constraint string.
        """
        prompt = generate_constraints_prompt(
            self.prob_statement, nat_lang_text, auxiliary_variables)
        conv = ConversationChain(self.llm, memory=ConversationBufferMemory())
        constr = conv.predict(input=prompt)
        return constr.strip()

    def build_user_schema(self, user_inputs: list, options: list) -> dict:
        conv = ConversationChain(self.llm, memory=ConversationBufferMemory())
        conv.predict(input=build_z3_user_auxiliary_variables_prompt(self.prob_statement, user_inputs, options))
        formatted = conv.predict(input="Can you formulate the above as a python list?").replace("\n", " ")
        str_list = re.findall(r"\[(.*)\]", formatted)[0]
        print("AAAAA", str_list)
        z3_parser(str_list, {})
        pass

    def build_options_schema(self, user_inputs: list, options: list, user_schema):
        return super().build_options_schema(user_inputs, options, user_schema)


if __name__ == "__main__":
    print("QQQQQ")
    print(build_z3_user_auxiliary_variables_prompt("deciding which projects should get funded", user_inputs_2, options).replace("\\n", "\n"))
    output_file = open("output_z3_state_builder.txt", "a")
    output_file.write("\nxxxxxxx\nxxxxxxxxx\nxxxxxxxx\n\n")
    sys.stdout = output_file
    llm = Anthropic(model="claude-instant-v1-100k")
    # llm = OpenAI(temperature=0, model_name="gpt-4")
    # user_inputs_2 is a list of citizen's description has length
    citizen_descs = user_inputs_2
    # voteRes = [4, 20, 3.5, 10, 5]

    # simulate some vote
    # vote_by_citiziens is a matrix such that every entry is one citizen's vote for each options, initialzed with random values between 0 and 10
    # vote_by_citiziens = np.random.randint(0,10,size=(len(citizen_descs),len(options)))
    vote_by_citiziens = np.array([
        [0, 0, 10, 0, 5],
        [0, 7, 10, 0, 10],
        [0, 10, 0, 10, 15]
    ])
    # make vote_by_citizen 's each entry sum up to 10
    vote_by_citiziens = vote_by_citiziens*10 / \
        vote_by_citiziens.sum(axis=1, keepdims=1)
    # print (vote_by_citiziens)

    # voteRes = perform_votes_from_prf(vote_by_citiziens)
    # print(voteRes)

    # for count in range(2):
    #     It_test = Iteration("using quadratic funding to allocate "+"money to projects being built for a co-living community of hackers",\
    #                         voteRes,options,llm=llm)
    #     # print (It_test.finalDecisions)
    #     citizen_objections = [It_test.create_natural_objection(citizen_desc) for citizen_desc in citizen_descs]
    #     # print (citizen_objections)
    #     summary_objections = It_test.summarize_objections(citizen_objections)
    #     print (summary_objections)
    #     # user_updated = It_test.update_user(citizen_descs[1],summary_objections,vote_by_citiziens[1],options)
    #     # print (user_updated)
    #     # print (It_test.get_formatted_votes(user_updated,5))
    #     newVotes = []
    #     for i in range(len(citizen_descs)):
    #         citizen_updated = It_test.update_user(citizen_descs[i],summary_objections,vote_by_citiziens[i],options)
    #         newVote = It_test.get_formatted_votes(citizen_updated,len(options))
    #         newVotes.append(newVote)
    #     newVotes =np.array(newVotes)
    #     newVotes =newVotes*10 / newVotes.sum(axis=1,keepdims=1)
    #     print("vote from last round"+vote_by_citiziens)
    #     print ("normalized new votes:\n"+newVotes)

    #     voteRes_new = perform_votes_from_prf(newVotes)
    #     print ("final allocation of last round:\n"+voteRes)
    #     print ("final allocation of this round:\n"+voteRes_new)

    #     voteRes = voteRes_new
    #     vote_by_citiziens = newVotes
    output_file.close()
