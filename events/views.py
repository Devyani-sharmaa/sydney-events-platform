from django.shortcuts import render, get_object_or_404, redirect
from .models import Event, TicketClick
from .forms import TicketForm


def event_list(request):
    events = Event.objects.exclude(status="inactive").order_by("-last_scraped_at")
    return render(request, "event_list.html", {"events": events})


def get_tickets(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            TicketClick.objects.create(
                event=event,
                email=form.cleaned_data["email"],
                consent=form.cleaned_data["consent"],
            )
            return redirect(event.source_url)
    else:
        form = TicketForm()

    return render(request, "ticket_form.html", {"form": form, "event": event})



def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, "event_detail.html", {"event": event})

