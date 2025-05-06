from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Interger, String, ForeignKey, Date, Enum
from sqlalchemy import Index, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from sqlalchemy.orm import relationship
from utils.configuration import Configuration


Base = declarative_base()

class UserSchema(Base):
    __tablename__ = "user"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(256), nullable=False, default='rabbit001')

    __table_args__ = (
        Index('ix_name', 'name')
    )

class ConversationSchema(Base):
    __tablename__ = "conversation"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = Column(String(256), nullable=False, default='conversation001')
    counter_chunk = Column(Interger, nullable=False, default=0)
    created_date = Column(Date, nullable=False)
    updated_date = Column(Date, nullable=False)
    created_user_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=False)

    __table_args = (
        CheckConstraint('counter_chunk > 0', name = 'check_counter_chunk_positive'),
        Index("ix_title", 'title')
    )
    user = relationship(UserSchema)

class AttendeeSchema(Base):
    __tablename__ = 'attendee'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey('conversation.id'), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=False)
    created_date = Column(Date, nullable=False)
    updated_date = Column(Date, nullable=False)
    nickname = Column(String(256), nullable=False, default='attendee0001') #, unique=True)
    conversation = relationship(ConversationSchema)

    user = relationship(UserSchema)

    __table_args__ = (
        Index('ix_nickname', 'nickname'),
    )


class DocumentMetadataSchema(Base):
    __tablename__ = 'document_metadata'

    #columns
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    file_name = Column(String(256), nullable=False, default="homework.txt")
    created_date = Column(Date, nullable=False)
    type = Column(Enum('pdf', 'txt', 'doc', 'png', name='file_type'), nullable=False)
    size = Column(Interger, nullable=False, default=0)
    object_id = Column(UUID(as_uuid=True), nullable=False)
    role_permissions= Column(String(1024), default='User')
    created_user_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=False)
    message_id = Column(UUID(as_uuid=True), nullable=False)

    #constraints: Index, Check,...
    __table_args__ = (
        CheckConstraint('size > 0', name='check_size_col_positive'),
        Index('ix_file_name', 'file_name')
    )

class MessageChunkSchema(Base):
    __tablename__ = 'message_chunk'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_date = Column(Date, nullable=False)
    no_of_chunk = Column(Interger,nullable=False, default=0)
    length = Column(Interger, nullable=False, default=0)
    conversation_id = Column(UUID(as_uuid=True),ForeignKey('conversation.id'), nullable=False)

    #relationship
    conversation = relationship(ConversationSchema)

    __table_args__ = (
        CheckConstraint('no_of_chunk > 0', name='check_no_of_chunk_positive')
    )


conn_string = Configuration.load('database_connections:postgresql:default')

engine = create_engine(conn_string)

Base.metadata.create_all(engine)



