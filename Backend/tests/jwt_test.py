
from app.config import supabase
from app.utils.supabase_jwt import get_user_id_from_jwt

def main():
    res = supabase.auth.sign_in_with_password({
    "email": "test3@m.com",
    "password": "123"
})

    token = res.session.access_token
    print(token)
    # Get user ID
    user_id = get_user_id_from_jwt(token)


if __name__ == "__main__":
    main()


