import os
from dotenv import load_dotenv
from peewee import PostgresqlDatabase, Model, CharField, IntegerField, FloatField, TextField, ForeignKeyField

load_dotenv()

db_name = os.getenv("POSTGRES_DB")
db_user = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")
db_host = os.getenv("POSTGRES_HOST")
db_port = os.getenv("POSTGRES_PORT")

db = PostgresqlDatabase(
    db_name,
    user=db_user,
    password=db_password,
    host=db_host,
    port=db_port,
)


class BaseModel(Model):
    class Meta:
        database = db


class Profile(BaseModel):
    username = CharField(unique=True, max_length=512)
    full_name = CharField(null=True, max_length=512)
    profile_pic_url = CharField(null=True, max_length=512)
    bio = TextField(null=True)
    external_url = CharField(null=True, max_length=512)
    followers = IntegerField(default=0)
    following = IntegerField(default=0)
    posts = IntegerField(default=0)


class Assessment(BaseModel):
    profile = ForeignKeyField(Profile, backref="assessments")
    activity_recency_score = FloatField(default=0.0)
    followers_authenticity_score = FloatField(default=0.0)
    profile_picture_authenticity = FloatField(default=0.0)
    bio_extraction_completeness = FloatField(default=0.0)
    product_extraction_completeness = FloatField(default=0.0)
    products_count = IntegerField(default=0)
    products_to_other_posts_ratio = FloatField(default=0.0)


class Product(BaseModel):
    profile = ForeignKeyField(Profile, backref="products")
    name = TextField()
    description = TextField(null=True)
    price = CharField(null=True, max_length=20)


def create_tables():
    with db:
        db.create_tables([Profile, Assessment, Product])
