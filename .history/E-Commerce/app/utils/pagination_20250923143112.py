from sqlalchemy.orm import Query, Session
from math import ceil

def paginate(query: Query, page: int = 1, size: int = 10):
    
    total = query.count()
    pages = ceil(total / size) if total > 0 else 1
    page = max(1, page)  # ensure page is >= 1

    items = query.offset((page - 1) * size).limit(size).all()

    return {
        "items": items,
        "total": total,
        "page": page,
        "size": size,
        "pages": pages,
        "next_page": page + 1 if page < pages else None,
        "prev_page": page - 1 if page > 1 else None,
    }