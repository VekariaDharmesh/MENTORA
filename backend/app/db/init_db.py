from sqlalchemy.orm import Session
from app.db.models import Base, Concept, User, StudentProfile
from app.db.session import engine, SessionLocal

def init_db(db: Session) -> None:
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Create dummy user and student profile for demo if not exists
    user = db.query(User).filter(User.email == "student@mentora.ai").first()
    if not user:
        user = User(email="student@mentora.ai", is_guest=False)
        db.add(user)
        db.commit()
        db.refresh(user)
        
        profile = StudentProfile(
            user_id=user.id,
            display_name="Demo Student",
            learning_level="beginner",
            default_language="English"
        )
        db.add(profile)
        db.commit()

    # Seed Physics Concepts
    concepts_data = [
        ('electric_charge', 'Electric Charge', 'Physics', 'beginner', "Coulomb's Law, fundamental charge carriers, positive and negative charges."),
        ('electric_current', 'Electric Current', 'Physics', 'beginner', 'Rate of charge flow over time (I = Q / t). Measured in Amperes.'),
        ('voltage', 'Voltage & Potential Difference', 'Physics', 'beginner', 'Work done per unit charge (ΔV = W / Q). Electric driving pressure.'),
        ('resistance', 'Resistance & Impedance', 'Physics', 'intermediate', 'Opposition to current flow caused by atomic collisions. Measured in Ohms (Ω).'),
        ('ohms_law', "Ohm's Law", 'Physics', 'intermediate', 'Fundamental relationship V = I * R linking voltage, current, and resistance.'),
        ('circuit_analysis', "Circuit Analysis & Kirchhoff's Laws", 'Physics', 'advanced', 'Series and parallel topologies, current division, loop conservation.')
    ]
    
    for key, name, domain, difficulty, desc in concepts_data:
        concept = db.query(Concept).filter(Concept.key == key).first()
        if not concept:
            concept = Concept(
                key=key,
                name=name,
                domain=domain,
                description=desc,
                difficulty_level=difficulty
            )
            db.add(concept)
    
    db.commit()

if __name__ == "__main__":
    db = SessionLocal()
    init_db(db)
    print("Database initialized successfully.")
    db.close()
