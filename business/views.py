from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from business.models import Business, Category, Phone, BusinessCategory
from django.http import Http404, JsonResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict

# Create your views here.


def home(request):
    search_query = request.GET.get('q')

    listings = Business.objects.filter(active=1).all()

    if search_query:
        listings = listings.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)).all()

    data = {'listings': listings}
    return render(request, 'home.html', data)


def view_listing(request, id):
    try:
        listing = Business.objects.get(id=id)
    except Business.DoesNotExist:
        raise Http404

    listing.views = listing.views + 1
    listing.save()

    data = {'listing': listing}
    return render(request, 'view.html', data)


@csrf_exempt
def search(request):

    search_query = request.GET.get('q')

    listings = Business.objects.filter(active=1).all()

    if search_query:
        listings = listings.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)).all()

    directory = []
    for listing in listings:
        business = model_to_dict(listing, fields=[
                                 'id', 'name', 'description', 'website', 'contact_email', 'address', 'views'])
        business.update(
            {'categories': [cat for cat in listing.categories.values('id', 'title')]})
        business.update(
            {'phones': [phone for phone in listing.phones.values('id', 'number')]})
        directory.append(business)
    return JsonResponse({'status': 'success', 'data': directory})


@login_required(redirect_field_name='url', login_url='login')
def add_listing(request):
    categories = Category.objects.all()

    data = {'categories': categories,
            'breadcrumb': ['Dashboard', 'Add Listing']}
    return render(request, 'admin/add-listing.html', data)


@login_required(redirect_field_name='url', login_url='login')
def edit_listing(request, id):
    try:
        listing = Business.objects.get(id=id)
    except Business.DoesNotExist:
        raise Http404

    categories = Category.objects.all()

    data = {'categories': categories, 'listing': listing,
            'breadcrumb': ['Dashboard', 'Add Listing']}
    return render(request, 'admin/add-listing.html', data)


@login_required(redirect_field_name='url', login_url='login')
def delete_listing(request, id):
    try:
        listing = Business.objects.get(id=id)
    except Business.DoesNotExist:
        raise Http404

    listing.delete()

    return redirect('listings')


@login_required(redirect_field_name='url', login_url='login')
def deactivate_listing(request, id):
    try:
        listing = Business.objects.get(id=id)
    except Business.DoesNotExist:
        raise Http404

    listing.active = False
    listing.save()

    return redirect('listings')


@login_required(redirect_field_name='url', login_url='login')
def activate_listing(request, id):
    try:
        listing = Business.objects.get(id=id)
    except Business.DoesNotExist:
        raise Http404

    listing.active = True
    listing.save()

    return redirect('listings')


@login_required(redirect_field_name='url', login_url='login')
def post_add_listing(request):
    if request.method != 'POST':
        raise Http404

    business_id = request.POST.get('id')

    if business_id:
        update_business_fn(request)
    else:
        add_business_fn(request)

    return redirect('listings')


def add_business_fn(request):
    business = Business.objects.create(
        name=request.POST.get('name'),
        description=request.POST.get('description'),
        contact_email=request.POST.get('contact_email'),
        website=request.POST.get('website'),
        address=request.POST.get('address'),
        views=0
    )

    add_phones_fn(request, business)

    add_categories_fn(request, business)


def add_phones_fn(request, business):
    phones = [request.POST.get('primary_phone'),
              request.POST.get('other_phone')]
    for phone in phones:
        try:
            phone_obj = Phone.objects.create(number=phone, business=business)
        except:
            pass


def add_categories_fn(request, business):
    categories = request.POST.getlist('categories')

    for category_id in categories:
        try:
            category = Category.objects.get(pk=category_id)
            business_cat = BusinessCategory.objects.create(
                category=category, business=business)
        except Category.DoesNotExist:
            pass


def update_business_fn(request):
    try:
        business = Business.objects.get(pk=request.POST.get('id'))
    except Business.DoesNotExist:
        return Http404

    business.name = request.POST.get('name')
    business.description = request.POST.get('description')
    business.contact_email = request.POST.get('contact_email')
    business.website = request.POST.get('website')
    business.address = request.POST.get('address')

    business.save()

    Phone.objects.filter(business=business).delete()

    add_phones_fn(request, business)

    BusinessCategory.objects.filter(business=business).delete()

    add_categories_fn(request, business)


@login_required(redirect_field_name='url', login_url='login')
def post_add_category(request):
    if request.method != 'POST':
        raise Http404
    category = Category.objects.create(title=request.POST.get('title'))
    return redirect('categories')


@login_required(redirect_field_name='url', login_url='login')
def all_listings(request):
    listings = Business.objects.all()
    data = {'listings': listings,
            'breadcrumb': ['Dashboard', 'Listings']}
    return render(request, 'admin/listings.html', data)


@login_required(redirect_field_name='url', login_url='login')
def add_category(request):
    data = {'breadcrumb': ['Dashboard', 'Add Listing']}
    return render(request, 'admin/add-category.html', data)


@login_required(redirect_field_name='url', login_url='login')
def all_categories(request):
    categories = Category.objects.all()
    data = {'categories': categories,
            'breadcrumb': ['Dashboard', 'Categories']}
    return render(request, 'admin/categories.html', data)
