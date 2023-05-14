from langchain import Anthropic
from langchain.chains import ConversationChain
llm = Anthropic(model="claude-v1.3-100k")

conversation = ConversationChain(
    llm=llm,
    verbose=False
)
with open("/Users/yihan/LocalYihan/openAgency/open-agency/src/preData.txt", "r") as f:
    rawOutput =  str(f.read())   
pre = conversation.predict(input=f"""
{rawOutput} \n above is a mix of texts from print statement of a program, use as context for the following questions
               the program is to let voters give their opinion on funding projects
               please output the following using the context:
               1. who are the voters, what are their characters
               2. what are the criteria for the projects
               3. what are users preferences for each criteria
               4. what are the projects
               5. what are projects' scores for each criteria
               6. what are final allocation of money to each project
               7. what are the reasons for the final allocation
               8. whar are soem objections to the final allocation
               9. how do the voters respond to the objections
               10. what are the final allocation after the voters respond to the objections
""")
print(pre)


