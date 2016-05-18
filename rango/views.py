from rango.models import Category, Page
from django.shortcuts import render
from rango.forms import CategoryForm, PageForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime


def index(request):
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    category_list = Category.objects.order_by('-likes')
    top_five_pages = Page.objects.order_by('-views')[:5]  # '-' means sort in descending order
    context_dict = {'categories': category_list, 'pages':top_five_pages}

    # Get the number of visits to the site.
    # We use the COOKIES.get() function to obtain the visits cookie.
    # If the cookie exists, the value returned is casted to an integer.
    # If the cookie doesn't exist, we default to zero and cast that.
    visits = request.session.get('visits')
    if not visits:
        visits = 1

    reset_last_visit_time = False
    last_visit = request.session.get('last_visit')
    if last_visit:
        last_visit_time = datetime.strptime(last_visit[:-7], '%Y-%m-%d %H:%M:%S')
        if (datetime.now() - last_visit_time).seconds > 0:
            visits += 1
            reset_last_visit_time = True
    else:
        reset_last_visit_time = True

    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits
    context_dict['visits'] = visits

    # We make use of the shortcut function to make our lives easier.
    # Return a rendered response to send to the client.
    return render(request, 'rango/index.html', context_dict)


def about(request):
    context_dict = {'about_message': 'Rango says here is the about page.'}
    if request.session.get("visits"):
        count = request.session.get('visits')
    else:
        count = 0
    context_dict['count'] = count
    return render(request, 'rango/about.html', context_dict)


def category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)  # If there isn't a category with given category_name_slug, a DoesNotExist exception will be thrown
        context_dict['category_name'] = category.name
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
        context_dict['category_name_slug'] = category.slug
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category
        # Don't do anything - the template displays the "no category" message.
        pass

    return render(request, 'rango/category.html', context_dict)


def add_category(request):
    if request.method == 'POST':  # An HTTP POST?
        form = CategoryForm(request.POST)
        if form.is_valid():
            # Save the new category to the database
            form.save(commit=True)
            # Now call the index() view
            # The user will be shown the homepage.
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print(form.errors)
    else:
        # If the request was not a POST, display the form to enter details.
        form = CategoryForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'rango/add_category.html', {'form': form})


def add_page(request, slug):
    try:
        cat = Category.objects.get(slug=slug)
    except Category.DoesNotExist:
        cat = None

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.view = 0
                page.save()
                return category(request, slug)
        else:
            print(form.errors)
    else:
        form = PageForm()

    context_dict = {'form': form, 'category': cat, 'slug': slug}
    return render(request, 'rango/add_page.html', context_dict)


@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this view.")
