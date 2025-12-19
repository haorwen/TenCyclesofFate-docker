from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, HTTPException, status, Cookie, Header, Request
from jose import JWTError, jwt
import urllib.parse
from passlib.context import CryptContext
from authlib.integrations.starlette_client import OAuth

from .config import settings

# --- Setup ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") # No longer needed for cookie-based auth

# --- OAuth Client ---
oauth = OAuth()
oauth.register(
    name="linuxdo",
    client_id=settings.LINUXDO_CLIENT_ID,
    client_secret=settings.LINUXDO_CLIENT_SECRET,
    access_token_url=settings.LINUXDO_TOKEN_URL,
    authorize_url=settings.LINUXDO_AUTHORIZE_URL,
    api_base_url=settings.LINUXDO_API_BASE_URL,
    client_kwargs={"scope": settings.LINUXDO_SCOPE},
)

# --- Models ---
class TokenData(object):
    username: str | None = None
    trust_level: int | None = 0

# --- Core Functions ---
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    """Decodes the access token and returns the payload."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        raise credentials_exception

# --- FastAPI Dependencies ---
async def get_current_user(
    request: Request = None,
    token: Annotated[str | None, Cookie()] = None,
    guest_name_cookie: Annotated[str | None, Cookie(alias="guest_name")] = None,
    x_guest_username_header: Annotated[str | None, Header(alias="X-Guest-Username")] = None
):
    """
    Decodes JWT from cookie and returns user info.
    If Linux.do login is disabled, it uses the guest username from header or cookie.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # If Linux.do login is disabled, we prioritize guest identity from headers or cookies
    if not settings.ENABLE_LINUXDO_LOGIN:
        # Check header (from dependency or manual request check)
        x_guest_username = x_guest_username_header
        if not x_guest_username and request:
            # works for both Request and WebSocket objects
            x_guest_username = request.headers.get("X-Guest-Username")
        
        # Check cookies from request if the specific cookie dependency didn't pick it up (e.g. manual call)
        guest_name = guest_name_cookie
        if not guest_name and request:
            guest_name = request.cookies.get("guest_name")

        raw_username = x_guest_username or guest_name
        if raw_username:
            try:
                username = urllib.parse.unquote(raw_username)
            except Exception:
                username = raw_username

            return {
                "username": f"guest_{username}",
                "trust_level": 1,
                "id": 0,
                "name": username,
            }

    if token is None:
        raise credentials_exception

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
        
        # The JWT payload contains the user info from OAuth
        user = {
            "username": username,
            "trust_level": payload.get("trust_level", 0),
            "id": payload.get("id"),
            "name": payload.get("name"),
        }
    except JWTError:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[dict, Depends(get_current_user)]
):
    # In a real app, you might check if the user is active
    return current_user