from fastapi import (
    HTTPException,
    Depends,
    APIRouter,
    status,
    HTTPException,
    Security,
    BackgroundTasks,
)
from sqlalchemy.orm import Session
import sqlalchemy
from db.session import get_db
import auth
from models import User, Campaign
from schemas import (
    UserSchema,
    Users,
    AddUser,
    UserUpdateSchema,
    Contacts,
    GetCampaignOut,
    BroadcastMessageOut,
    BroadcastMessageIn,
)
from auth import get_current_active_user, get_password_hash
from background_tasks import broadcast_emails

router = APIRouter()


@router.get("/{id}", response_model=UserSchema)
def userById(
    id: int,
    session: Session = Depends(get_db),
    current_user: User = Security(get_current_active_user, scopes=["superuser"]),
):
    """ "
        get user by id
    Args:
        id (int): user_id
        session (Session, optional): database connection

    Raises:
        HTTPException: 404, user not found

    Returns:
        _type_: instant user by id
    """
    user = session.query(User).get(id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    response: UserSchema = user
    return response


@router.get(
    "/",
    response_model=Users,
)
def userList(
    session: Session = Depends(get_db),
    current_user: User = Security(get_current_active_user, scopes=["superuser"]),
):
    """get all users list

    Args:
        session (Session, optional): database connection

    Returns:
        _type_: all users list
    """
    users = session.query(User).all()
    response: Users = Users(users=users)
    return response


@router.post("/", status_code=status.HTTP_201_CREATED)
def addUser(
    user: AddUser,
    session: Session = Depends(get_db),
    current_user: User = Security(get_current_active_user, scopes=["superuser"]),
):
    """for adding new user

    Args:
        user (AddUser): user schema
        session (Session, optional):  database connection
        current_user (User, optional): for authentication and authorization

    Raises:
        HTTPException: 400, Email Already exists

    Returns:
        _type_: pass successful created string
    """
    try:
        password = get_password_hash(user.password)
        user.password = password
        userObj = User(**user.dict())
        session.add(userObj)
        session.commit()
        session.refresh(userObj)
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=400, detail="Email Already exists")
    return "User Created Successfully"


@router.put("/{id}")
def updateUser(
    id: int,
    user: UserUpdateSchema,
    session: Session = Depends(get_db),
    current_user: User = Security(get_current_active_user, scopes=["superuser"]),
):
    """update

    Args:
        id (int): take id for updating user
        session (Session, optional): database connection

    Raises:
        HTTPException: 404, user not found

    Returns:
        _type_: send response for updating user
    """
    userObj = session.query(User).get(id)
    if userObj is None:
        raise HTTPException(status_code=404, detail="User not found")
    userObj.first_name = user.first_name
    userObj.last_name = user.last_name
    session.commit()
    return {"msg": "user updated"}


@router.delete("/{id}")
def deleteUser(
    id: int,
    session: Session = Depends(get_db),
    current_user: User = Security(get_current_active_user, scopes=["superuser"]),
):
    """delete user

    Args:
        id (int): id for deleting user
        session (Session, optional): database connection

    Raises:
        HTTPException: 404, user not found

    Returns:
        _type_: return deleted user name + deleted message
    """
    userObj = session.query(User).get(id)
    if userObj is None:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(userObj)
    session.commit()
    session.close
    return userObj.first_name + "  deleted"


@router.get("/me/contacts", response_model=Contacts)
def get_current_user_contacts(
    current_user: User = Security(get_current_active_user, scopes=["user"]),
):

    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    response: Contacts = Contacts(contacts=current_user.contacts)
    return response


@router.get("/me/campaigns", response_model=GetCampaignOut)
def get_current_user_campaigns(
    current_user: User = Security(auth.get_current_active_user, scopes=["user"]),
):

    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    response: GetCampaignOut = GetCampaignOut(campaigns=current_user.campaigns)
    return response


@router.post("/broadcast-message", response_model=BroadcastMessageOut)
def broadcast_message(
    message_details: BroadcastMessageIn,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Security(auth.get_current_active_user, scopes=["user"]),
):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    # one of the fields should be true
    if not (message_details.is_email or message_details.is_sms):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='One of the fields "is_sms" or "is_email" should be true.',
        )

    if message_details.is_email:
        # broadcasting emails through background tasks
        background_tasks.add_task(
            broadcast_emails,
            emails=message_details.emails,
            message=message_details.message,
            subject=message_details.subject,
        )

    # creating new campaign record
    campaign = Campaign(
        via_sms=message_details.is_sms,
        via_email=message_details.is_email,
        audience_number=len(message_details.emails),
        user_id=current_user.id,
    )
    db.add(campaign)
    db.commit()

    response: BroadcastMessageOut = BroadcastMessageOut(
        message="Email broadcasting added in queue"
    )
    return response
