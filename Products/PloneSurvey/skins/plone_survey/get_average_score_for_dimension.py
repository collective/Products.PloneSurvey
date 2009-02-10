##parameters=dimension,include_sub_survey=False

survey = context

average = 0.0
counter = 0
for question in survey.get_all_questions_in_order_filtered(
    include_sub_survey=include_sub_survey,
    dimensions=[dimension],
    ignore_meta_types=('SurveyMatrix', 'SurveyTwoDimensional'),
    ignore_input_types=('text', 'area')):
    
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
        average = average + sum_of_weights * 100.0 / (num_respondents * max_weight)        
    
    counter += 1
    
if counter:
    return average/counter
else:
    return 0
