from langchain import OpenAI
from natural_formal_translator import struct_state_builder
from natural_formal_translator import iteration

from pathos.multiprocessing import ProcessingPool as Pool

from langchain import Anthropic
from langchain.chat_models import ChatAnthropic
import os
import sys

from algorithms.voting.quadratic import perform_votes, perform_votes_from_prf
from data import options, user_inputs
import numpy as np

pool = Pool()

# llm = OpenAI(model_name="gpt-3.5-turbo")


#TODO: UserWarning: This Anthropic LLM is deprecated. Please use `from langchain.chat_models import ChatAnthropic` instead
llm = Anthropic(model="claude-instant-v1-100k")
# llm = OpenAI(model_name="gpt-4")

def simple_voting(problem_statement: str, user_inputs: list[str], options: list[str]):
    """
    user_inputs is voter profiles; options is the options to vote on; 
    """
    if True:
        state_formalizer = struct_state_builder.SimpleLLMStateBuilder(
            problem_statement, llm=llm)
        user_schema = state_formalizer.build_user_schema(user_inputs, options)
        options_schema = state_formalizer.build_options_schema(
            user_inputs, options, user_schema)
        print("User schema: ", user_schema)

        def build_user(user_input):
            return state_formalizer.build_user_struct_state(user_input, user_schema)

        def build_option(option):
            return state_formalizer.build_option_struct_state(option, options_schema)

        # user_structs = list(pool.map(build_user, user_inputs))
        user_structs = [build_user(user) for user in user_inputs]

        # options_structs = list(pool.map(build_option, options))
        options_structs = [build_option(option) for option in options]
        print("Got all user structs:", user_structs)
        print("Got all options structs:", options_structs)
    
    # user_structs =  [{'health': 0.9, 'transport': 0.8, 'energy': 0.9, 'skill': 0.3, 'art': 0.5, 'food': 0.7}, {'food': 0.8, 'health': 0.9, 'transport': 0.5, 'skill': 0.7, 'art': 0.3, 'energy': 0.9}, {'food': 0.3, 'health': 0.4, 'transport': 0.2, 'skill': 0.8, 'art': 0.9, 'energy': 0.5}, {'food': 0.5, 'health': 0.7, 'transport': 0.8, 'skill': 0.9, 'art': 0.6, 'energy': 1}, {'food': 0.3, 'health': 0.8, 'transport': 0.7, 'skill': 0.5, 'art': 0.2, 'energy': 0.4}, {'food': 1.0, 'health': 1.0, 'transport': 0.7, 'skill': 0.8, 'art': 0.5, 'energy': 0.5}, {'food': 0.3, 'health': 0.8, 'transport': 0.7, 'skill': 0.5, 'art': 0.4, 'energy': 0.9}]
    # options_structs = [{'food': 1, 'health': 1, 'transport': 0, 'skill': 1, 'art': 1, 'energy': 1}, {'food': 1.0, 'health': 0.0, 'transport': 0.0, 'skill': 1.0, 'art': 1.0, 'energy': 0.0}, {'food': 0.9, 'health': 1, 'transport': 1, 'skill': 0, 'art': 0, 'energy': 0.8}, {'food': 0, 'health': 1, 'transport': 0, 'skill': 0, 'art': 0, 'energy': 1}, {'food': 0, 'health': 0, 'transport': 0, 'skill': 0, 'art': 1, 'energy': 0}]
    # criteria = list(user_schema["criteria"].keys())
    return perform_votes(options_structs, user_structs), user_structs, options_structs



if __name__ == "__main__":
    # direct std to output_vote.txt
    output_file = open("output_main_withIter.txt", "a")
    output_file.write("\nxxxxxxx\nxxxxxxxxx\nxxxxxxxx\n\n")
    sys.stdout = output_file
    #problem="allocating money to projects being built for a community of hackers"
    problem="using quadratic funding to allocate "+"money to projects being built for a co-living community of hackers"
  
    v, user_structs, options_struct = simple_voting(problem, user_inputs, options)
    voteRes = v['qvRes']
    jsonRes = {}
    jsonRes["users"] = []
    for i, u in enumerate(user_structs):
        jsonRes["users"].append({
            "description": user_inputs[i],
            "scoring": u
        })

    jsonRes["options"] = []
    for i, o in enumerate(options_struct):
        jsonRes["options"].append({
            "description": options[i],
            "scoring": o
        })
    print("jsonRes", jsonRes)
    out_json_file = open("out_preferences.json", "a")
    out_json_file.write(str(jsonRes).replace("\\n", "\n"))
    out_json_file.close()


    vote_by_citiziens = v['preferenceMatrix']
    print("user votes", vote_by_citiziens)
    print("final Votes", voteRes)

    for count in range(2):
        It_test = iteration.Iteration("using quadratic funding to allocate "+"money to projects being built for a co-living community of hackers",\
                            voteRes,options,llm=llm)
        # print (It_test.finalDecisions)
        citizen_objections = [It_test.create_natural_objection(citizen_desc) for citizen_desc in vote_by_citiziens]
        # print (citizen_objections)
        summary_objections = It_test.summarize_objections(citizen_objections)
        print (summary_objections)

        newVotes = []
        for i in range(len(user_inputs)):
            citizen_updated = It_test.update_user(user_inputs[i],summary_objections,vote_by_citiziens[i],options)
            newVote = It_test.get_formatted_votes(citizen_updated,len(options))
            newVotes.append(newVote)
        newVotes = np.array(newVotes)
        newVotes = newVotes*10 / newVotes.sum(axis=1,keepdims=1)
        print("vote from last round:")
        print(vote_by_citiziens)
        print ("normalized new votes:\n", newVotes)


        voteRes_new = perform_votes_from_prf(newVotes)
        print ("final allocation of last round:\n", voteRes)
        print ("final allocation of this round:\n", voteRes_new)

        voteRes = voteRes_new
        vote_by_citiziens = newVotes


    output_file.close()
