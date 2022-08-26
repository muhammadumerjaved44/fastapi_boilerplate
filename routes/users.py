from fastapi import HTTPException, Depends, APIRouter, status, HTTPException, Security
from sqlalchemy.orm import Session
from db.session import get_db
from models import User
from schemas import UserSchema, Users, AddUser, UserUpdateSchema
from .auth import get_current_active_user, get_password_hash

router = APIRouter()


@router.get("/{id}", response_model=UserSchema)
def show(
    id: int,
    session: Session = Depends(get_db),
    current_user: User = Security(get_current_active_user, scopes=["superuser"]),
):
    """"
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
    "/", response_model=Users,
)
def users(
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
    response: UserSchema = users
    response: Users = Users(users=users)
    return response


@router.post("/", status_code=status.HTTP_201_CREATED)
def create(
    user: AddUser,
    session: Session = Depends(get_db),
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
        userObj = User(
                    email = user.username,
                    password = user.password,
                    first_name = user.first_name,
                    last_name = user.last_name,
                    is_active = user.is_active,
                    scope = user.scope,
                       )
        session.add(userObj)
        session.commit()
        session.refresh(userObj)
    except Exception:
        raise HTTPException(status_code=400, detail="Email Already exists")
    return "User Created Successfully"


@router.put("/{id}")
def update(
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
def delete(
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