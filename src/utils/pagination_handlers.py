from typing import List

from errors import InvalidPagination

from constants import MAX_PAGINATION_SIZE


def parse_str_page_with_validation(page: str) -> int:
    page = page if page else "1"
    try:
        page = int(page)
    except Exception:
        raise InvalidPagination()

    return page


def parse_str_page_size_with_validation(page_size: str) -> int:
    page_size = page_size if page_size else MAX_PAGINATION_SIZE
    try:
        page_size = int(page_size)
    except Exception:
        raise InvalidPagination()

    if page_size > MAX_PAGINATION_SIZE:
        raise InvalidPagination()

    return page_size


def format_response_with_pagination(data: List[dict], page: int, page_size: int) -> dict:
    return {"data": data, "pagination": {"current_page": page, "rows_per_page": page_size}}
