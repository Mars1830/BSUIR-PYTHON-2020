from django.contrib.auth import logout
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.forms.models import inlineformset_factory
from django.template import loader
from django.core.mail import send_mail
from multiprocessing import Pool
from background_task import background
from .models import Book, BookInstance, Visitor, Registration, User
from .tokens import account_activation_token
from .forms import SignUpForm
import logging

logger = logging.getLogger(__name__)

BookFormset = inlineformset_factory(
    Registration, BookInstance, fields=('type',), can_delete=False
)


def index(request):
    return HttpResponseRedirect('accounts/login')


def home(request):
    return render(
        request,
        'base.html')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/accounts/login/')


def sign_up_success(request):
    return render(request, 'registration/sign_up-success.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponseRedirect('/accounts/login')
    else:
        return HttpResponse('Activation link is invalid!')


class SignUpFormView(FormView):
    form_class = SignUpForm
    success_url = reverse_lazy('sign-up-success')
    template_name = 'registration/sign_up.html'

    def form_valid(self, form):
        user = form.save()
        email_to = form.data['email']

        self.email_user(user, email_to)
        # pool.map(email_user, [self.request, user, email_to])
        return super(SignUpFormView, self).form_valid(form)

    def form_invalid(self, form):
        return super(SignUpFormView, self).form_invalid(form)

    def email_user(self, user, email_to):
        current_site = get_current_site(self.request)
        mail_subject = 'Activate your library account'
        t = loader.get_template('jinja2/acc_activate_email.html')
        message = t.render(request=self.request,
                           context={'user': user,
                                    'domain': current_site.domain,
                                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                    'token': account_activation_token.make_token(user)})
        email_from = 'm.pouga@outlook.com'

        s_send(mail_subject, message, email_from, email_to)
    pass


# @background()
def s_send(mail_subject, message, email_from, email_to):
    send_mail(subject=mail_subject, message=message, from_email=email_from, recipient_list=[email_to, ])


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

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)

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

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)

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

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)

    model = Registration
    pk_url_kwarg = 'id'
    fields = ('lend_date', 'return_date', 'visitor')
    template_name = 'library_app/registration_update.html'



