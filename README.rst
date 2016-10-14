.. contents::

.. image:: https://travis-ci.org/collective/Products.PloneSurvey.png?branch=master
    :target: http://travis-ci.org/collective/Products.PloneSurvey

.. image:: https://coveralls.io/repos/collective/Products.PloneSurvey/badge.png?branch=master
    :target: https://coveralls.io/r/collective/Products.PloneSurvey

Products.PloneSurvey - A survey tool for Plone
==============================================

This package allows users to create a survey or simple form for collecting user's feedback: on a course, simple data collection etc..
Surveys can be a simple single page, or a multi page survey with complex branching.

.. ATTENTION::

   The 1.x Series is only compatible with Plone4.3. Use 2.X (or github master branch) for Plone5.

Installation
------------

To install the package, list it in the ``eggs`` line in buildout.cfg, e.g.::

    [instance]
    ...
    eggs =
        ...
        Products.PloneSurvey

Once you have the package installed, you need to use the activate it in the Site-Setups ``Add-ons`` sections to install it into your Plone site.

Usage
-----

Once a survey has been added, you can add questions within the survey. For a multi page survey, add a `sub survey` and add your questions within the `sub survey`. To make a survey available to users, publish the survey and the questions within it. If you want the survey to be available to anonymous users, you must select `Allow Anonymous` on the survey edit form.

There are several question types: Text Question, Select Question, Date Question and Matrix Question. Matrix Questions are for tabular question banks, where the matrix questions share the same answer options.

The sub surveys allow fairly simple branching based on either an option in a previous question being selected or not selected. The option to branch on more than one answer option or more than one question is not supported yet. The branching functionality should support most use cases if your survey is well designed, but it is possible to create portions of your survey that can not be completed by branching on a question that has not been presented to the user before the branch takes place.

Answers are stored with the question, so deleting a question will also remove all responses to that question. Questions can also be added after the survey is launched without compromising the survey, however users who have already completed the survey will appear to have not completed the new question.

You can reset the survey completely, which will remove all answers to all questions, or reset for particular users. There is also a permission `PloneSurvey: Reset Own Responses` that will allow users to reset their own responses and allow them to fill in the survey again.

Anonymous users are tracked with a cookie, so they will be unable to complete the survey more than once. However, if the anonymous user closes their browser and reopens the survey, they will be able to complete the survey as a new anonymous user. This is to support multiple user computers such as drop in computers within Libraries. The IP address is tracked, so users trying to spam the survey can be spotted within the results and these could be reset by the survey administrator.

There is also a permission, ``PloneSurvey: View Survey Results``, to grant users access to the results of the survey. This has not been fully tested and may not work as expected.

Respondents can be categorised as one of three kinds.

1. Portal members, who must have view permission on the survey in order to be able to complete it.

2. Anonymous users, who must have view permission, and you must have enabled the `allow anonymous` option on the survey.

3. Survey respondents, who can be added using the respondents tab on the survey. This allows you to add users with a one time token to allow a closed survey to be completed by users who are not portal members.

Respondents can be added individually, or can be bulk uploaded by uploading a file using the Import Respondents link under the respondents tab.

See also: `Plone Product Page for PloneSurvey <http://plone.org/products/plonesurvey>`_.


Known Issues
------------

The save functionality does not work reliably, and should not be used.

The confidential option on the survey does not do anything yet, and respondent's personal data is still saved to the system.


Source Code
-----------

The sources are in a GIT DVCS with its main master branch at `github <http://github.com/collective/Products.PloneSurvey>`_.

We'd be happy to see many commits, forks and pull-requests to make it even better.

