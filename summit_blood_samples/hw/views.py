from django.views import View
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse
from django.shortcuts import render



class hw(View):
    """
    Class for User management, where Admin can add/block/delete a user.
    """
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        """
        Method for GET Request
        :param request: Request
        :param args: args
        :param kwargs: kwargs
        :return: HttpResponse object
        """
        return render(request, self.template_name,
                      {})
