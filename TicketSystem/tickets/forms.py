from django import forms
from django_summernote.widgets import  SummernoteWidgetBase, SummernoteWidget

from .models import Ticket, File, TicketComment


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['product', 'subject', 'text']


class TicketChangingStatusForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['status', 'responsible_user']
        widgets = {'status': forms.HiddenInput(),
                   'responsible_user': forms.HiddenInput()}



class AddFileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['file']
        #Add file extns checking


#Comment Form
'''
Completed. Need IMPORT MODEL'''


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = TicketComment
        fields = ['message']

