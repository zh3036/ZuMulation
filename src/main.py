from langchain import OpenAI
from natural_formal_translator import struct_state_builder
from pathos.multiprocessing import ProcessingPool as Pool

from langchain import Anthropic
from langchain.chat_models import ChatAnthropic
import os
import sys

from algorithms.voting.quadratic import perform_votes
pool = Pool()

# llm = OpenAI(model_name="gpt-3.5-turbo")
ANTRHOPIC_KEY = os.environ['ANTHROPIC_API_KEY']

#TODO: UserWarning: This Anthropic LLM is deprecated. Please use `from langchain.chat_models import ChatAnthropic` instead
llm = Anthropic(anthropic_api_key=ANTRHOPIC_KEY, model="claude-instant-v1")
# llm = OpenAI(model_name="gpt-4")

def simple_voting(problem_statement: str, user_inputs: list[str], options: list[str]):
    """
    user_inputs is voter profiles; options is the options to vote on; 
    """
    if True:
        state_formalizer = struct_state_builder.LLMStateBuilder(
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
    return perform_votes(options_structs, user_structs)



if __name__ == "__main__":
    # direct std to output_vote.txt
    output_file = open("output_main2.txt", "a")
    output_file.write("\nxxxxxxx\nxxxxxxxxx\nxxxxxxxx\n\n")
    sys.stdout = output_file
    #problem="allocating money to projects being built for a community of hackers"
    problem="using quadratic funding to allocate "+"money to projects being built for a co-living community of hackers"
    user_inputs=["""Citizen 1: Mary Green
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
Attitudes towards projects: Enthusiastic about art and culture projects, community garden programs, and anything related to enhancing creativity. Appreciates the community-based actions leading to the environmental stewardship of multiple projects.""",
                   """Citizen 4: Carlos Diaz
Persona: Environmental engineer, age 37, married, interested in STEM subjects
General Opinion on Zuzalu: Extensively fascinated by the potential to contribute expertise to develop more sustainable living spaces
Attitudes towards projects: Highly keen on projects involving renewable energy infrastructure, waste management solutions, and technology-driven skill-sharing workshops. Wants to explore the world of art and culture for stress-relieving purposes.""",
                   """Citizen 5: Angela Jenkins
Persona: Single mom, age 35, raising two children alone, works from home as a marketing specialist
General Opinion on Zuzalu: A potentially secure and supportive environment for her children to grow up and learn the importance of valuable community interaction.
Attitudes towards projects: Primarily focused on the health and wellness program, the educational initatives, and the transportation & mobility promoting projects, as well as supportive and inclusive spaces like the resource library and the collaborative work zones.""",
                   """Citizen 6: Louisa Hernandez
Persona: Aspiring chef, age 25, just completed culinary education, co-living native since college
General Opinion on Zuzalu: Planning to adopt an all-practical, cutting-edge model for healthy, sustainable lifestyles
Attitudes towards projects: Extremely open to options that welcome her to innovate, actively participate, and contribute in new ways. Zones involving food production and transportation resonate, as well as the poised skill-sharing initiatives and health promotion activities at large.""",
                   """Citizen 7: Samuel Wilson
Persona: Architect, age 46, separated, devoted father and amateur cyclist
General Opinion on Zuzalu: He’s hungry to join projects driving improvement in healthier urban landscape design, as it aligns with his worldview and principles.
Attitudes towards this matter are expressed through his deep interest to contribute to solid renewable energy schemes, enhancing transportation, promoting ecosystem conservation-centric activities, and securing enough Rec and Tech facilities triggering creative development amongst dwellers in these spaces."""]

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

    v = simple_voting(problem, user_inputs, options)
    FinalVoteRes = v['qvRes']
    userVotes = v['preferenceMatrix']
    print("user votes", userVotes)
    print("final Votes", FinalVoteRes)
    output_file.close()
