# -*- coding: utf-8 -*-

from dildeolupbiten import db
from sqlalchemy.dialects.postgresql import JSONB


class ItalianVerbModel(db.Model):
    __tablename__ = "italian_verbs"
    id = db.Column(db.Integer, primary_key=True)
    verb = db.Column(JSONB, nullable=False)

    def __init__(self, verb):
        self.verb = verb

    def __repr__(self):
        return self.verb['verb']
