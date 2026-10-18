"""Тесты API уведомлений."""

from unittest.mock import patch

import pytest

from notifications.models import Notification


def test_create_requires_auth(api_client):
    response = api_client.post(
        "/notifications/create/", {"topic": "t", "text": "x"}, format="json"
    )
    assert response.status_code == 401


@pytest.mark.django_db
def test_create_sets_owner_and_dispatches_task(auth_client, user, recipient):
    with patch("notifications.views.send_notification.delay") as mock_delay:
        response = auth_client.post(
            "/notifications/create/",
            {"topic": "t", "text": "x", "recipients": [recipient.pk]},
            format="json",
        )

    assert response.status_code == 201
    notification = Notification.objects.get()
    assert notification.owner_id == user.pk

    mock_delay.assert_called_once_with(notification.pk, [recipient.pk])
    task_id, recipient_ids = mock_delay.call_args.args
    assert isinstance(task_id, int)
    assert recipient_ids == [recipient.pk]
    assert all(isinstance(item, int) for item in recipient_ids)


@pytest.mark.django_db
def test_list_returns_only_own_notifications(auth_client, user, other_user):
    Notification.objects.create(topic="mine", owner=user)
    Notification.objects.create(topic="foreign", owner=other_user)

    response = auth_client.get("/notifications/list/")

    assert response.status_code == 200
    body = response.json()
    results = body["results"] if isinstance(body, dict) else body
    assert [item["topic"] for item in results] == ["mine"]


@pytest.mark.django_db
def test_retrieve_own_notification(auth_client, user):
    notification = Notification.objects.create(topic="mine", owner=user)

    response = auth_client.get(f"/notifications/read/{notification.pk}/")

    assert response.status_code == 200
    assert response.json()["topic"] == "mine"


@pytest.mark.django_db
def test_retrieve_foreign_notification_returns_404(auth_client, other_user):
    notification = Notification.objects.create(topic="foreign", owner=other_user)

    response = auth_client.get(f"/notifications/read/{notification.pk}/")

    assert response.status_code == 404
