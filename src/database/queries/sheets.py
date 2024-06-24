from database.models.sheets import Sheet

from database.connection import session, session_decorator


@session_decorator
def get_sheets(user_id: int, sheet_id: int | None = None):
    sheets = session.query(Sheet).filter(Sheet.user_id == user_id)
    if sheet_id:
        return sheets.filter(Sheet.id == sheet_id).first()
    return sheets.all()


@session_decorator
def create_sheet(fields):
    sheet = Sheet(**fields)
    session.add(sheet)
    session.commit()
    return sheet


@session_decorator
def update_sheet(user_id: int, sheet_id, fields):
    sheet = session.query(Sheet).filter(Sheet.id == sheet_id, Sheet.user_id == user_id)
    sheet.update(fields)
    session.commit()
    return get_sheets(sheet_id)


@session_decorator
def delete_sheet(user_id, sheet_id):
    sheet = session.query(Sheet).filter(Sheet.id == sheet_id, Sheet.user_id == user_id)
    sheet.delete()
    session.commit()
