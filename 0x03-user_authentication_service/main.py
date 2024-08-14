#!/usr/bin/env python3
"""
Main file
"""
import requests


def register_user(email: str, password: str) -> None:
    """register_user
    """
    resp = requests.post('http://127.0.0.1:5000/users',
                         data={'email': email, 'password': password})
    if resp.status_code == 200:
        assert (resp.json() == {"email": email, "message": "user created"})
    else:
        assert(resp.status_code == 400)
        assert (resp.json() == {"message": "email already registered"})


def log_in_wrong_password(email: str, password: str) -> None:
    """_summary_

    Args:
        email (str): _description_
        password (str): _description_
    """
    payload = {'email': email, 'password': password}
    x = requests.post('http://localhost:5000/sessions', data=payload)
    assert x.status_code == 401


def profile_unlogged() -> None:
    """_summary_
    """
    x = requests.get('http://localhost:5000/profile')
    assert x.status_code == 403


def log_in(email: str, password: str) -> str:
    """_summary_

    Args:
        email (str): _description_
        password (str): _description_

    Returns:
        str: _description_
    """
    payload = {'email': email, 'password': password}
    x = requests.post('http://localhost:5000/sessions', data=payload)
    assert x.status_code == 200
    assert x.json() == {'email': email, 'message': 'logged in'}
    return x.cookies.get('session_id')


def profile_logged(session_id: str) -> None:
    """_summary_

    Args:
        session_id (str): _description_
    """
    cookies = {'session_id': session_id}
    x = requests.get('http://localhost:5000/profile', cookies=cookies)
    assert x.status_code == 200


def log_out(session_id: str) -> None:
    """_summary_

    Args:
        session_id (str): _description_
    """
    cookies = {'session_id': session_id}
    x = requests.delete('http://localhost:5000/sessions', cookies=cookies)

    if x.status_code == 302:
        assert x.url == 'http://localhost:5000/'
    assert x.status_code == 200


def reset_password_token(email: str) -> str:
    """_summary_

    Args:
        email (str): _description_

    Returns:
        str: _description_
    """
    payload = {'email': email}
    x = requests.post('http://localhost:5000/reset_password', data=payload)
    assert x.status_code == 200
    return x.json().get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """_summary_

    Args:
        email (str): _description_
        reset_token (str): _description_
        new_password (str): _description_
    """
    payload = {'email': email, 'reset_token': reset_token,
               'new_password': new_password}
    x = requests.put('http://localhost:5000/reset_password', data=payload)
    assert x.status_code == 200
    assert x.json() == {'email': email, 'message': 'Password updated'}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
