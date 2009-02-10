Overview

  PloneSurvey is a simple but powerful product written to collect data from people
  - feedback on a course, survey, simple data collection etc.

Installation

  Use the Plone Portal Quickinstaller to install this product. 

Usage

  Add a Survey within a plone site, and add questions and sub-surveys within the survey.
  Only published questions will be displayed in the survey form for users.
  The survey is an ordered folder, so question order can be changed within folder contents.
  There are 6 different types of questions that can be added, 'Radio Buttons', 'Selection Box',
  'Text Field', 'Text Area', 'Multiple Selection Box' and 'Check Boxes'. These question types
  correspond to the HTML tag used to display the answer options. For the text input question
  types there are no answer options and so this field should be ignored. Each Question also
  has an optional comment field, there are two different types of Comment Field, 'Text Area'
  or 'Text Field'. 
  Users are given the option of saving and submitting their data.
  Saving means that they can come back later and their answers will be remembered. Once a
  user has submitted their answers will be verified to make sure they gave a response to every
  question. They only way to later change their answers, is if they choose 'reset' which resets all
  their answers.

  The Thank you message text and Saved message text are used when a user completes a survey,
  and the email options determine whether emails are generated for the survey owner.
  You can also set the Survey to open or closed (which changes whether users are able to submit)
  and set whether to allow anonymous users. Anonymous support is done using a cookie __cmfquestions_name
  which stores the users name. This cookie is not persistent and so when the user exits their browser
  and returns their username will not be remembered and they will be able to take the questionnaire again.

  Questions and sub-surveys can be branched, meaning they only appear if a certain answer was given to an
  earlier question. This means the respondent answers only relevant questions and bypasses irrelevant ones.
  It is a powerful feature which reduces the time respondents take to fill in a survey.

  Use the Review results Tab to check the results of the questionnaire. There are 3 different
  spreadsheets which show different degrees of detail and are in html or csv format which can be
  opened in Excel or SPSS as well as other Statistical packages that support this format. There
  is also a summary of results on this page that will show a bar chart and numbers for multiple
  choice questions (not the text based ones obviously).

  An exit url property specifies where the user will be forwarded to on completing the survey,
  this can be an internal or external url.


Known issues:
Please check the Issue Tracker for PloneSurvey on plone.org , in case issues are discovered after these notes are written.

At the time of releasing 1.1 - :

Open/closed doesn't work - survey still remains open after you've attempted to close it. Not a big deal 
as workaround is to simply make the survey private using Plone's workflow when you wish to close the survey to new responses.

Anonymous submissions can be guessed by looking at cookie. Please don't use PloneSurvey to get anonymous respondents to
submit confidential data, as someone else on the same machine could fake a cookie and view that data. (This problem only 
applies to anonymous responses, not logged in ones). 

Currently, if one results spreadsheet doesn't tell you what you want, the likelihood is one of the other two does. The
information is all there somewhere. However there are plans in future to organise the results better, and possibly merge
the spreadsheets together.

Only tested with Plone 2.0.5 and 2.1.3 - regrettably not 2.5. 2.5 support coming soon hopefully. Any help welcome. ;-)

Testing
This code has only minor differences to a slightly earlier svn version that was used successfully for a survey 
at the University of Leicester on a Plone 2.1.3/Zope2.8.5/python2.3.5/Debian Sarge platform.
This had 8 sub-surveys and 41 questions total, with extensive use of branching, and received over 600 responses.
While 1.1 is not promised to be bug-free, it is hoped that this recent use in the field makes it reasonably well proven.
