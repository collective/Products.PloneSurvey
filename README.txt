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

Testing
Tested against Plone 3.1.2 by University of Leicester. Compared to the existing PloneSurvey 1.1.1 that we were running against Plone 2.5,
we didn't find any new problems. We have quite a lot of quite complex surveys. We cannot guarantee that any new features added since 1.1.1 are working properly. Our main goal at this point was to be able to migrate to Plone 3.x and have PloneSurvey still working.
This is labelled Alpha but University of Leicester is planning to go live with this.
