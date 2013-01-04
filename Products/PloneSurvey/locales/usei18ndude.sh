#!/bin/sh

i18ndude rebuild-pot --pot plonesurvey.pot --create plonesurvey ..
i18ndude sync --pot plonesurvey.pot plonesurvey-??.po

# Updating "plone" domain
i18ndude sync --pot plonesurvey-plone.pot plonesurvey-plone-??.po