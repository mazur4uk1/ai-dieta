import pytest
from app.services.auth_service import AuthService
from app.schemas.auth import UserRegister


def test_register_user(db_session):
    user_data = UserRegister(email="test@example.com", password="Test1234", first_name="Test", last_name="User")
    user = AuthService.register_user(
        db_session, user_data.email, user_data.password, user_data.first_name, user_data.last_name
    )
    assert user.email == "test@example.com"
    assert user.first_name == "Test"


def test_register_user_assigns_free_subscription(db_session):
    from app.models.subscription import Subscription

    user = AuthService.register_user(db_session, "sub@example.com", "Test1234", "Sub", "User")
    subscription = db_session.query(Subscription).filter(Subscription.user_id == user.id).first()
    assert subscription is not None
    assert subscription.tier.name.lower() == "free"


def test_authenticate_user(db_session):
    # First register
    AuthService.register_user(db_session, "auth@example.com", "Test1234", "Auth", "User")
    # Then authenticate
    user = AuthService.authenticate_user(db_session, "auth@example.com", "Test1234")
    assert user.email == "auth@example.com"


def test_create_sms_code(db_session):
    code = AuthService.create_sms_code(db_session, "+1234567890")
    assert code == "123456"  # In development mode


def test_verify_sms_code(db_session):
    phone = "+1234567890"
    code = AuthService.create_sms_code(db_session, phone)
    result = AuthService.verify_sms_code(db_session, phone, code)
    assert result is True