from django.shortcuts import get_object_or_404,render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .models import Listing
from listings.choices import bedroom_choices,price_choices,state_choices
# Create your views here.

def index(request):
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)

    paginator = Paginator(listings,2)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    contex = {
        'listings':paged_listings
    }
    return render(request,'listings/listings.html',contex)

def listing(request,listing_id):
    listing = get_object_or_404(Listing,pk=listing_id)
    contex = {
        'listing':listing
    }
    return render(request,'listings/listing.html',contex)


def search(request):
    queryset_list = Listing.objects.order_by('-list_date')

    #keywords
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(description__icontains=keywords)
    
    #city
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            queryset_list = queryset_list.filter(city__iexact=city)

    #state
    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            queryset_list = queryset_list.filter(state__iexact=state)

    #bedrooms
    if 'bedrooms' in request.GET:
        bedroom = request.GET['bedrooms']
        if bedroom:
            queryset_list = queryset_list.filter(bedroom__lte=bedroom)

    #price
    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            queryset_list = queryset_list.filter(price__lte=price)

    contex = {
        'bedroom_choices':bedroom_choices,
        'price_choices':price_choices,
        'state_choices':state_choices,
        'listings':queryset_list

    }
    return render(request,'listings/search.html',contex)
