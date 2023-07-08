import pytest

from api_requests import get_user, login, register, get_adv, patch_adv, post_adv, logout, delete_adv
from config import DEFAULT_USER, DEFAULT_PASSWORD


def test_register():
    user_id = register(DEFAULT_USER, DEFAULT_PASSWORD)
    assert isinstance(user_id, int)


def test_invalid_email():
    with pytest.raises(ApiError) as error:
        register("invalid_email", DEFAULT_PASSWORD)

    assert error.value.status_code == 400
    assert error.value.message == {
        "status": "error",
        "description": [{"loc": ["email"], "msg": "value is not a valid email address", "type": "value_error.email"}],
    }


def test_register_existed(new_user):
    with pytest.raises(ApiError) as error:
        register(new_user["email"], DEFAULT_PASSWORD)
    assert error.value.status_code == 409
    assert error.value.message == {'description': 'such user already exists', 'status': 'error'}


def test_login(new_user):
    response = login(new_user["email"], new_user["password"])
    assert response == {'status': 'Auth is successfully'}


def test_logout(new_user):
    login(new_user["email"], new_user["password"])
    response = logout(new_user["email"], new_user["password"])
    assert response == 'logout'


def test_login_incorrect(new_user):
    with pytest.raises(ApiError) as error:
        login(new_user["email"], new_user["password"] + "a")
    assert error.value.status_code == 401
    assert error.value.message['description'] == {'status': 'Not authenticated'}


def test_get_user(new_user):
    user = get_user(new_user["id"])
    assert user["email"] == new_user["email"]


def test_get_not_existing_user():
    with pytest.raises(ApiError) as er:
        get_user(9999999)
    assert er.value.status_code == 404
    assert er.value.message == {'description': 'User not exists', 'status': 'error'}


def test_post_adv(new_user):
    login(new_user["email"], new_user["password"])
    new_adv = post_adv("new_title", "new_description")
    assert isinstance(new_adv["id"], int)
    assert new_adv["title"] == "new_title"


def test_post_adv_without_login(new_user):
    login(new_user["email"], new_user["password"])
    with pytest.raises(ApiError) as error:
        logout(new_user["email"], new_user["password"])
        post_adv("new_title", "new_description")
    assert error.value.status_code == 400
    assert error.value.message["description"] == "User not login"


def test_get_adv(new_adv):
    adv = get_adv(new_adv["id"])
    assert adv["title"] == new_adv["title"]


def test_get_adv_without_login(new_adv):
    adv = get_adv(new_adv["id"])
    assert adv["title"] == new_adv["title"]


def test_patch_adv(new_adv):
    login(new_adv["email"], new_adv["password"])
    adv = patch_adv(new_adv["id"], "new_description")
    assert adv["title"] == new_adv["title"]


def test_patch_adv_without_login(new_adv):
    with pytest.raises(ApiError) as error:
        patch_adv(new_adv["id"], "new_description")
    assert error.value.status_code == 403
    assert error.value.message['description'] == 'Access denied'


def test_delete_adv(new_adv):
    login(new_adv["email"], new_adv["password"])
    response = delete_adv(new_adv['id'])
    assert response == 'deleted'


def test_patch_adv_from_not_owner(root_user, new_adv):
    login(root_user["email"], root_user["password"])
    with pytest.raises(ApiError) as error:
        patch_adv(new_adv["id"], "new_description")
    assert error.value.status_code == 403
    assert error.value.message['description'] == 'Access denied'


def test_delete_adv_from_not_owner(root_user, new_adv):
    login(root_user["email"], root_user["password"])
    with pytest.raises(ApiError) as error:
        delete_adv(new_adv['id'])
    assert error.value.status_code == 403
    assert error.value.message['description'] == 'Access denied'
