class UsernameBalanceMiddleware(object):
    def process_template_response(self, request, response):
        user = request.user
        if user.is_authenticated():
            if response.context_data is None:
                response.context_data = {}
            response.context_data['username'] = user.username
            response.context_data['balance'] = user.get_profile().balance
        return response
