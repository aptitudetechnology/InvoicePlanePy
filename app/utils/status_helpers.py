def get_status_id(db, status_enum):
    """Resolve QuoteStatus enum to quote_statuses.id"""
    from app.models.quote_status import QuoteStatusModel  # Avoid circular import
    status_obj = db.query(QuoteStatusModel).filter_by(name=status_enum.value).first()
    if not status_obj:
        raise ValueError(f"Status '{status_enum.value}' not found in quote_statuses table.")
    return status_obj.id
