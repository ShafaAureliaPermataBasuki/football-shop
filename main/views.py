from django.shortcuts import render

def show_main(request):
    context = {
        'app_name': 'Football Shop',
        'nama': 'Shafa Aurelia Permata Basuki',
        'kelas': 'PBP C',
    }
    return render(request, "main.html", context)
