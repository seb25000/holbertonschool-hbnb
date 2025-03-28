from app.models.base_model import BaseModel


class User(BaseModel):
    """
    User class that defines the users, with name, last name, email and role.
    """
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin


    def validate(self):
        if not self.first_name or len(self.first_name) > 50:
            raise ValueError("First name is required and must be 50 characters or less")
        if not self.last_name or len(self.last_name) > 50:
            raise ValueError("Last name is required and must be 50 characters or less")
        if not self.email or '@' not in self.email:
            raise ValueError("Valid email is required")


    @staticmethod
    def is_valid_email(email):
        """Basic email validation"""
        return "@" in email and "." in email


    def update(self, data):
        super().update(data)
        self.validate()


        def __repr__(self):
            return (f"User (id='{self.id}', first_name='{self.first_name}', "
                    f"last_name='{self.last_name}', email='{self.email}', "
                    f"is_admin{self.is_admin})")