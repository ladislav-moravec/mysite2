from django.shortcuts import redirect

def index_handler(request):
    return redirect("clientapp/klient_index")


