# --- BULK SAVE ENDPOINT ---
@router.post("/api/save", response_class=JSONResponse)
async def bulk_save_tax_rates(
    payload: dict = Body(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Bulk save endpoint for tax rates. Accepts a list of tax rates and updates/inserts/deletes as needed.
    Expects JSON: { "tax_rates": [ {id, name, rate}, ... ] }
    """
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("tax_rates_bulk_save")
    logger.info(f"Bulk save called. Payload: {payload}")
    tax_rates_in = payload.get("tax_rates", [])
    if not isinstance(tax_rates_in, list):
        logger.error("tax_rates is not a list!")
        raise HTTPException(status_code=400, detail="tax_rates must be a list")

    # Fetch all existing tax rates from DB
    db_tax_rates = db.query(TaxRate).all()
    db_tax_rates_by_id = {tr.id: tr for tr in db_tax_rates}
    incoming_ids = set()

    # Update or create (by id or by name)
    for tr_in in tax_rates_in:
        tr_id = tr_in.get("id")
        name = tr_in.get("name", "").strip()
        rate = tr_in.get("rate")
        logger.info(f"Processing: id={tr_id}, name={name}, rate={rate}")
        if not name or rate is None or not (0 <= rate <= 100):
            logger.warning(f"Skipping invalid entry: {tr_in}")
            continue
        # Try to find by id first
        tr = db_tax_rates_by_id.get(tr_id) if tr_id else None
        if tr:
            logger.info(f"Updating by id: {tr_id}")
            tr.name = name
            tr.rate = rate
            db.add(tr)
            incoming_ids.add(tr.id)
        else:
            # Try to find by name
            existing_by_name = db.query(TaxRate).filter(TaxRate.name == name).first()
            if existing_by_name:
                logger.info(f"Updating by name: {name}")
                existing_by_name.rate = rate
                db.add(existing_by_name)
                incoming_ids.add(existing_by_name.id)
            else:
                logger.info(f"Creating new tax rate: {name}")
                new_tr = TaxRate(name=name, rate=rate)
                db.add(new_tr)
                db.flush()
                incoming_ids.add(new_tr.id)

    # Delete tax rates not present in incoming list
    for tr in db_tax_rates:
        if tr.id not in incoming_ids:
            logger.info(f"Deleting tax rate id={tr.id}, name={tr.name}")
            db.delete(tr)

    try:
        # Query and serialize final state BEFORE commit to avoid post-commit session issues
        final_tax_rates_query = db.query(TaxRate).all()
        final_tax_rates_data = [
            {'id': tr.id, 'name': tr.name, 'rate': tr.rate} 
            for tr in final_tax_rates_query
        ]
        
        # Now commit the transaction
        db.commit()
        
        logger.info("Bulk save committed successfully.")
        # Log final state using the pre-commit data
        logger.info(f"Final tax rates in DB: {final_tax_rates_data}")
        
        return {"message": "Tax rates saved successfully!"}
        
    except Exception as e:
        import traceback
        logger.exception("Bulk save failed with exception:")
        # Log session state
        logger.error(f"Session dirty: {db.dirty}")
        logger.error(f"Session new: {db.new}")
        logger.error(f"Session deleted: {db.deleted}")
        db.rollback()
        # Log state after rollback
        logger.error(f"Session dirty after rollback: {db.dirty}")
        logger.error(f"Session new after rollback: {db.new}")
        logger.error(f"Session deleted after rollback: {db.deleted}")
        # Query tax rates after rollback using a fresh query
        try:
            rolled_back_tax_rates = db.query(TaxRate).all()
            rolled_back_data = [
                {'id': tr.id, 'name': tr.name, 'rate': tr.rate} 
                for tr in rolled_back_tax_rates
            ]
            logger.error(f"Tax rates in DB after rollback: {rolled_back_data}")
        except Exception as inner_e:
            logger.error(f"Error querying tax rates after rollback: {inner_e}")
        tb_str = traceback.format_exc()
        raise HTTPException(status_code=500, detail=f"Bulk save failed: {type(e).__name__}: {e}\nTraceback:\n{tb_str}")