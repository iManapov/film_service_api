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


error_msgs = ErrorMsg()
