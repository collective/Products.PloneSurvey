from AccessControl import ClassSecurityInfo
#from zope.interface import implements

from Products.Archetypes.atapi import *
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.content.base import registerATCT
from Products.validation import validation
from Products.CMFCore.permissions import View, ModifyPortalContent

from Products.PloneSurvey import permissions
from Products.PloneSurvey.config import TEXT_INPUT_TYPE, TEXT_VALIDATORS
from Products.PloneSurvey.config import PROJECTNAME
from Products.PloneSurvey.content.BaseQuestion import BaseQuestion

from schemata import BaseQuestionSchema

# log
from zLOG import LOG, INFO
#from Products.PloneSurvey.interfaces import ISurveyGridQuestion

#grid support

from Products.DataGridField import \
    DataGridField, DataGridWidget, Column

MainSchema = BaseQuestionSchema.copy()
del MainSchema['commentType']
del MainSchema['commentLabel']

schema = MainSchema + Schema((

    StringField('inputType',
        searchable=0,
        required=0,
        vocabulary=TEXT_INPUT_TYPE,
        default='text',
        widget=SelectionWidget(
            label="Input Type",
            label_msgid="label_input_type",
            description="Please select what type of input you would like to use for this question.",
            description_msgid="help_input_type",
            i18n_domain="plonesurvey",
           ),
        ),

    IntegerField('maxLength',
        searchable=0,
        required=0,
        default=4000,
        widget=StringWidget(
            label="Maximum length of characters",
            label_msgid="XXX",
            description="Enter the maximum number of characters a user can enter for this question",
            description_msgid="XXX",
            i18n_domain="plonesurvey",
             ),
        ),

    IntegerField('cols',
        searchable=0,
        required=0,
        default=20,
        widget=StringWidget(
            label="Cols (width in characters)",
            label_msgid="label_text_cols",
            description="Enter a number of columns for this field (width of the field in the characters)",
            description_msgid="help_text_cols",
            i18n_domain="plonesurvey",
             ),
        ),

    IntegerField('rows',
        searchable=0,
        required=0,
        default=6,
        widget=StringWidget(
            label="Rows (number of lines)",
            label_msgid="label_text_rows",
            description="Enter a number of rows for this field. This value is applicable only in the Text Area input type",
            description_msgid="help_text_rows",
            i18n_domain="plonesurvey",
           ),
        ),

    StringField('validation',
        searchable=0,
        required=0,
        vocabulary='getValidators',
        widget=SelectionWidget(
            label="Validation",
            label_msgid="label_validation",
            description="Select a validation for this question",
            description_msgid="help_validation",
            i18n_domain="plonesurvey",
          ),
        ),


        DataGridField('columnDefs',
            searchable = False,
            required = True,
            columns=('columnId','columnTitle','columnDefault'),
            default = [ {'columnId':'column1', 'columnTitle':'Column One', 'columnDefault':''}, ],
            widget = DataGridWidget(
                label = 'Column Definitions',
                i18n_domain = "pfgdatagrid",
                label_msgid = "label_column_defs_text",
		auto_insert = False,
                description = """
                    Specify a unique identifier and a title for each column
                    you wish to appear in the datagrid. The default value
                    is optional.
                """,
                description_msgid = "help_column_defs_text",
                columns={
                    'columnId':Column('Column Id'),
                    'columnTitle':Column('Column Title'),
                    'columnDefault':Column('Default Value'),
                },
            ),
        ),

        BooleanField('allowDelete',
            searchable = False,
            default = '1',
            widget = BooleanWidget(
                label = 'Allow Row Deletion',
                i18n_domain = "pfgdatagrid",
                label_msgid = "label_allow_delete_text",
            ),
        ),
        BooleanField('allowInsert',
            searchable = False,
            default = '1',
            widget = BooleanWidget(
                label = 'Allow Row Insertion',
                i18n_domain = "pfgdatagrid",
                label_msgid = "label_allow_insert_text",
            ),
        ),
        BooleanField('allowReorder',
            searchable = False,
            default = '1',
            widget = BooleanWidget(
                label = 'Allow Row Reordering',
                i18n_domain = "pfgdatagrid",
                label_msgid = "label_allow_reorder_text",
            ),
        ),



    ))

