from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.utils.decorators import decorator_from_middleware
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from social_event.services import authentication, attachment
from social_event.models import *
from social_event_admin.forms import *
from social_event_admin.middlewares import *

MAX_RESULT_PER_PAGE = 50

@require_http_methods(["GET", "POST"])
def sign_in(request):
    if request.method == "GET":
        form = SessionForm()
    else:
        form = SessionForm(request.POST)
        if form.is_valid():
            admin = authentication.sign_in(Admin, form.cleaned_data.get("username"), form.cleaned_data.get("password"))
            if admin:
                resposne = HttpResponseRedirect("/admin/events")
                resposne.set_cookie("token", admin.token, max_age=authentication.SESSION_DURATION)
                return resposne
            else:
                # TODO: Add a utils for this. It's so ugly this way.
                form._errors["__all__"] = ["Incorrect combination of username and password."]
    return render(request, "sessions/new.html", {"form": form})

@require_http_methods(["GET", "POST"])
@decorator_from_middleware(AdminTokenValidateMiddleware)
def events(request):
    if request.method == "GET":
        page = request.GET.get('page')
        events = Event.objects.order_by('-id')
        paginator = Paginator(events, MAX_RESULT_PER_PAGE)
        try:
            event_page = paginator.page(page)
        except PageNotAnInteger:
            event_page = paginator.page(1)
        except EmptyPage:
            event_page = paginator.page(paginator.num_pages)

        return render(request, "events/index.html", {"event_page": event_page})
    else:
        form = EventForm(request.POST, request.FILES, prefix="event")
        if form.is_valid():
            event = form.save()
            formset = PictureFormSet(request.POST, request.FILES, instance=event, prefix="pictures")
            if formset.is_valid():
                formset.save()
            return HttpResponseRedirect("/admin/events/" + str(event.id))

@require_http_methods(["GET", "POST"])
@decorator_from_middleware(AdminTokenValidateMiddleware)
def event(request, id):
    event = get_object_or_404(Event, id=id)
    if request.method == "GET":
        form = EventForm(instance=event, prefix="event")
        formset = PictureFormSet(instance=event, prefix="pictures")
    else:
        form = EventForm(request.POST, request.FILES, instance=event, prefix="event")
        formset = PictureFormSet(request.POST, request.FILES, instance=event, prefix="pictures")
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return HttpResponseRedirect("/admin/events/" + str(event.id))
    return render(request, "events/form.html", {"form": form, "formset": formset})

@require_GET
@decorator_from_middleware(AdminTokenValidateMiddleware)
def event_new(request):
    form = EventForm(prefix="event")
    formset = PictureFormSet(prefix="pictures")
    return render(request, "events/form.html", {"form": form, "formset": formset})
