from langchain.chains import ConversationChain
from langchain.llms import OpenAI
from langchain.output_parsers import CommaSeparatedListOutputParser
from langchain.memory import ConversationBufferMemory

class Iteration:
    def __init__(self, natural_problem_statement: str, decision: str, option: str, llm=None):
        self.llm = llm if llm is not None else OpenAI(temperature=0, model_name="GPT-4")
        self.prob_statement = natural_problem_statement
        self.decision = decision

    def create_natural_objection(self, user_input) -> str:
        """
        Create a natural language objection to the decision
        """
        conversation = ConversationChain(
            llm=self.llm,
            memory=ConversationBufferMemory(),
            verbose=False
        )
        ret = conversation.predict(input=f"""You are acting as a person. Here is the person: 
{user_input}
A decision has been made regarding {self.prob_statement}. The decision is to {self.decision}.
What is your biggest objection to this decision? Please write three objections.""")
        return ret

    def summarize_objections(self, objections: list[str]) -> str:
        return 
    def update_user(self, user_input, objections):
        """
        Update the user's beliefs and values based on the objections 
        """
        conversation = ConversationChain(
            llm=self.llm,
            memory=ConversationBufferMemory(),
            verbose=False
        )
        ret = conversation.predict(input=f"""You are acting as a person. Here is the person:
{user_input}
A decision has been made regarding {self.prob_statement}. The decision is to {self.decision}.
Different people have different objections to this decision. Here are some objections:
{objections}
Consider these objections and update your set of beliefs and values. What is your new set of beliefs and values? Please write a sentence or two.""")
        return ret
