from django.shortcuts import get_object_or_404,render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .models import Listing
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
    return render(request,'listings/search.html')
