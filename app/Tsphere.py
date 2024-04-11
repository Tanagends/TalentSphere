from app import create_app, db
from app.models.basemodel import BaseModel, Role
from app.models.academy import Academy
from app.models.club import Club
from app.models.scout import Scout
from app.models.sponsor import Sponsor
from app.models.video import Video
from app.models.player import Player
from app.create_role import create_roles

app = create_app()

with app.app_context():
    create_roles()