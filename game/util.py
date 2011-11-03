from djangorestframework.response import ErrorResponse
from django.core.exceptions import ObjectDoesNotExist


def get_key_or_400(querydict, value):
    try:
        return querydict[value]
    except KeyError:
        raise ErrorResponse(400, content={'detail': 'missing ' + value})


def get_model_or_404(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except ObjectDoesNotExist:
        raise ErrorResponse(404,
                            {'detail': '{model} not found'.format(
                                                 model=model.__name__)})
