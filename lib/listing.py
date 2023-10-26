class Listing():
   
    def __init__(self, id, title, description, price, owner_id):
        self.id = id
        self.owner_id = owner_id  # foreign key to user_id
        self.title = title
        self.description = description
        self.price = price


    def __eq__(self, other):
        if not isinstance(other, Listing):
            return False
        return self.__dict__ == other.__dict__

    def format(self):
        return f'ID: {self.id}, Owner_ID: {self.owner_id}, Title: {self.title}, Description: {self.description}, Price: £{self.price}'


    
