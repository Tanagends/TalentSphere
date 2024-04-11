from app import db
from app.models.basemodel import Role


def create_roles():
    roles_data = [
        {'name': 'player', 'description': 'Registered player'},
        {'name': 'scout', 'description': 'Registered scout'},
        {'name': 'sponsor', 'description': 'Registered sponsor'},
        {'name': 'club', 'description': 'Registered club'},
        {'name': 'academy', 'description': 'Registered academy'}
    ]
    
    for role_data in roles_data:
        role = Role.query.filter_by(name=role_data['name']).first()
        if not role:
            role = Role(**role_data)
            db.session.add(role)
    
    db.session.commit()


if __name__ == '__main__':
    create_roles()