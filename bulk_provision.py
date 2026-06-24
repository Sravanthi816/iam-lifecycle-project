import csv
from provision_user import get_access_token, create_user, provision_user

def main():
    token = get_access_token()

    with open("employees.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            print(f"--- Processing {row['email']} ---")
            user_id = create_user(token, row["first_name"], row["last_name"], row["email"])
            if user_id:
                provision_user(token, user_id, row["department"], row["title"])

if __name__ == "__main__":
    main()