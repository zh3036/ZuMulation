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
    citizen_descs=["""Citizen 1: Mary Green
Persona: Environmental enthusiast, age 32, single, yoga instructor
General Opinion on Zuzalu: Excited about the idea of living in an ecologically focused environment promoting a strong, healthy sense of community.
Attitudes towards projects: Highly interested in health and wellness, renewable energy, and ecosystem conservations. Appreciates access to shared resources, creative culture, and sustainable transportation methods.""",
                   """Citizen 2: Tom Sanders
Persona: Entrepreneur, age 40, married, two kids, involved in the tech industry
General Opinion on Zuzalu: Sees it as a smart way of living, intrigued by innovation and creative opportunities offered in such a space.
Attitudes towards projects: Looks forward to collaborative workspaces, skill-sharing opportunities, and sustainable solutions in energy and food production. Appreciates health and wellness initiatives to achieve a better work-life balance.""",
                   """Citizen 3: Rachel Thompson
Persona: Artist, age 29, in a relationship, mural artist
General Opinion on Zuzalu: Loves the idea of a creative and culturally thriving space with exciting opportunities for artists and creators.
Attitudes towards projects: Enthusiastic about art and culture projects, community garden programs, and anything related to enhancing creativity. Appreciates the community-based actions leading to the environmental stewardship of multiple projects."""]

    # voteRes = [4, 20, 3.5, 10, 5]
    options=["""Project 1 - Sustainable Food Production System 
Explanation: As an aspiring chef with a culinary education, I am passionate about turning locally-grown and sustainably sourced ingredients into delicious culinary creations. I believe this project could provide valuable resources and inspire community residents, including myself, in innovative and sustainable cooking practices while also reducing our carbon footprint.""",
               """Project 2 - Skill-Sharing and Educational Initiatives 
Explanation: We can never stop learning, improving and sharing our knowledge with others. Combining culinary education and experience with others' skill sets will only lead to a more vibrant and multifaceted community. I look forward to expanding my own horizons as well as having the opportunity to teach cooking classes and share my passion for food with my fellow community members.""",
               """Project 3 - Transportation and Mobility Promoting 
Explanation: Being an advocate for healthy living and sustainability, ensuring efficient and environment-friendly mobility options is important. Commuting to local farmers' markets and other food sourcing without negatively impacting the environment is both practical and appealing for me. Investing in bike-shares and community-friendly pathways will also encourage a more active lifestyle and foster community-wide connections.""",
               """Project 4 - Health and Wellness Program 
Explanation: Total well-being comprises more than just eating right; a healthy mind and body are of vital importance too. Yoga, meditation, and holistic therapies resonate deeply with my desire to live a well-rounded life. This project could attract health professionals from whom I can learn and truly cultivate a wholesome atmosphere in our community.""",
               """Project 5 - Art and Culture Enrichment 
Explanation: A healthy dose of art and culture can breathe life into any community. As an appreciator of art, I believe dedicated gallery spaces, workshops, and other creative projects will not only foster our home-grown artistic expressions but also incorporate creativity into our everyday lives, potentially blending with food production and healthy living."""]

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
    # generate a quadraftic voting result
    # voteRes = [
    #     sum(sqrt(vote_by_citiziens[i][j]) for i in range(len(citizen_descs)))
    #     for j in range(len(options))
    # ]
    # voteRes = [v**2 for v in voteRes]
    voteRes = perform_votes_from_prf(vote_by_citiziens)
    print(voteRes)

    for count in range(3):
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
        print (newVotes)
        newVotes =np.array(newVotes)
        newVotes =newVotes*10 / newVotes.sum(axis=1,keepdims=1)
        print (newVotes)
        print(vote_by_citiziens)

        # voteRes_new = [
        #     sum(sqrt(newVotes[i][j]) for i in range(len(citizen_descs)))
        #     for j in range(len(options))
        # ]
        # voteRes_new = [v**2 for v in voteRes_new]
        voteRes_new = perform_votes_from_prf(newVotes)
        print (voteRes_new)
        print (voteRes)

        voteRes = voteRes_new
        vote_by_citiziens = newVotes
    output_file.close()
