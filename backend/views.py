from django.http import HttpResponse


def ola_view(request):
    return HttpResponse("Bem vindo ao leilão humano!")  # Resposta para o navegador
