from dataclasses import dataclass


@dataclass
class ErrorMsg:
    """Класс сообщений об ошибках."""

    not_found: str = 'Not found'
    bad_request: str = 'Bad request: errors in parameters'

    film_not_exist: str = 'Film not exist or not results'
    film_not_found: str = 'Film not found'

    genre_not_found: str = 'Genre not found'

    person_not_found: str = 'Person not found'

    non_valid_token: str = 'Token not valid'
    non_fresh_token: str = 'Token was expired'
    authorized_only: str = 'Only authorized users'
    subscription_only: str = 'Subscription only'


error_msgs = ErrorMsg()
