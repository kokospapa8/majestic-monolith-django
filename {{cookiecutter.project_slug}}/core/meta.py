# -*- coding: utf-8 -*-
from django.conf import settings
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


def get_default(request, meta=None):
    def get_facebook_locale(request):
        fb_locale = 'en_US'
        if request is None:
            return fb_locale
        try:
            # nujabes8: exception for fil and maybe other with different prefix
            if request.LANGUAGE_CODE == "fil":
                return "tl_PH"
            elif request.LANGUAGE_CODE == "zh-cn":
                return "zh_CN"
            elif request.LANGUAGE_CODE == "zh-tw":
                return "zh_TW"

            locale = request.LANGUAGE_CODE[:2]
            for og_locale in settings.OG_LOCALES:
                if locale in og_locale:
                    fb_locale = og_locale
                    break
            return fb_locale
        except:
            return fb_locale

    def check_key(key, dictionary):
        if key in dictionary.keys():
            return dictionary[key]
        else:
            return None

    locales = list(settings.OG_LOCALES)

    info = meta or {}
    info['title'] = check_key('title', info) or "dmm title"
    info['description'] = check_key(
        'description', info) or "dmm description."
    info['image_src'] = check_key('og:image', info) or (
        f'{settings.STATIC_URL}{settings.ENV}/img/web/logo.png')

    info['og:image'] = check_key('og:image', info) or info['image_src']
    info['og:description'] = check_key('og:description', info) or info['description']
    info['og:url'] = check_key('og:url', info) or settings.SITE_URL
    info['og:title'] = check_key('og:title', info) or info['title']

    # info['fb:app_id'] = settings.FACEBOOK_APP_ID
    info['og:locale'] = check_key('og:locale', info) or get_facebook_locale(request)
    info['og:type'] = check_key('og:type', info) or 'website'
    info['og:site_name'] = check_key('og:site_name', info) or '{{cookiecutter.project_slug}}'
    try:
        locales.remove(info['og:locale'])
    except ValueError:
        info['og:locale'] = 'en_US'
        locales.remove(info['og:locale'])
    info['og:locale:alternate'] = locales
    return info

# https://gist.github.com/lancejpollard/1978404
