from django.conf import settings


def google_tag_manager_id(request):
    if settings.ENV in ["beta", "prod"]:
        return {"GOOGLE_TAG_MANAGER_ID": settings.GOOGLE_TAG_MANAGER_ID}
    else:
        return {}


def static_url(request):
    return {"STATIC_URL": settings.STATIC_URL}
