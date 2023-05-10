import openai
import re


def get_completion(messages, max_tokens=100):
    return openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            max_tokens=max_tokens,
            messages=messages)['choices'][0]['message']['content']

def preference_option_score(pref, option):
    prompt = 'The following user has these preferences: "' + pref + '".\n' + \
            'Here is an option available to them:\n "' + option + '".\n' + \
            'Predict how good this option is according to their preferences, from 0-1000. Just say the number, nothing else.'
    while True:
        text = get_completion([{'role': 'user', 'content': prompt}])
        num_text = re.search('\d+', text)
        if num_text:
            return int(num_text.group(0))
        print('Could not find integer in text: ' + text)

def preference_option_matrix(prefs, options):
    return [[preference_option_score(pref, option) for option in options] for pref in prefs]

def option_average_scores(matrix):
    opt_scores = [0] * len(matrix[0])
    for pref_scores in matrix:
        for i, score in enumerate(pref_scores):
            opt_scores[i] += float(score) / len(matrix)
    return opt_scores

def max_index(vec):
    max_val = vec[0]
    max_ind = 0
    for i, val in enumerate(vec):
        if val > max_val:
            max_val = val
            max_ind = i
    return max_ind

prefs = ['I like to eat healthy food.', 'I like to eat meat.']
options = ['This restaurant serves vegetables and noodels', 'This restaurant serves hamburgers and fries', 'This restaurant serves fish and salad']

matr = preference_option_matrix(prefs, options)
print(matr)
avg_scores = option_average_scores(matr)
print(avg_scores)
print(max_index(avg_scores))

# print(preference_option_score('I like to eat healthy food.', 'This restaurant sells vegetables and noodles'))
# print(preference_option_score('I like to eat healthy food.', 'This restaurant sells hamburgers and fries'))
# print(preference_option_score('I like to eat healthy food.', 'This restaurant sells fish and salad'))
