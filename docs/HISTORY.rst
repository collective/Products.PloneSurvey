Changelog for Products.PloneSurvey
==================================


1.4.10 (2016-10-14)
-------------------

  * Remove ${enablingObjective} from translations [gaudenzius]

  * Fix survey-notification emails containing non ascii-characters in survey title [fRiSi]

  * Use Mailhost to encode email headers in survey invitations correctly.

    ATTENTION: existing customizations of survey_send_invite_template need to be adapted
    [fRiSi]


1.4.9 - 2016-04-10
------------------

  * Update locales with i18dudue [tcurvelo]
  * Fix PlonePAS imports [davidemoro]
  * Don't create the respondent for anon on survey view [Michael Davis]
  * On a multipage survey only display captcha on last page
    [keul]
  * Fix typo in `getValidationQuestions` method that breaks SubSurvey creation
    when a Select question was created in the form
    [cekk]

1.4.8 - 2015-01-06
------------------

  * Captcha integration with collective.recaptcha, if quintagroup.plonecaptchas isn't installed [fdelia]
  * Fix captcha integration with quintagroup.plonecaptchas in validate_survery for anonymous [fdelia]

1.4.7 - 2014-05-17
------------------

  * Write a buildout and setup travis [Michael Davis]

  * German translation [Michael Bunk]

  * updated Spanish translation
    [Manuel Gualda Caballero]

  * Fix: mistake link url for @@Products.PloneSurvey.html_spreadsheet at survey_view_results.pt
    [terapyon]

  * Restored minimal Plone 3 compatibility (but beware z3c.rml version)
    [keul]

  * Fixed getAnswerFor return value for selectionBox fields. Now force to return a string like radio
    [cekk]

  * Some fixes to translations and i18ndude script [cekk]

1.4.6 - 2013-05-19
------------------

  * Fix: hide respondent names in html_spreadsheet for confidential surveys
    [Gaudenz Steinlin]
  * Fix: avoid overwriting authenticated respondent data when refreshing the
    survey_view [david.batranu]
  * Fix: fixing spreadsheet3 export for multiple select question
    [david.batranu]
  * Fix: url quoting respondent keys to fix key login [david.batranu]
  * Fix: fixing answers attribute check for matrix questions [david.batranu]
  * Fix: int iteration and Attribute Error in Survey.py [david.batranu]
  * Updated package to new i18n translation framework
    [sauzher]

1.4.5 - 2012-10-14
------------------

  * Plone 4.3 compatibility
    [alert]

  * Include Products.CMFCore permissions.zcml for Plone 4.1 compatibility
    [gaudenzius]

  * Fixed italian translation
    [keul]

1.4.4 - 2011-05-09
------------------

  * Add a MANIFEST.in file to fix the 1.4.3 release bug
    [encolpe]

1.4.3 - 2011-05-05
------------------

  * Fix z3c.rml dependency
    [encolpe]

  * Fix permission typo
    [jriboux]

  * Very basic survey printing using z3c.rml
    [Michael Davis]

  * Add browser layers, add an add survey permission, fix the results permission
    [Michael Davis]

1.4.2 - 2011-02-23
------------------

  * Patch from Gaudenz Steinlin for Sendmail issue in Plone4
    [Michael Davis]
  * Is now possible to translate also default values for some questions content type
    [keul]
  * The use of i18dude now translate a lot of new entries, not translable before
    [keul]
  * Many "plone" msgid moved to a more correct "plonesurvey" domain
    [keul]
  * Added internal "*folder_factories*" view to see Plone Survey subtypes translated
    (see also `#11520`__) [keul]

__ http://dev.plone.org/plone/ticket/11520

1.4.1 - 2010-10-11
------------------

  * New version as messed up the distribution
    [Michael Davis]

1.4.0 - 2010-10-10
------------------

  * Polish translation and i18n improvements
    [Maciej Zieba]

  * Eggification and upgrade to Plone 4 compatibility
    [Ross Patterson]

  * Improve the respondents functionality and various other improvements
    [Michael Davis]

  * Captcha integration (with quintagroup.plonecaptchas)
    [sureshvv]

  * Bugfix on SurveyDateQuestion, in barchart view
    [tiazma]

  * French translation update
    [tiazma]

1.3.0 - 2009-02-10
------------------

  * Fork for plone 3 compatibility

1.2.2 - alpha1 - 2009-02-09
---------------------------

  * French translation update
    [sneridagh]

  * Catalan translation
    [Pilar Marinas]

  * Date question
    [Michael Davis]

  * Pass survey id in form to get round cookies disabled problem
    [Michael Davis]

  * Capture respondent details with date times for start and end
    [Michael Davis]

