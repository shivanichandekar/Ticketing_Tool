from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.template.loader import get_template, TemplateDoesNotExist
from django.http import HttpResponseServerError, HttpResponseNotFound
from .models import Ticket
from .forms import TicketForm, CommentForm
from django.template.loader import get_template
from django.http import HttpResponse


# Test template loading
def test_template(request):
    try:
        get_template('tickets/ticket_detail.html')
        return HttpResponse("Template found!")
    except TemplateDoesNotExist:
        return HttpResponse("Template not found!", status=404)

@method_decorator(login_required, name='dispatch')
class TicketListView(ListView):
    model = Ticket
    template_name = 'tickets/ticket_list.html'
    context_object_name = 'tickets'

    def get_queryset(self):
        try:
            status = self.request.GET.get('status')
            if status:
                return Ticket.objects.filter(status=status)
            return Ticket.objects.all()
        except Exception as e:
            # Handle any unexpected errors, log the exception if necessary
            return HttpResponseServerError(f"Error retrieving tickets: {str(e)}")


@method_decorator(login_required, name='dispatch')
class TicketDetailView(DetailView):
    model = Ticket
    template_name = 'tickets/ticket_detail.html'
    context_object_name = 'ticket'

    def get_object(self):
        try:
            return super().get_object()
        except Ticket.DoesNotExist:
            # Handle case where ticket is not found
            return HttpResponseNotFound("Ticket not found.")

@method_decorator(login_required, name='dispatch')
class TicketCreateView(CreateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'tickets/ticket_form.html'
    success_url = reverse_lazy('ticket_list')

    def form_valid(self, form):
        try:
            form.instance.creator = self.request.user
            return super().form_valid(form)
        except Exception as e:
            # Handle form errors or database issues
            return HttpResponseServerError(f"Error creating ticket: {str(e)}")

    def form_invalid(self, form):
        # Return response for invalid form
        return self.render_to_response(self.get_context_data(form=form))


@method_decorator(login_required, name='dispatch')
class TicketUpdateView(UpdateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'tickets/ticket_form.html'
    success_url = reverse_lazy('ticket_list')

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except Exception as e:
            # Handle form submission errors
            return HttpResponseServerError(f"Error updating ticket: {str(e)}")

@login_required
def comment_create(request, ticket_id):
    try:
        ticket = get_object_or_404(Ticket, pk=ticket_id)
    except Ticket.DoesNotExist:
        return HttpResponseNotFound("Ticket not found.")

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            try:
                comment = form.save(commit=False)
                comment.ticket = ticket
                comment.user = request.user
                comment.save()
                return redirect('ticket_detail', pk=ticket_id)
            except Exception as e:
                # Handle comment saving errors
                return HttpResponseServerError(f"Error saving comment: {str(e)}")
    else:
        form = CommentForm()

    return render(request, 'tickets/comment_form.html', {'form': form, 'ticket': ticket})
