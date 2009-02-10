##parameters=include_sub_survey=False,dimensions=[],ignore_meta_types=[],ignore_input_types=[],restrict_meta_types=[]

questions = context.getAllQuestionsInOrder(include_sub_survey=include_sub_survey)

result = []
for question in questions:
    ok = True
    
    # At least one dimension in question.getDimensions() must be in dimensions
    if dimensions:     
        not_found = True
        for dim in question.getDimensions():
            if dim in dimensions:
                not_found = False
                break
        if not_found:
            ok = False
            
    if ignore_meta_types:
        if question.meta_type in ignore_meta_types:
            ok = ok and False
            
    if ignore_input_types:
        if question.getInputType() in ignore_input_types:
            ok = ok and False
   
    if restrict_meta_types:
        if question.meta_type not in restrict_meta_types:
            ok = ok and False

    if ok:
        result.append(question)

return result        
