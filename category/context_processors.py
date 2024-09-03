from . models import Category

def menu_links(request):
    links = Category.objects.all()
    return dict(links=links)


# Since we use context processor ,we need to tell our templates we are using context processor
