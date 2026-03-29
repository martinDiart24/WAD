from sqlalchemy.orm import Session

from ..models import CarModel, Engine, Part


def find_parts_for_engine(session: Session, query: str):
    """
    Very simple search helper.
    - if query looks like engine code, search engines and return parts
    - otherwise search by part name / OEM code
    """
    q = query.strip()

    engine = (
        session.query(Engine)
        .filter(Engine.code.ilike(f"%{q}%"))
        .first()
    )

    if engine:
        return [
            {
                "engine": engine,
                "part": compat.part,
                "compatibility": compat,
            }
            for compat in engine.engine_parts
        ]

    parts = (
        session.query(Part)
        .filter(
            (Part.name.ilike(f"%{q}%"))
            | (Part.oem_code.ilike(f"%{q}%"))
        )
        .limit(50)
        .all()
    )

    return [{"engine": None, "part": part, "compatibility": None} for part in parts]

