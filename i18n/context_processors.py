from django.conf import settings
from django.utils.translation import get_language

def language_info(request):
    """Add language info to all template contexts."""
    current_lang = get_language()
    lang_name = dict(settings.LANGUAGES).get(current_lang, 'English')
    return {
        'available_languages': settings.LANGUAGES,
        'current_language_code': current_lang,
        'current_language_name': lang_name,
    }