#!/bin/sh

DOMAIN='plonesurvey'

i18ndude rebuild-pot --pot ${DOMAIN}.pot --create ${DOMAIN} ..
i18ndude rebuild-pot --pot plone.pot --create plone ../profiles/default/types

i18ndude sync --pot ${DOMAIN}.pot */LC_MESSAGES/${DOMAIN}.po
i18ndude sync --pot plone.pot */LC_MESSAGES/plone.po
# Updating "plone" domain
i18ndude sync --pot plonesurvey-plone.pot plonesurvey-plone-??.po