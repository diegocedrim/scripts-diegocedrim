import refactorings
import issues

reopening_by_class = {}

for ref in refactorings.all():
    tline = issues.timeline(ref)
    if tline and issues.was_reopened(tline):
        clazz = ref["classification"]
        reopening_by_class[clazz] = reopening_by_class.get(clazz, 0) + 1

for i in reopening_by_class:
    print i, "\t", reopening_by_class[i]