from src.adminauction.models import UserPermission


def theme(request):
    themes = UserPermission.objects.all()
    return {"themes": themes}


def site_name(request):
    site_name = UserPermission.objects.all()
    return {"site_name": site_name}
