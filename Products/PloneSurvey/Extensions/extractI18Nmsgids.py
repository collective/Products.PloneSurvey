# This method is used only for generating msgids for manual.pot
# Should NOT be used by users, only by developers with i18n knowledge.

def extractI18Nmsgids(self):
    from Products.PloneSurvey.content.Survey import Survey
    from Products.PloneSurvey.content.SubSurvey import SubSurvey
    from Products.PloneSurvey.content.SurveyLikertQuestion import SurveyLikertQuestion
    from Products.PloneSurvey.content.SurveyMatrix import SurveyMatrix
    from Products.PloneSurvey.content.SurveyMatrixQuestion import SurveyMatrixQuestion
    from Products.PloneSurvey.content.SurveySelectQuestion import SurveySelectQuestion
    from Products.PloneSurvey.content.SurveyTextQuestion import SurveyTextQuestion
    from Products.PloneSurvey.content.SurveyQuestion import SurveyQuestion
    
    types = [Survey, SubSurvey, SurveyLikertQuestion, SurveyMatrix, SurveyMatrixQuestion,
             SurveySelectQuestion, SurveyTextQuestion, SurveyQuestion] 

    i18ndata = {}
    for t in types:
        if hasattr(t, 'schema'):
            schema = t.schema
            for field in schema.keys():
                w = schema[field].widget
                if hasattr(w, 'i18n_domain'):
                    if w.i18n_domain == 'plonesurvey':
                        msgid = w.label_msgid
                        default = w.label
                        if msgid and msgid not in i18ndata.keys():
                            i18ndata[msgid] = default
                        if hasattr(w, 'description_msgid'):
                            msgid = w.description_msgid
                            default = w.description
                            if msgid and msgid not in i18ndata.keys():
                                i18ndata[msgid] = default
                            
    for msg, default in i18ndata.items():
        print "#."
        print "# Default: %s" % default
        print 'msgid "%s"' % msg
        print 'msgstr ""'
        print ''
        
                            
