from django.shortcuts import render

from collecti_stamp.app.models import Tickets


# Create your views here.
def home(request):
    if request.method == 'POST':
        # TODO: Cambiar a producto y realizar compra desde inicio.
        ticket_id = request.POST.get('ticket_id')
        ticket = Tickets.objects.get(uuid=ticket_id)
        print(ticket.user)
        if ticket.user is None:
            ticket.user = request.user
            ticket.save()
            return render(request, 'base/details.html',
                            {'ticket': ticket, 'message': 'Ticket was successfully assigned', 'status': 'Success'})
        else:
            return render(request, 'base/details.html',
                            {'ticket': ticket, 'message': 'Ticket is already assigned', 'status': 'Error'})
    return render(request, 'base/home.html')