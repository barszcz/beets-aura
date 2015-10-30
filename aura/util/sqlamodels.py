# coding: utf-8
from sqlalchemy import Column, Float, Integer, LargeBinary, Text, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class AlbumAttribute(Base):
    __tablename__ = 'album_attributes'
    __table_args__ = (
        UniqueConstraint('entity_id', 'key'),
    )

    id = Column(Integer, primary_key=True)
    entity_id = Column(Integer, index=True)
    key = Column(Text)
    value = Column(Text)


class Album(Base):
    __tablename__ = 'albums'

    disctotal = Column(Integer)
    albumstatus = Column(Text)
    month = Column(Integer)
    original_day = Column(Integer)
    albumartist = Column(Text)
    year = Column(Integer)
    albumdisambig = Column(Text)
    albumartist_sort = Column(Text)
    id = Column(Integer, primary_key=True)
    album = Column(Text)
    asin = Column(Text)
    script = Column(Text)
    mb_albumid = Column(Text)
    label = Column(Text)
    rg_album_gain = Column(Float)
    mb_releasegroupid = Column(Text)
    artpath = Column(LargeBinary)
    rg_album_peak = Column(Float)
    albumartist_credit = Column(Text)
    catalognum = Column(Text)
    added = Column(Float)
    original_month = Column(Integer)
    comp = Column(Integer)
    genre = Column(Text)
    day = Column(Integer)
    original_year = Column(Integer)
    language = Column(Text)
    mb_albumartistid = Column(Text)
    country = Column(Text)
    albumtype = Column(Text)


class ItemAttribute(Base):
    __tablename__ = 'item_attributes'
    __table_args__ = (
        UniqueConstraint('entity_id', 'key'),
    )

    id = Column(Integer, primary_key=True)
    entity_id = Column(Integer, index=True)
    key = Column(Text)
    value = Column(Text)


class Item(Base):
    __tablename__ = 'items'

    lyrics = Column(Text)
    disctitle = Column(Text)
    month = Column(Integer)
    channels = Column(Integer)
    disc = Column(Integer)
    mb_trackid = Column(Text)
    composer = Column(Text)
    albumartist_sort = Column(Text)
    bitdepth = Column(Integer)
    title = Column(Text)
    mb_albumid = Column(Text)
    acoustid_fingerprint = Column(Text)
    rg_album_gain = Column(Float)
    mb_releasegroupid = Column(Text)
    rg_album_peak = Column(Float)
    albumartist_credit = Column(Text)
    acoustid_id = Column(Text)
    format = Column(Text)
    encoder = Column(Text)
    rg_track_gain = Column(Float)
    day = Column(Integer)
    original_year = Column(Integer)
    artist = Column(Text)
    mb_albumartistid = Column(Text)
    bpm = Column(Integer)
    artist_credit = Column(Text)
    grouping = Column(Text)
    disctotal = Column(Integer)
    album_id = Column(Integer)
    albumstatus = Column(Text)
    mtime = Column(Float)
    original_day = Column(Integer)
    albumartist = Column(Text)
    year = Column(Integer)
    albumdisambig = Column(Text)
    samplerate = Column(Integer)
    id = Column(Integer, primary_key=True)
    album = Column(Text)
    mb_artistid = Column(Text)
    media = Column(Text)
    artist_sort = Column(Text)
    comments = Column(Text)
    tracktotal = Column(Integer)
    rg_track_peak = Column(Float)
    catalognum = Column(Text)
    added = Column(Float)
    original_month = Column(Integer)
    asin = Column(Text)
    track = Column(Integer)
    comp = Column(Integer)
    initial_key = Column(Text)
    genre = Column(Text)
    path = Column(LargeBinary)
    bitrate = Column(Integer)
    language = Column(Text)
    country = Column(Text)
    script = Column(Text)
    label = Column(Text)
    length = Column(Float)
    albumtype = Column(Text)
