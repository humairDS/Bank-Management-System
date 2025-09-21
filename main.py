# Bank Management System

from datetime import datetime
from typing import List

#Class 1: 
class InsufficientFundError(Exception):
    def __init__(self,balance,requested_amount):
        self.balance = balance
        self.requested_amount = requested_amount
        super().__init__(f"Insufficient Funds, Balance:${self.balance}, Requested Amount:${self.requested_amount}")

class InvalidAmountError(Exception):
    def __init__(self,amount):
        self.amount = amount
        super().__init__(f"Invalid Amount: ${self.amount}, Amount Must Be Postive")

class Transaction:
    def __init__(self,transaction_type,amount,balance_after):
        self.transaction_type = transaction_type
        self.amount = amount
        self.balance_after = balance_after
        self.timestamp = datetime.now()

    def __str__(self):
        return (f"{self.timestamp.strftime('%Y-%m-%D,%H-%M-%S')}|"
        f"{self.transaction_type.upper()}: ${self.amount}|"
        f"Balance: ${self.balance_after}")

class Account:

    def __init__(self,account_number,initial_balance = 0):
        self.account_number = account_number

        self._balance = initial_balance
        self._transaction_history = []

        if initial_balance > 0:
            self._transaction_history.append(
                Transaction("initial deposit",initial_balance,initial_balance)
            )
    @property
    def balance(self):
        return self._balance
    
    def deposit(self,amount):
        if amount < 0:
            raise InvalidAmountError(amount)
        
        self._balance += amount

        transaction = Transaction("deposit",amount,self._balance)
        self._transaction_history.append(transaction)
        print(f"Depsosit:${amount}, New Balance:${self._balance}")
        return self._balance
    
    def withdraw(self,amount):

        if amount < 0:
            raise InvalidAmountError
        
        if amount > self._balance:
            raise InsufficientFundError(self._balance,amount)
        
        self._balance -= amount

        transaction = Transaction("withdraw", amount, self._balance)
        self._transaction_history.append(transaction)
        
        print(f"Withdrew ${amount}. New balance: ${self._balance}")
        return self._balance
        
    def get_transaction_history(self):
        return self._transaction_history.copy()
    
    def display_transaction_history(self):
        """Display all transactions in a nice format"""
        print(f"\n Transaction History for Account #{self.account_number}")
        print("-" * 60)
        
        if not self._transaction_history:
            print("No transactions yet.")
            return
        
        for transaction in self._transaction_history:
            print(transaction)
        print("-" * 60)

class Customer:
    """Represents a bank customer"""
    
    def __init__(self, customer_id, name, email, phone):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.phone = phone
        self.accounts = []  # List to store multiple accounts
    
    def add_account(self, account):
        """Link an account to this customer"""
        self.accounts.append(account)
    
    def get_accounts(self):
        """Get all accounts for this customer"""
        return self.accounts
    
    def __str__(self):
        """How to display customer info"""
        return (f"Customer: {self.name} (ID: {self.customer_id})\n"
                f"Email: {self.email} | Phone: {self.phone}\n"
                f"Number of accounts: {len(self.accounts)}")
    
def demo_bank_system():
    """Demonstrate how the bank system works"""
    
    print("Welcome to Python Bank Management System!")
    print("=" * 50)
    
    try:
        # Create a customer
        customer = Customer(
            customer_id="CUST001",
            name="Alice Johnson",
            email="alice@email.com",
            phone="555-0123"
        )
        
        # Create an account with initial balance
        account = Account("ACC001", 1000)  # Start with $1000
        
        # Link account to customer
        customer.add_account(account)
        
        print(f"Created account for: {customer.name}")
        print(f"Initial balance: ${account.balance}")
        print()
        
        # Demonstrate deposit
        print("Making a deposit...")
        account.deposit(500)
        print()
        
        # Demonstrate withdrawal
        print("Making a withdrawal...")
        account.withdraw(200)
        print()
        
        # Check balance (using encapsulated property)
        print(f"Current balance: ${account.balance}")
        print()
        
        # Show transaction history
        account.display_transaction_history()
        print()
        
        # Demonstrate custom exception - insufficient funds
        print("Trying to withdraw more than balance..")
        try:
            account.withdraw(2000)  # This will fail
        except InsufficientFundError as e:
            print(f"Error caught: {e}")
        print()
        
        # Demonstrate custom exception - invalid amount
        print("Trying to deposit negative amount..")
        try:
            account.deposit(-100)  # This will fail
        except InvalidAmountError as e:
            print(f"Error caught: {e}")
            
    except Exception as e:
        print(f"An error occurred: {e}")

# Run the demo
if __name__ == "__main__":
    demo_bank_system()