finalizeATCTSchema(schema, moveDiscussion=False)
del schema["relatedItems"]

class SurveyGridQuestion(BaseQuestion):
    """A textual question within a survey, with a grid interface"""
    schema = schema
    _at_rename_after_creation = True

    #implements(ISurveyGridQuestion)

    security = ClassSecurityInfo()

    security.declareProtected(permissions.View, 'addAnswer')
    def addAnswer(self, value, comments=""):
	""" accessor modificato per togliere linee inutili """

        value1 = []
	for i in value:
         if i['orderindex_'] <> 'template_row_marker':
          value1.append(i)

	return BaseQuestion.addAnswer(self, value1, comments)

    security.declareProtected(permissions.View, 'getValueGrid')
    def getValueGrid(self):
        """ get the accessor """
        value = self.getAnswerFor(self.getSurveyId())
	if value == None or value == []:
	 return self.returnemptyrow()
	else:
	 return value

    security.declareProtected(permissions.View, 'getValidators')
    def getValidators(self):
        """Return a list of validators"""
        validator_list = ['None', ]
        validator_list.extend(TEXT_VALIDATORS)
        return validator_list

    security.declareProtected(permissions.View, 'getValidators')
    def validateQuestion(self, value):
        """Return a list of validators"""
        validator = self.getValidation()
        v = validation.validatorFor(validator)
        return v(value)

    security.declareProtected(ModifyPortalContent, 'setColumnDefs')
    def setColumnDefs(self, value, **kwa):
        """ mutator for columnDefs """

        myval = [col for col in value if col.get('columnId')]
        self.columnDefs = myval
        try:
	 #we are still at object creation
	 self.fgField.columns = [col['columnId'] for col in myval]

         res = {}
         for col in myval:
             res[ col['columnId'] ] = Column( col['columnTitle'], default=col['columnDefault'] )
         self.fgField.widget.columns = res
	 self.fgField.widget.label = ''
	 self.fgField._p_changed = 1
	except:
	 pass

    security.declareProtected(View, 'getAllColumns')
    def getAllColumns(self):
        """list all the column in the widget"""

	res = []
	thefield = self.columnDefs
	for l in thefield:
	 res.append(l['columnId'])

	return res

    security.declareProtected(View, 'getAllColumnsTitle')
    def getAllColumnsTitle(self):
        """list all the columns and title in the widget"""

        res = []
        thefield = self.columnDefs
        for l in thefield:
         res.append((l['columnId'],l['columnTitle']))

        return res

    security.declareProtected(View, 'returnemptyrow')
    def returnemptyrow(self):
        """return an empty row"""

        res = {}
        for col in self.columnDefs:
            if col.get('columnId'):
                res[col['columnId']] = col['columnDefault']
	res['orderindex_'] = ''
        return [res]

    security.declareProtected(permissions.ModifyPortalContent, 'resetForUser')
    def resetForUser(self, userid):
        """Remove answer for a single user - leave one empty for editing"""

        if self.answers.has_key(userid):
            self.addAnswer(self.returnemptyrow())
