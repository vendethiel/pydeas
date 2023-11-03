from ideas.helpers.user import can_see_unvalidated


def validated_filter(qs, user):
    if can_see_unvalidated(user):
        return qs.all()
    else:
        return qs.filter(validated=True)
