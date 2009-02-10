##parameters=
"""
Return (currently) weighted average score for question.
The result is a dictionary so more stats can be added.
"""

question = context

res = {}

# Dict for quick answerOption lookups
answeroption_dict = {}
for ob in question.getAnswerOptionsAsObjects():
    answeroption_dict[ob()] = ob

aggr = question.getAggregateAnswers() # eg. {'Yes': 1, 'No': 2}

# Apply weighting and sum
sum_of_weights = 0.0
for answeroption, number_of_respondents_who_chose_this in aggr.items():
    sum_of_weights += number_of_respondents_who_chose_this * answeroption_dict[answeroption].getWeight()    

num_respondents = question.getNumberOfRespondents()
max_weight = question.getMaxWeight()
if num_respondents and max_weight:
    res['weighted_average_percentage'] = sum_of_weights * 100.0 / (num_respondents * max_weight)
else:
    res['weighted_average_percentage'] = 0.0

return res
