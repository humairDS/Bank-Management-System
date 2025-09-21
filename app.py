import streamlit as st
from datetime import datetime

# ---------------- Exceptions ----------------
class InsufficientFundError(Exception):
    def __init__(self, balance, requested_amount):
        super().__init__(f"Insufficient Funds, Balance:${balance}, Requested Amount:${requested_amount}")

class InvalidAmountError(Exception):
    def __init__(self, amount):
        super().__init__(f"Invalid Amount: ${amount}, Amount Must Be Positive")

# ---------------- Transaction ----------------
class Transaction:
    def __init__(self, transaction_type, amount, balance_after):
        self.transaction_type = transaction_type
        self.amount = amount
        self.balance_after = balance_after
        self.timestamp = datetime.now()

    def __str__(self):
        return (f"{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')} | "
                f"{self.transaction_type.upper()}: ${self.amount} | "
                f"Balance: ${self.balance_after}")

# ---------------- Account ----------------
class Account:
    def __init__(self, account_number, initial_balance=0):
        self.account_number = account_number
        self._balance = initial_balance
        self._transaction_history = []

        if initial_balance > 0:
            self._transaction_history.append(
                Transaction("initial deposit", initial_balance, initial_balance)
            )

    @property
    def balance(self):
        return self._balance

    def deposit(self, amount):
        if amount <= 0:
            raise InvalidAmountError(amount)

        self._balance += amount
        transaction = Transaction("deposit", amount, self._balance)
        self._transaction_history.append(transaction)
        return self._balance

    def withdraw(self, amount):
        if amount <= 0:
            raise InvalidAmountError(amount)
        if amount > self._balance:
            raise InsufficientFundError(self._balance, amount)

        self._balance -= amount
        transaction = Transaction("withdraw", amount, self._balance)
        self._transaction_history.append(transaction)
        return self._balance

    def get_transaction_history(self):
        return self._transaction_history.copy()

# ---------------- Customer ----------------
class Customer:
    def __init__(self, customer_id, name, email, phone):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.phone = phone
        self.accounts = []

    def add_account(self, account):
        self.accounts.append(account)

    def get_accounts(self):
        return self.accounts

# ---------------- Streamlit App ----------------
st.set_page_config(page_title="Bank Management System", page_icon="🏦", layout="centered")

# Initialize session state (so balance and transactions persist)
if "customer" not in st.session_state:
    customer = Customer("CUST001", "Umair", "umair@gmail.com", "555-0123")
    account = Account("ACC001", 1000)  # Initial balance = $1000
    customer.add_account(account)
    st.session_state.customer = customer
else:
    customer = st.session_state.customer
    account = customer.get_accounts()[0]

st.title("🏦 Python Bank Management System")
st.write(f"👤 **Customer:** {customer.name}")
st.write(f"📧 {customer.email} | 📞 {customer.phone}")
st.write(f"💰 **Current Balance:** ${account.balance}")

# Deposit section
st.subheader("💵 Deposit Money")
deposit_amount = st.number_input("Enter deposit amount:", min_value=0, step=10)
if st.button("Deposit"):
    try:
        account.deposit(deposit_amount)
        st.success(f"Deposited ${deposit_amount}. New balance: ${account.balance}")
    except InvalidAmountError as e:
        st.error(str(e))

# Withdraw section
st.subheader("🏧 Withdraw Money")
withdraw_amount = st.number_input("Enter withdrawal amount:", min_value=0, step=10)
if st.button("Withdraw"):
    try:
        account.withdraw(withdraw_amount)
        st.success(f"Withdrew ${withdraw_amount}. New balance: ${account.balance}")
    except (InvalidAmountError, InsufficientFundError) as e:
        st.error(str(e))

# Transaction history
st.subheader("📜 Transaction History")
transactions = account.get_transaction_history()
if not transactions:
    st.write("No transactions yet.")
else:
    for t in transactions:
        st.text(str(t))
