PARENTS = context.REQUEST.PARENTS

if context.meta_type == 'Survey':
    return context
for parent in PARENTS:
    if parent.meta_type == 'Survey':
        return parent

return