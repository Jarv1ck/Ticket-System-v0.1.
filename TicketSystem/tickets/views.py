from django.shortcuts import render, HttpResponse, get_object_or_404, HttpResponseRedirect, reverse
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Ticket, TicketComment, File, Product
from .forms import TicketForm, AddFileForm, AddCommentForm, TicketChangingStatusForm

'''
Rebuild to CLASS BASED VIEWS !IMPORTANT 
'''


@login_required
def main(request):
    last_five_tickets = Ticket.objects.all()[:6]
    #Dashboard of three cases status N/TB/C
    ticket_new = Ticket.objects.filter(status='New').count()
    ticket_tb = Ticket.objects.filter(status='Troubleshooting').count()
    ticket_closed = Ticket.objects.filter(status='Closed').count()
    admin_ticket = Ticket.objects.all()

    return render(request, 'tickets/main.html', {'last_five_tickets' : last_five_tickets,
                                                 'ticket_new': ticket_new,
                                                 'ticket_tb': ticket_tb,
                                                 'ticket_closed': ticket_closed,
                                                 'admin_ticket': admin_ticket})


''' Ticket list view function | permission settings'''


@login_required
def ticket_list(request):
    tickets = Ticket.objects.filter(creator=request.user)
    ticket_admin = Ticket.objects.all()
    return render(request, 'tickets/list.html', {'tickets': tickets,
                                                 'ticket_admin': ticket_admin,})


'''Ticket detail view function, adding comment, adding file, changing ticket status'''


@login_required
def ticket_detail(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    files = File.objects.filter(ticket=ticket)
    form = AddCommentForm()
    form_status = TicketChangingStatusForm(request.POST or None, instance=ticket)
    comment = TicketComment(creator=request.user, ticket=ticket)
    comments = TicketComment.objects.filter(ticket=ticket)

    if request.method == 'POST':
        if form_status.is_valid():
            #Change status form-button
            form_status.save(commit=False)
            if ticket.status == 'New':
                user = User.objects.get(id=request.user.pk)
                ticket.responsible_user = user
                ticket.status = 'Troubleshooting'
            elif ticket.status == 'Troubleshooting':
                ticket.status = 'Closed'
            form_status.save()
            #Add comment form
        form = AddCommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            subject = 'New comment in ticket #{}'.format(ticket.pk)
            message = 'You have new message from {}:\n' \
                      '{}'.format(comment.creator, comment.message)
            from_smtp = 'smtpserverffff@gmail.com'
            to = ['jojopanda8093@gmail.com', ticket.creator.email]
            send_mail(subject, message, from_smtp, to)
            #Adding sendmail to admin and to creator of comment
        return HttpResponseRedirect(reverse('tickets:detail', args=[ticket.pk]))
    else:
        form = AddCommentForm()
        context = {'form': form, 'ticket': ticket,
                   'files': files, 'comments': comments,
                   'form_status': form_status}
        return render(request, 'tickets/detail.html', context)


'''Create ticket view function, email sending'''


@login_required
def create_ticket(request):
    ticket = Ticket(creator=request.user)

    if request.method == 'POST':
        form = TicketForm(request.POST or None, instance=ticket)
        if form.is_valid():
            form.save()
            '''Sending mail to admin about creating ticket'''
            subject = request.POST['subject']
            message = request.POST['text']
            from_smtp = 'smtpserverfffff@gmail.com'
            to = ['jojopanda8093@gmail.com']
            send_mail(subject, message, from_smtp, to)

            return HttpResponseRedirect(reverse('tickets:detail', args=[ticket.pk]))
    else:
        form = TicketForm()
        return render(request, 'tickets/create.html', {'form': form,})


'''
Checking files extension
'''


''' Adding files to existing tickets'''


@login_required
def add_file_to_ticket(request, pk):
    ticket = get_object_or_404(Ticket, id=pk)
    form = AddFileForm()

    if request.method == 'POST':
        file = File(ticket=ticket, name=request.FILES['file'])
        form = AddFileForm(request.POST, request.FILES, instance=file)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse('tickets:detail', args=[ticket.pk]))
    else:
        form = AddFileForm()
        return render(request, 'tickets/add.html', {'form': form})


''' Deleting ticket view function '''


@login_required
def delete_view(request, id):
    ticket = get_object_or_404(Ticket, id=id)

    if request.method == 'POST':
        ticket.delete()
        return HttpResponseRedirect(reverse('tickets:list'))
    return render(request, 'tickets/delete.html', {})



