import logging
from django.utils import translation
from django.conf import settings

logger = logging.getLogger(__name__)

class LanguageDetectionMiddleware:
    """Auto-detect language from visitor IP address.
    
    Uses django-geoip2 to determine country, then maps to language.
    Falls back to browser Accept-Language header.
    Session-stored language preference takes priority.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Check if language is specified via GET parameter (?lang=en)
        lang_from_param = request.GET.get('lang')
        
        # Check if language is already set in session or cookie (user override)
        lang_from_session = request.session.get('django_language')
        lang_from_cookie = request.COOKIES.get('django_language')
        
        # Priority: URL param > session > cookie > IP detection > Accept-Language
        if lang_from_param and lang_from_param in dict(settings.LANGUAGES):
            lang = lang_from_param
            translation.activate(lang)
            request.LANGUAGE_CODE = translation.get_language()
            response = self.get_response(request)
            response.set_cookie('django_language', lang, max_age=86400 * 365)
            return response
        
        if lang_from_session or lang_from_cookie:
            lang = lang_from_session or lang_from_cookie
            if lang in dict(settings.LANGUAGES):
                translation.activate(lang)
                request.LANGUAGE_CODE = translation.get_language()
                response = self.get_response(request)
                response.set_cookie('django_language', lang)
                return response
        
        # Try to detect from IP
        lang = self._detect_from_ip(request)
        if lang:
            translation.activate(lang)
            request.LANGUAGE_CODE = translation.get_language()
            response = self.get_response(request)
            response.set_cookie('django_language', lang, max_age=86400 * 365)
            return response
        
        # Fall back to Accept-Language header (Django default behavior)
        response = self.get_response(request)
        return response
    
    def _detect_from_ip(self, request):
        """Detect language from client IP address using GeoIP."""
        try:
            import geoip2.database
            import os
            
            # Try to find GeoIP database
            geoip_path = os.path.join(settings.BASE_DIR, 'geoip', 'GeoLite2-Country.mmdb')
            if os.path.exists(geoip_path):
                reader = geoip2.database.Reader(geoip_path)
                ip = self._get_client_ip(request)
                if ip and ip != '127.0.0.1' and ip != '::1':
                    response = reader.country(ip)
                    country_code = response.country.iso_code
                    reader.close()
                    if country_code in settings.COUNTRY_LANGUAGE_MAP:
                        return settings.COUNTRY_LANGUAGE_MAP[country_code]
        except Exception as e:
            logger.warning(f"GeoIP detection failed: {e}")
        return None
    
    def _get_client_ip(self, request):
        """Extract client IP from request headers."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')


class DeviceDetectionMiddleware:
    """Add device type info to request for responsive templates."""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
        
        # Simple mobile/tablet/desktop detection
        if 'mobile' in user_agent or 'android' in user_agent and 'mobile' in user_agent:
            request.device_type = 'mobile'
        elif 'tablet' in user_agent or 'ipad' in user_agent:
            request.device_type = 'tablet'
        else:
            request.device_type = 'desktop'
        
        # Screen size hint for responsive design
        if 'iphone' in user_agent or 'android' in user_agent:
            request.screen_size_hint = 'small'
        elif 'ipad' in user_agent or 'tablet' in user_agent:
            request.screen_size_hint = 'medium'
        else:
            request.screen_size_hint = 'large'
        
        response = self.get_response(request)
        return response