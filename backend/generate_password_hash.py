from passlib.context import CryptContext
import sys

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generate_hash(password: str):
    return pwd_context.hash(password)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python generate_password_hash.py <password>")
        sys.exit(1)
    password = sys.argv[1]
    hash = generate_hash(password)
    print(f"Hashed password: {hash}") 