1.2.1 - 2008-05-21
------------------

  * Bugfixes, minor functionality improvements
    [Michael Davis]

  * Updated French translation
    [Yves Moisan]

  * Spanish translation
    [Hector Velarde]

1.2.0 - 2007-10-15
------------------

  * Bug fixes, minor improvements etc during Naples Sprint
    [Michael Davis, Nick Davis, Paul Roeland]

  * ReportLab integration, two dimensional questions, answer weighting, authenticated respondents, survey dimensions
    [Hedley Roos]

  * Italian translation
    [Massimo Azzolini]

  * Dutch translation
    [Pander]

  * Brasilian Portuguese translation
    [Luis Flavio Rocha]

  * Update to German translation
    [Sven Deichmann]

  * Add Likert scale functionality to types
    [Michael Davis]

  * Sub class types from ATContentTypes
    [Michael Davis]

  * Implement generic setup
    [Michael Davis]

  * Remove backward compatibility with 1.0
    [Michael Davis]

1.1.0 - 2006-12-21
------------------
  * Fix spreadsheet bugs (see resolved issues in tracker)
    [Michael Davis, Nick Davis]

  * Remove sub survey from navigation portlet
    [Michael Davis]

  * Deprecate Survey Likert Question
    [Michael Davis]

  * Add French translation from Marc Van Coillie
    [Michael Davis]

  * Add max length for text questions
    [Michael Davis]

  * Add Polish translation and some i18n fixes
    [Piotr Furman]

  * Add save functionality
    [Michael Davis]

  * Convert answers to OOBTree
    [Michael Davis]

  * Tidy overview template, and add functionality to it
    [Michael Davis]

  * On the overview template, add links to edit function
    [Jin Tan]

  * fixed the overview information: sub survey
    [Jin Tan]

  * Add German po file from Eggert Ehmke
    [Jin Tan]

  * fixed the overview information: sub survey and branching
    [Jin Tan]

  * Add overview for user function
    [Jin Tan]

  * Add method to return questions in correct order
    [Jin Tan]

  * Remove required field from Survey Matrix and use BaseQuestion abstract
    [Jin Tan]

  * Don't validate non required fields with no value
    [Jin Tan]

  * Move getColors to survey root
    [davismr]

  * Add css file to portal_css
    [davismr]

  * Add test framework and some basic tests
    [davismr]

  * Radio buttons and Check boxes are using <label> tag to easy select of item (it is possible
    to click to the text of the answer, not only to the small area of the circle or box)
    [naro]

  * removed obsolete i18n files and created new one. Added initial Czech translation.
    [naro]

  * fixed some errors in SubSurveys caused by using getFolderContents without full_objects parameter.
    [naro]

  * fixed UnknownValidator error (validator may be empty string sometimes)
    [naro]

  * fixed some templates - not all question types has Comment field now.
    [naro]

  * Added rows and cols fields to the SurveyTextQuestion type and fixed text and textarea
    macros (question_macro). It is possible to modify number of rows of the textarea field
    and number of columns of the Text field. Number of columns of the textarea seems to be
    ignored (or overriden by the Plone CSS).
    [naro]

  * Added Survey configuration field - modifyTitle. According to this field settings,
    survey title is extended with the current survey status (open) (closed).
    Default behaviour is the same as before (extend title with the status).
    [naro]

  * Add new types for question matrix and rough macro for view
    [davismr]

  * Disable enabling objective field
    [davismr]

  * Change get FolderListingFolderContents to getFolderContents
    [davismr]

  * Add new questions to view and results
    [davismr]

  * Add switch for deprecating SurveyQuestion
    [davismr]

  * Stop new questions from appearing in nav
    [davismr]

  * Add Likert question type
    [davismr]

  * Add select question type
    [davismr]

  * Remove unuseful validators
    [davismr]

  * Add text question type
    [davismr]

  * Add branching
    [davismr]

  * Add validation
    [davismr]

  * Add question to TypesNotToList
    [davismr]

  * Enable portal factory for types
    [davismr]

  * Create base question class
    [davismr]

  * Fix bug in view results if question options have been deleted with answers for that option
    [davismr]

  * Add message in view results if no respondents
    [davismr]

  * Stop view respondents link from opening new window
    [davismr]

  * Enable allow anonymous function
    [davismr]

  * Add reset for user function
    [davismr]

1.0.0 - 2006-06-06
------------------

  * Refactor CMFQuestions to Archetypes
    [davismr]
