#!/bin/sh
TEMPLATES=`find ../skins -iregex '.*\..?pt'`

i18ndude rebuild-pot --pot plonesurvey.pot --create plonesurvey --merge manual.pot -s  $TEMPLATES
i18ndude sync -s --pot plonesurvey.pot plonesurvey-??.po

