import openai
from langchain import PromptTemplate, FewShotPromptTemplate

criteria_extraction_template = PromptTemplate(template="""
Give a list of people and opinions related to {topic}, can you extract out a list of referenced criteria related to {topic}? Here are the opinions: {opinions}
""", input_variables=["topic", "opinions"])

criteria_simplification_template = PromptTemplate(template="""
Given the following list, can you extract out a Python list with the criteria? {list}
""", input_variables=["list"])


objective_fn_template  = PromptTemplate(template="""
I want you to create a single concrete formalization of {preference} preference as a single objective function related to the following opinions. Do not be overly specific and merge similar opinions into a more general criteria: {opinions}.
""", input_variables=["preference", "opinions"])

def get_opinions(topic: str, opinions: str):
	prompt = criteria_extraction_template.format(topic=topic, opinions=opinions)
	res = openai.ChatCompletion.create(
	    model="gpt-3.5-turbo",
	    messages=[
	        {"role": "system", "content": "You extract out a list of categories from different opinions"},
					{"role": "user", "content": prompt},
	    ]
	)
	prompt = criteria_simplification_template.format(list=res.choices[0].message)
	return openai.ChatCompletion.create(
	    model="gpt-3.5-turbo",
	    messages=[
					{"role": "user", "content": prompt},
	    ]
	)

def ask_obj_fn(preference_target: str, opinions: list[str]):
	prompt = objective_fn_template.format(preference=preference_target, opinions="\n".join(opinions))
	return openai.ChatCompletion.create(
	    model="gpt-3.5-turbo",
	    messages=[
	        {"role": "system", "content": "You formalize preferences into a single, concrete objective functions and return only a single function, nothing else."},
					{"role": "user", "content": prompt},
	    ]
	)

# print(ask_obj_fn("food choice", opinions=["I like to eat healthy food.", "I like to eat meat.", "I like Korean food.", "I like Chinese food.", "I like Israeli food.", "I am allergic to wheat."]))
print(get_opinions(topic="choosing whether to watch a comedy or horror movie", opinions="""
Character 1: Cleopatra (Ancient Egypt)
1. I am Cleopatra, the last active ruler of the Ptolemaic Kingdom of Egypt. I am known for my intelligence, charm, and political prowess.

2. As Cleopatra, I enjoy a wide range of entertainment. I appreciate performances that evoke strong emotions, such as tragic plays that make me cry or historical narratives that stir my intellect. I also enjoy the company of others and often organize grand banquets and gatherings where we can indulge in lively conversations and revelry. On a free night, I would host a lavish feast, surrounded by musicians, dancers, and poets, and engage in intellectual discussions and games with my guests.

Character 2: Leonardo da Vinci (Renaissance)
1. I am Leonardo da Vinci, a polymath from the Renaissance period, known for my mastery in various fields such as art, science, and engineering.

2. As Leonardo da Vinci, I find entertainment in exploring the mysteries of the natural world and expanding my knowledge. I prefer solitary pursuits that allow me to delve into my studies and create masterpieces of art and inventions. With a free night, I would spend it in my workshop, experimenting with new techniques, sketching intricate designs, or indulging in philosophical contemplation.

Character 3: Joan of Arc (Medieval France)
1. I am Joan of Arc, a French military leader and a prominent figure during the Hundred Years' War.

2. As Joan of Arc, my preference for entertainment lies in the thrill of battle and the triumph of justice. I do not seek personal amusement but find fulfillment in fighting for a noble cause. I enjoy the company of my fellow soldiers and the camaraderie that comes with shared experiences on the battlefield. On a free night, I would strategize with my comrades, discuss tactics, and prepare for the next battle.

Character 4: Confucius (Ancient China)
1. I am Confucius, a philosopher and educator from ancient China, whose teachings had a profound impact on Chinese society and culture.

2. As Confucius, I derive entertainment from intellectual pursuits and meaningful conversations. I prefer to engage with others in discussions about ethics, morality, and societal harmony. I find joy in guiding and educating my disciples and facilitating their personal growth. On a free night, I would gather with my students, engage in philosophical debates, and share wisdom and insights to foster mutual enlightenment.

Character 5: Marie Antoinette (18th-century France)
1. I am Marie Antoinette, the last queen of France before the French Revolution.

2. As Marie Antoinette, I have a penchant for lavish and extravagant entertainment. I enjoy attending grand balls, operas, and theater performances that allow me to immerse myself in opulence and elegance. I prefer to be surrounded by a retinue of courtiers and friends who appreciate the finer things in life. On a free night, I would host a sumptuous masquerade ball, filled with music, dancing, and decadent delights.

Character 6: Mahatma Gandhi (Indian Independence Movement)
1. I am Mahatma Gandhi, a political and spiritual leader who played a crucial role in India's struggle for independence.

2. As Mahatma Gandhi, I find solace in simplicity and introspection. My entertainment comes from engaging in peaceful activities like meditation, reading, and practicing self-reflection. I prefer spending time alone, seeking inner tranquility and contemplating the path towards social justice and equality. On a free night, I would retreat to a quiet place, meditate, and immerse myself in spiritual texts.
"""))