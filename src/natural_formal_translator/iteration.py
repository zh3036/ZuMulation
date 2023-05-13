from langchain.chains import ConversationChain
from langchain.llms import OpenAI
from langchain.output_parsers import CommaSeparatedListOutputParser
from langchain.memory import ConversationBufferMemory
from langchain import Anthropic
import numpy as np
from math import sqrt
import ast
from algorithms.voting.quadratic import perform_votes_from_prf
import sys
from data import user_inputs_2, options


class Iteration:
    def __init__(self, prb_st: str, voteRes: list, options: list[str], llm=None):
        self.llm = llm if llm is not None else OpenAI(temperature=0, model_name="gpt-4")
        self.prob_statement = prb_st
        self.voteRes = voteRes
        self.options = options
        vr = ["the funding allocation for this project is "+str(v) for v in voteRes]
        finalDecisionsList = list(zip(options, vr))
        self.finalDecisions = "\n".join([f"{o} {v}" for o, v in finalDecisionsList])

    def create_natural_objection(self, user_input) -> str:
        """
        Create a natural language objection to the decision
        """
        conversation = ConversationChain(
            llm=self.llm,
            memory=ConversationBufferMemory(),
            verbose=False
        )
        ret = conversation.predict(input=f"""You are acting as a voter. Here is the person's description: 
            {user_input}
            An outcome has been created regarding {self.prob_statement}, after collecting every citizen's vote. 
            The result of quadratic funding allocation is:\n {self.finalDecisions}.
            According to your persona,
            What is your biggest objection to this funding allocation results? Please write two objections.""")
        return ret

    def summarize_objections(self, objections: list[str]) -> str:
        """
        a helper function to aggrate all objections into one big objections
        """
        conversation = ConversationChain(
            llm=self.llm,
            memory=ConversationBufferMemory(),
            verbose=False
        )
        objections = "\n".join(objections)
        ret = conversation.predict(input=f"""{objections} above are objections from different voters for the problem {self.prob_statement}.
         Please summarize all the objections into an announcement for decision makers to understand the feedback of the voters.""")
        return ret        
    
    def update_user(self, citizen_persona:str, objections_summary:str, original_vote:list,options:list[str]):
        """
        Update the user's beliefs and values based on the objections 
        """
        original_vote = ",".join([str(v) for v in original_vote])
        options = "\n".join(options)
        conversation = ConversationChain(
            llm=self.llm,
            memory=ConversationBufferMemory(),
            verbose=False
        )
        ret = conversation.predict(input=f"""You are acting as a voter. Here is the person's description: 
            {citizen_persona}
            An outcome has been created regarding {self.prob_statement}, after collecting every citizen's vote. 
            The result of quadratic funding allocation is:\n {self.finalDecisions}.
            According to your persona,
            What is your biggest objection to this funding allocation results? Please write two objections.
            Different people have different objections to this decision. Here are some objections summary:
            {objections_summary}
            you original vote for {options} are {original_vote} respectively which contributes the final allocation through quadratic funding.
            we want you to respond to the objection summary, 
            give your new vote if you would like change, and give your reasons for each change/or no change
            If you want to change your vote, please write down your new vote for each option. 
            if you donot want to change your vote, please output your original vote for each option.
            notice there are {str(len(options))} options
            your output should be in format of 
            $&$ [option1 vote, option2 vote, option3 vote, ...] $&$ reasons for each change/or no change
            """)
        print(ret)
        return ret
    
    def get_formatted_votes(self,update_msg:str, num_options:int)->list[float]:
        """
        get the formatted votes from the user's response
        """
        conversation = ConversationChain(
            llm=self.llm,
            memory=ConversationBufferMemory(),
            verbose=False
        )
        # catch exceptions of SyntaxError: invalid syntax for the following code
        for i in range(10):
            try:
                ret = conversation.predict(input=f"""{update_msg}
                above is an message about a voter changing his/her vote.
                there are {str(num_options)} options in this votes.
                    Please output the formatted vote for each option in the format of
                    [option1 vote, option2 vote, option3 vote, ...] , and output nothing else
                    make sure it can be parsed into python list using ast.literal_eval
                """)
                print (ret)
                ret = ast.literal_eval(ret)
                assert len(ret) == num_options
                break # no error, break the loop
            except:
                print ("error in parsing the votes, retrying...")
        return ret




if __name__ == "__main__":
    output_file = open("output_iter.txt", "a")
    output_file.write("\nxxxxxxx\nxxxxxxxxx\nxxxxxxxx\n\n")
    sys.stdout = output_file
    llm = Anthropic(model="claude-instant-v1-100k")
    # llm = OpenAI(temperature=0, model_name="gpt-4")
    citizen_descs=user_inputs_2 # user_inputs_2 is a list of citizen's description has length 
    # voteRes = [4, 20, 3.5, 10, 5]

# simulate some vote
# vote_by_citiziens is a matrix such that every entry is one citizen's vote for each options, initialzed with random values between 0 and 10
    # vote_by_citiziens = np.random.randint(0,10,size=(len(citizen_descs),len(options)))
    vote_by_citiziens = np.array([
    [0,0, 10, 0, 5],
    [0, 7, 10, 0, 10],
    [0, 10, 0, 10, 15]
])
    # make vote_by_citizen 's each entry sum up to 10
    vote_by_citiziens = vote_by_citiziens*10 / vote_by_citiziens.sum(axis=1,keepdims=1)
    # print (vote_by_citiziens)

    voteRes = perform_votes_from_prf(vote_by_citiziens)
    print(voteRes)

    for count in range(2):
        It_test = Iteration("using quadratic funding to allocate "+"money to projects being built for a co-living community of hackers",\
                            voteRes,options,llm=llm)
        # print (It_test.finalDecisions)
        citizen_objections = [It_test.create_natural_objection(citizen_desc) for citizen_desc in citizen_descs]
        # print (citizen_objections)
        summary_objections = It_test.summarize_objections(citizen_objections)
        print (summary_objections)
        # user_updated = It_test.update_user(citizen_descs[1],summary_objections,vote_by_citiziens[1],options)
        # print (user_updated)
        # print (It_test.get_formatted_votes(user_updated,5))
        newVotes = []
        for i in range(len(citizen_descs)):
            citizen_updated = It_test.update_user(citizen_descs[i],summary_objections,vote_by_citiziens[i],options)
            newVote = It_test.get_formatted_votes(citizen_updated,len(options))
            newVotes.append(newVote)
        newVotes =np.array(newVotes)
        newVotes =newVotes*10 / newVotes.sum(axis=1,keepdims=1)
        print("vote from last round"+vote_by_citiziens)
        print ("normalized new votes:\n"+newVotes)


        voteRes_new = perform_votes_from_prf(newVotes)
        print ("final allocation of last round:\n"+voteRes)
        print ("final allocation of this round:\n"+voteRes_new)

        voteRes = voteRes_new
        vote_by_citiziens = newVotes
    output_file.close()
