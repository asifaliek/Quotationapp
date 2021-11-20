from django.shortcuts import render

# Create your views here.

# @login_required
def dashboard(request):

    context = {
        "title": " Test | Dashboard",
        "is_index":True,
    }
    return render(request, 'index.html', context)