#            LOG('PloneSurvey', INFO, self.answers[userid] )
	else:
	    # non dovrebbe mai accadere
	    pass



    security.declareProtected(ModifyPortalContent, 'disableautoinsert')
    def disableautoinsert(self):
	""" disable auto insert """
	self.fgField.widget.auto_insert = False
        self.fgField._p_changed = 1

    security.declareProtected(ModifyPortalContent, 'enableautoinsert')
    def enableautoinsert(self):
        """ enable auto insert """
        self.fgField.widget.auto_insert = True
        self.fgField._p_changed = 1

    security.declareProtected(ModifyPortalContent, 'setAllowDelete')
    def setAllowDelete(self, value, **kwa):
        """ set allow_delete flag for field """

        # Note: booleans come in the request as '0' or '1';
        # we need to translate them into True or False.
        try:
	 self.fgField.allow_delete = True
        except:
	 pass

    security.declareProtected(View, 'getAllowDelete')
    def getAllowDelete(self, **kw):
        """ get allow_delete flag for field """

        try:
	 return self.fgField.allow_delete
	except:
	 return True

    security.declareProtected(ModifyPortalContent, 'setAllowInsert')
    def setAllowInsert(self, value, **kwa):
        """ set allow_insert flag for field """

        try:
	 self.fgField.allow_insert = True
	except:
	 return True

    security.declareProtected(View, 'getAllowInsert')
    def getAllowInsert(self, **kw):
        """ get allow_insert flag for field """

        try:
	 return self.fgField.allow_insert
	except:
	 return True

    security.declareProtected(ModifyPortalContent, 'setAllowReorder')
    def setAllowReorder(self, value, **kwa):
        """ set allow_reorder flag for field """

        try:
	 self.fgField.allow_reorder = True
	except:
	 return True

    security.declareProtected(View, 'getAllowReorder')
    def getAllowReorder(self, **kw):
        """ get allow_reorder flag for field """

        try:
	 return self.fgField.allow_reorder
	except:
	 return True

#    security.declarePrivate('manage_afterAdd')
#    def manage_afterAdd(self, item, container):
#        """add the gridfield subfield with the same id of the question """
#
#        self.fgField = DataGridField(self.id,
#            searchable=False,
#            required=False,
#            write_permission = View,
#            widget = DataGridWidget(),
#            columns=('column1','column2','The third'),
#            allow_delete = True,
#            allow_insert = True,
#            allow_reorder = True,
#            )
#        self.fgField.edit_accessor = 'getValueGrid'

    def manage_afterAdd(self, item, container):
        # TODO: when we're done with 2.1.x, implement this via event subscription

        ATCTContent.manage_afterAdd(self, item, container)

        id = self.id
        try:
         if self.fgField.__name__ != id:
             self.fgField.__name__ = id
        except:
        # non siamo ancora arrivati al punto giusto, siamo ancora in portal factory
         pass

    security.declareProtected(View, 'validateAnswer')
    def validateAnswer(self, form, state):
        """Validate the question"""

        columns = self.getAllColumns()
        value = form.get(self.getId())
        valore = ''
        for row in value:
          for col in columns:
    #       try:
            valore = valore + str(row[col]).strip()
    #       except:
    #        pass
        if valore == '':
           error_msg = self.translate(
                default='Please provide an answer for the question',
                msgid='please_provide_answer_for',
                domain='plonesurvey')
           state.setError(self.getId(), error_msg )


    security.declarePrivate('at_post_create_script')
    def at_post_create_script(self):
        """add the gridfield subfield with the same id of the question """


        self.fgField = DataGridField(self.id,
            searchable=False,
            required=False,
	    allow_oddeven=True,
            write_permission = View,
            widget = DataGridWidget(
             auto_insert = False,
             label=" ",
             helper_css = "datagridwidget.css",
             helper_js = "datagridwidget.js",
             ),
            columns=('column1','column2','The third'),
            allow_delete = True,
            allow_insert = True,
            allow_reorder = True,
            )
        self.fgField.edit_accessor = 'getValueGrid'
	self.fgField.widget.label = ''
	value = self.columnDefs
        myval = [col for col in value if col.get('columnId')]
        self.columnDefs = myval
        try:
         #we are still at object creation
         self.fgField.columns = [col['columnId'] for col in myval]

         res = {}
         for col in myval:
             res[ col['columnId'] ] = Column( col['columnTitle'], default=col['columnDefault'] )
         self.fgField.widget.columns = res
	 # Add an empty answer to have a non empty widget (maybe can be avoided, to check the DataGridWidget documentation)
         self.addAnswer(self.returnemptyrow());
         self.fgField._p_changed = 1
        except:
         pass

registerATCT(SurveyGridQuestion, PROJECTNAME)
