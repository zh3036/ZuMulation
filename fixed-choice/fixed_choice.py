import asyncio
import re
import openai
import openai_async


def get_completion(messages, max_tokens=100):
    return openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            max_tokens=max_tokens,
            messages=messages)['choices'][0]['message']['content']

async def get_completion_async(messages, max_tokens=100):
    resp = await openai_async.chat_complete(
            timeout=2,
            payload={
                'model': 'gpt-3.5-turbo',
                'max_tokens': max_tokens,
                'messages': messages})
    return resp['choices'][0]['message']['content']

async def generate_options(situation, samples=1):
    if samples == 1:
        n_options_text = "an option"
    else:
        n_options_text = str(samples) + " options"
    # opts = []
    # for i in range(samples):
    prompt = 'Here is a situation: """' + situation + '""".\n' + \
            'Generate ' + n_options_text + ' that a decisionmaker has available in this situation, in a numbered list.'
    text = get_completion([{'role': 'user', 'content': prompt}], max_tokens=samples*40)
    return text
    #     opts.append(text)
    # return opts



async def preference_option_score(pref, option, explain=False, samples=1):
    prompt = 'The following user has these preferences: """' + pref + '""".\n' + \
            'Here is an option available to them:\n """' + option + '""".\n' + \
            'Predict how good this option is according to their preferences, from 0-1000. '
    if explain:
        prompt += 'Give the number first, and then explain your reasoning.'
    else:
        prompt += 'Give the number only.'
    scores = []
    explans = []
    for i in range(samples):
        while True:
            text = get_completion([{'role': 'user', 'content': prompt}])
            num_text = re.search('\d+', text)
            if num_text:
                scores.append(int(num_text.group(0)))
                if explain:
                    explans.append(text[num_text.end():])
                break
            print('Could not find integer in text: ' + text)
    score = sum(scores) / len(scores)
    return (score, scores, explans)

async def preference_option_matrix(prefs, options, explain=False, samples=1):
    # coros = []
    results = []
    for pref in prefs:
        for option in options:
            # coros.append(preference_option_score(pref, option, explain, samples))
            results.append(await preference_option_score(pref, option, explain, samples))
    # note: using asyncio.gather doesn't actually improve performance!
    # results = await asyncio.gather(*coros)
    mat = []
    for i, pref in enumerate(prefs):
        mat.append(results[i*len(options) : (i+1)*len(options)])
    return mat

def option_average_scores(matrix):
    opt_scores = [0] * len(matrix[0])
    for pref_scores in matrix:
        for i, score in enumerate(pref_scores):
            opt_scores[i] += float(score[0]) / len(matrix)
    return opt_scores

def max_index(vec):
    max_val = vec[0]
    max_ind = 0
    for i, val in enumerate(vec):
        if val > max_val:
            max_val = val
            max_ind = i
    return max_ind

async def main():

    prefs = ['I like to eat healthy food.', 'I like to eat meat.']
    options = ['This restaurant serves vegetables and noodles', 'This restaurant serves hamburgers and fries', 'This restaurant serves fish and salad']
    
    matr = await preference_option_matrix(prefs, options, explain=True, samples=1)
    print(matr)
    avg_scores = option_average_scores(matr)
    print(avg_scores)
    print(max_index(avg_scores))

async def main2():
    situation = 'I am in New York at 125 st looking for a restaurant to eat at.'
    prompt = situation + ' List 6 possible restaurants that are options.'
    text = get_completion([{'role': 'user', 'content': prompt}], max_tokens=6*40)
    print(text)
    num_spans = [(m.start(), m.end()) for m in re.finditer('(\d+)\.', text)]
    options = []
    for i in range(len(num_spans)):
        text_start = num_spans[i][1]
        if i == len(num_spans) - 1:
            text_end = len(text)
        else:
            text_end = num_spans[i+1][0]
        options.append(text[text_start:text_end].strip())
    print(options)
    prefs = ['I like to eat healthy food.', 'I like to eat meat.']
    matr = await preference_option_matrix(prefs, options, explain=True, samples=1)
    print(matr)
    avg_scores = option_average_scores(matr)
    print(avg_scores)
    print(max_index(avg_scores))


asyncio.run(main2())

# print(preference_option_score('I like to eat healthy food.', 'This restaurant sells vegetables and noodles'))
# print(preference_option_score('I like to eat healthy food.', 'This restaurant sells hamburgers and fries'))
# print(preference_option_score('I like to eat healthy food.', 'This restaurant sells fish and salad'))
