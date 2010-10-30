## Script (Python) "crea_db"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=nome_db
##title=Crea DB
##

context.sql.agg_db(dbid=nome_db)
return nome_db
