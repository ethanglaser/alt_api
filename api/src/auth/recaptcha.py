#!/usr/bin/env python3
"""
recaptcha login functions
"""

from utils.config import RECAPTCHA_SECRET
import requests

RECAPTCHA_URL: str = 'https://www.google.com/recaptcha/api/siteverify'


def verify_recaptcha(token: str) -> None:
    """
    verify recaptcha token
    """
    recaptcha_res = requests.get(RECAPTCHA_URL, params={
        'response': token,
        'secret': RECAPTCHA_SECRET
    })
    if recaptcha_res.status_code != 200:
        raise RuntimeError('invalid recaptcha token')
    json_data = recaptcha_res.json()
    if not json_data['success']:
        errors = ', '.join(json_data['error-codes'])
        raise RuntimeError(f'invalid recaptcha token: {errors}')
