from dataclasses import dataclass


@dataclass
class ErrorMsg:
    """Класс сообщений об ошибках."""

    not_found: str = 'Not found'
    film_not_exist: str = 'Film not exist or not results'
    film_not_found: str = 'Film not found'


error_msgs = ErrorMsg()
