from django.shortcuts import render
from django.http import HttpResponseRedirect
import logging
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import Book, BookInstance, Visitor, Registration, User
from django.urls import reverse_lazy
from django.forms.models import inlineformset_factory

logger = logging.getLogger(__name__)

BookFormset = inlineformset_factory(
    Registration, BookInstance, fields=('type',), can_delete=False
)


def index(request):
    return render(
        request,
        'home.html'
    )


class BooksView(ListView):
    model = Book
    queryset = Book.objects.all()
    template_name = 'book_list.html'

    pass


class BookDetail(DetailView):
    model = Book
    pk_url_kwarg = 'id'
    template_name = 'book_detail.html'
    pass


class VisitorsView(ListView):
    model = Visitor
    queryset = Visitor.objects.all()
    template_name = 'visitor_list.html'
    pass


class VisitorDetail(DetailView):
    model = Visitor
    pk_url_kwarg = 'id'
    template_name = 'visitor_detail.html'
    pass


class RegistrationsView(ListView):
    model = Registration
    queryset = Registration.objects.all()
    template_name = 'registration_list.html'
    pass


class RegistrationDetail(DetailView):
    model = Registration
    pk_url_kwarg = 'id'
    template_name = 'registration_detail.html'
    pass


class RegistrationCreate(CreateView):
    model = Registration
    fields = ('lend_date', 'return_date', 'visitor')
    success_url = reverse_lazy('registrations')

    def get_form(self, form_class=None):
        from django.forms.widgets import SelectDateWidget
        form = super(RegistrationCreate, self).get_form()
        form.fields['lend_date'].widget = SelectDateWidget()
        form.fields['return_date'].widget = SelectDateWidget()
        return form

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['children'] = BookFormset(self.request.POST)
        else:
            data['children'] = BookFormset()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        books = context['children']
        self.object = form.save()
        if books.is_valid():
            books.instance = self.object
            books.save()
            return super().form_valid(form)
        else:
            self.object.delete()
            return HttpResponseRedirect('/registrations/add/')

    def get_success_url(self):
        return reverse_lazy('registrations')

    pass


class RegistrationDelete(DeleteView):
    model = Registration
    success_url = reverse_lazy('registrations')
    pk_url_kwarg = 'id'

    def post(self, request, *args, **kwargs):
        if "Cancel" in request.POST:
            return HttpResponseRedirect(self.success_url)
        else:
            return super(RegistrationDelete, self).post(request, *args, **kwargs)
    pass


class RegistrationUpdate(UpdateView):
    model = Registration
    pk_url_kwarg = 'id'
    fields = ('lend_date', 'return_date', 'visitor')
    template_name = 'library_app/registration_update.html'



