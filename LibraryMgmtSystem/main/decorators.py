from django.http import HttpResponse
from django.shortcuts import redirect

def is_authorised_user(view_func):
	def wrapper_func(request, *args, **kwargs):

		'''somehow checking groups is not reliable'''
		# group = None

		# if request.user.is_authenticated and request.user.groups.exists():
		# 		group = request.user.groups.all()[0].name

		# 		if group == 'admin':
		# 			return redirect('dashboard')

		if request.user.is_authenticated and request.user.is_staff:
				return redirect('dashboard')
			
		return view_func(request, *args, **kwargs)

	return wrapper_func
