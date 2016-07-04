from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.http import HttpResponseRedirect


class UploadView(View):
    # препраща към fail_url, когато формата е невалидна
    error_message = 'Invalid form!'

    @method_decorator(login_required)
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    @method_decorator(login_required)
    def post(self, request, friends=None):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            self.post_function(request.user, form, friends)
            return HttpResponseRedirect(self.success_url)
        else:
            return render(request, 'error.html', {'error': self.error_message})
