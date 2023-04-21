from django.shortcuts import render

from . import nas_modul

def kalkulacka(request):
    error_msg = None
    vysledek = None
    if request.method == "POST":
            try:
                float(request.POST["a"])
                float(request.POST["b"])
            except:
                error_msg = "A nebo B není číslo!"
                return render(request, "calculator/kalkulacka.html", dict(error_msg=error_msg, vysledek=vysledek))

            if(float(request.POST["b"]) == 0 and request.POST["operator"] == "/"):
                    error_msg = "Zero ERROR"
                    return render(request, "calculator/kalkulacka.html", dict(error_msg=error_msg, vysledek=vysledek))
            if(request.POST["operator"] == "+"):
                vysledek = nas_modul.secti(request.POST["a"], request.POST["b"])
            elif(request.POST["operator"] == "-"):
                vysledek = nas_modul.odecti(request.POST["a"], request.POST["b"])
            elif(request.POST["operator"] == "/"):
                vysledek = nas_modul.podil(request.POST["a"], request.POST["b"])
            elif(request.POST["operator"] == "*"):
                vysledek = nas_modul.soucin(request.POST["a"], request.POST["b"])
            else:
                error_msg = "Something went wrong :("
                return render(request, "calculator/kalkulacka.html", dict(error_msg=error_msg, vysledek=vysledek))
    return render(request, "calculator/kalkulacka.html", dict(error_msg=error_msg, vysledek=vysledek))