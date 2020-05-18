from django.test import RequestFactory
from django.urls import resolve, reverse
from django.contrib.auth.models import AnonymousUser
from mixer.backend.django import mixer
import pytest
from . import models
from . import views


@pytest.fixture
def factory(db):
    return RequestFactory()


@pytest.fixture
def user_factory(db):
    return mixer.blend(models.User)


def test_detail_visitor():
    path = reverse('visitor-detail', kwargs={'id': 1})
    assert resolve(path).view_name == 'visitor-detail'


def test_detail_book():
    path = reverse('book-detail', kwargs={'id': 1})
    assert resolve(path).view_name == 'book-detail'


def test_create_no_auth(factory):
    path = reverse('registration-add')
    request = factory.get(path)
    request.user = AnonymousUser()

    view = views.RegistrationCreate.as_view()
    response = view(request)

    assert response.status_code == 302


def test_create_auth(factory, user_factory):
    path = reverse('registration-add')
    request = factory.get(path)
    request.user = user_factory

    view = views.RegistrationCreate.as_view()
    response = view(request)

    assert response.status_code == 200


def test_delete_no_auth(factory):
    path = reverse('registration-del', kwargs={'id': 1})
    request = factory.get(path)
    request.user = AnonymousUser()

    view = views.RegistrationCreate.as_view()
    response = view(request)

    assert response.status_code == 302


def test_delete_auth(factory, user_factory):
    path = reverse('registration-del', kwargs={'id': 1})
    request = factory.get(path)
    request.user = user_factory

    view = views.RegistrationCreate.as_view()
    response = view(request)

    assert response.status_code == 200
