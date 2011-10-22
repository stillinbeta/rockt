from django.http import HttpResponseBadRequest

from djangohttpdigest.http import HttpResponseNotAuthorized
from djangohttpdigest.digest import Digestor, parse_authorization_header
from djangohttpdigest.authentication import SimpleHardcodedAuthenticator, ClearTextModelAuthenticator, ModelAuthenticator

def protect_method_digest_model(model, realm, realm_field=None, 
                                username_field='username',
                                password_field='password'):
    def _innerDecorator(function):
        def _wrapper(self, request, *args, **kwargs):
            
            digestor = Digestor(method=request.method, path=request.path, realm=realm)
            if request.META.has_key('HTTP_AUTHORIZATION'):
                try:
                    parsed_header = digestor.parse_authorization_header(request.META['HTTP_AUTHORIZATION'])
                except ValueError, err:
                    return HttpResponseBadRequest(err)

                if parsed_header['realm'] == realm:
                    authenticator = ClearTextModelAuthenticator(model=model, realm=realm, realm_field=realm_field, username_field=username_field, password_field=password_field)
                    if authenticator.secret_passed(digestor):
                        return function(self, request, *args, **kwargs)
                
            # nothing received, return challenge
            response = HttpResponseNotAuthorized("Not Authorized")
            response['www-authenticate'] = digestor.get_digest_challenge()
            return response
        return _wrapper
    return _innerDecorator
