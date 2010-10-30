## Script (Python) "vuoto"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=record
##title=
##
valore = ''

for r in record.keys():
 if r <> 'orderindex_':
  valore = valore + record[r].strip()

return valore
if valore == '':
 return 0
else:
 return 1
