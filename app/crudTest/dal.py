from crudTest.models import M


def add_multiple(model: M, obj_set: list[M]):
    model.objects.bulk_create(obj_set)


def get_all(model: M) -> list[M]:
    return list(model.objects.all())


def get_many(model: M, ids: list[int]) -> list[M]:
    return list(model.objects.filter(pk__in=ids))


def get_one(model: M, obj_id: int) -> M:
    return model.get(pk=obj_id)
