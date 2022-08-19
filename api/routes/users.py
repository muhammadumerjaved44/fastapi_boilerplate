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
from db.session import get_db
import auth
from models import User, Campaign, Contact
from schemas import (
    UserSchema,
    Users,
    CreateUserIn,
    CreateUserOut,
    UpdateUserIn,
    UpdateUserOut,
    DeleteUserOut,
    Contacts,
    GetCampaignOut,
    BroadcastMessageOut,
    BroadcastMessageIn,
)
from auth import get_current_active_user, get_password_hash
from background_tasks import broadcast_emails
from bs4 import BeautifulSoup
from sqlalchemy import inspect
from crud import user_crud, campaign_crud


router = APIRouter()


@router.get("/{id}", response_model=UserSchema)
def get_user_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Security(get_current_active_user, scopes=["superuser"]),
):
    """get user by id
    Args:
        id (user's id): int

    Raises:
        HTTPException: 404, user not found

    Returns:
        UserSchema: instance of user
    """
    user = user_crud.get(id=id, db=db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    response: UserSchema = user
    return response


@router.get(
    "/",
    response_model=Users,
)
def get_all_users(
    db: Session = Depends(get_db),
    current_user: User = Security(get_current_active_user, scopes=["superuser"]),
):
    """get all users list

    Args:
        None

    Returns:
        Users: all users list
    """
    users = user_crud.get_all(db=db)
    response: Users = Users(users=users)
    return response


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CreateUserOut)
def create_user(
    user: CreateUserIn,
    db: Session = Depends(get_db),
    current_user: User = Security(get_current_active_user, scopes=["superuser"]),
):
    """create new user

    Args:
        email: str
        password: str
        first_name: str
        last_name: str
        scope: str
        is_active: bool

    Raises:
        HTTPException: 400, Email Already exists

    Returns:
        CreateUserOut: response message for successfully creating user
    """
    user = user_crud.create(user_in=user, db=db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email Already exists"
        )

    response: CreateUserOut = CreateUserOut(message="User Created Successfully")
    return response


@router.put("/{id}", response_model=UpdateUserOut)
def update_user(
    id: int,
    user: UpdateUserIn,
    db: Session = Depends(get_db),
    current_user: User = Security(get_current_active_user, scopes=["superuser"]),
):
    """update user by id

    Args:
        id (id for updating user): int

    Raises:
        HTTPException: 404, user not found

    Returns:
        UpdateUserOut: response message for updating user
    """
    user = user_crud.update(id=id, user_in=user, db=db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    response: UpdateUserOut = UpdateUserOut(message="user updated")
    return response


@router.delete("/{id}", response_model=DeleteUserOut)
def delete_user(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Security(get_current_active_user, scopes=["superuser"]),
):
    """delete user

    Args:
        id (int): id for deleting user

    Raises:
        HTTPException: 404, user not found

    Returns:
        DeleteUserOut: return deleted user name + deleted message
    """
    user_id = user_crud.delete(id=id, db=db)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    response: DeleteUserOut = DeleteUserOut(message=f"user with id: {user_id} deleted")
    return response


@router.get("/me/contacts", response_model=Contacts)
def get_current_user_contacts(
    current_user: User = Security(get_current_active_user, scopes=["user"]),
):
    """Get contacts of current user

    Args:
        None

    Returns:
        Contacts: list of contacts
    """

    response: Contacts = Contacts(contacts=current_user.contacts)
    return response


@router.get("/me/campaigns", response_model=GetCampaignOut)
def get_current_user_campaigns(
    current_user: User = Security(auth.get_current_active_user, scopes=["user"]),
):
    """Get campaigns of current user

    Args:
        None

    Returns:
        Campaigns: list of campaigns
    """

    response: GetCampaignOut = GetCampaignOut(campaigns=current_user.campaigns)
    return response


@router.post("/broadcast-message", response_model=BroadcastMessageOut)
def broadcast_message(
    message_details: BroadcastMessageIn,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Security(auth.get_current_active_user, scopes=["user"]),
):
    """Broadcast message via email and/or sms

    Args:
        is_sms (bool): should it send message through SMS/MMS
        is_email (bool): should it send message through Email
        subject (string): Subject of the Email
        message (string): Message contect with tags
        emails (list of strings): list of email addresses of recipients (if any email is not in user's contacts table then message will not be broadcasted to that contact)

    Raises:
        HTTPException: 400 if both of the "is_sms" or "is_email" fields are false

    Returns:
        BroadcastMessageOut: success message
    """

    # one of the fields should be true
    if not (message_details.is_email or message_details.is_sms):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='One of the fields "is_sms" or "is_email" should be true.',
        )

    # checking unknown tags in message
    soup = BeautifulSoup(message_details.message, "html.parser")
    tag_spans = soup.select('span[class="mention"]')
    tag_texts = [tag_span.text.replace("@", "") for tag_span in tag_spans]
    db_tags = inspect(Contact).columns.keys()
    tags_present_in_db = all(tag in db_tags for tag in tag_texts)

    # raise Bad Request if unknown tag present in message
    if not tags_present_in_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="One/some of provided tag(s) in the message are not present in the database.",
        )

    if message_details.is_email:
        # broadcasting emails through background tasks
        background_tasks.add_task(
            broadcast_emails,
            emails=message_details.emails,
            message=message_details.message,
            subject=message_details.subject,
            user_id=current_user.id,
        )

    # creating new campaign record
    campaign = campaign_crud.create(
        via_sms=message_details.is_sms,
        via_email=message_details.is_email,
        message=message_details.message,
        audience_number=len(message_details.emails),
        user_id=current_user.id,
        db=db,
    )

    response: BroadcastMessageOut = BroadcastMessageOut(
        message="Email broadcasting added in queue"
    )
    return response
