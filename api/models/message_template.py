from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.sql.schema import Column
from db.session import Base


class MessageTemplate(Base):
    """This model has message template details and is parent of MessageTemplateDefault and MessageTemplateCustom"""

    __tablename__ = "message_template"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String(100), nullable=False)
    message = Column(String(1000), nullable=False)
    template_type = Column(String(100), nullable=False)
    __mapper_args__ = {
        "polymorphic_identity": "message_template",
        "polymorphic_on": template_type,
    }


class DefaultMessageTemplate(MessageTemplate):
    """This model has default message template details and is child model class of MessageTemplate"""

    __tablename__ = "default_message_template"

    id = Column(Integer, ForeignKey("message_template.id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "default_message_template",
    }


class CustomMessageTemplate(MessageTemplate):
    """This model has user's custom message template details and is child model class of MessageTemplate"""

    __tablename__ = "custom_message_template"

    id = Column(Integer, ForeignKey("message_template.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "custom_message_template",
    }
