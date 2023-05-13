# open-agency
prototypes on open-agency architecture



## application on funding allocation: QF copilot

### high level description of process
Use LLM to help communities conduct Quadratic Funding more effectively.
1. Each member creates a voter profile: expressing their general thoughts on the desired projects to be built, expectations for the community, and evaluations of previous projects using natural language.
2. LLM generates a set of criteria based on the ideas of all members, and for each criteria LLM tries to score each project on behalf of every member of the community.
3. LLM tries to conduct quadratic voting on behalf of each member for a group of projects based on these criteria scores (with a budget of 100 USD).
4. A funding allocation is generated from the quadratic voting process.
5. LLM simulates being each member, provides feedback on the funding allocation, and decides whether to modify their vote.
6. Recalculate the funding allocation based on the modified votes.
7. Repeat steps 5 and 6 until the funding allocation doesn't change significantly, at which point we consider it to have reached a dynamic equilibrium(or a fix point). This LLM-generated funding allocation can serve as a reference for the actual allocation.
8. If new projects come up later, the APP can predict whether the community members are likely to be willing to fund them. Each member can inspect the vote/criteria score generated by LLM on their behalf and provide feedback to update their voter profile.


### techinical description for each step
1. for step one , we can let users directly enter their preferences or using a interactive chat interface
2. for step two, there seem no better way than LLM doing everything, the scoring should be inspectable by human member and make changes give explanations(the explanation can be added to voter profile)
3. for step three, there can be a determinist algorithm from criterian scoring to voting, but can also be done by LLM, the first stage, we do this using LLM,  this process should also be inspectable. We can also train a neural network from criteria scoring to voting.
4. using classic quadratic funding algorithm
5. Using LLM all along: everyone(or every cluster if we want to do some clustering), read the final allocation, give some opinion to everyone else . everyone reads everyone else opinion, reference the final allocation and then decide whether they change their criteria score, vote(with some explanations). This part can be inspectable as well. We could create some vector representation for how everyone want others to change their votes or criteria scoring. 
6. using classic quadratic funding algorithm
7. we need an algorithm to decide when to stop or just give a iteration limit


## comment by deger
using nash bargaining rather than quadratic funding



## 0513 notes

the current process is

1. LLM get criteria from human
2. LLM got human weight of each criteria 
3. LLM rate projects for each criteria 
4. LLM generate vote for human and aggregate 


# 0513 TODO
0. show vote of everyone DONE
1. make vote result pair with projects  
2. seek objections
3. summarize objections
4. ask whether people change their votes(weights on criteria)
5. compute new votes