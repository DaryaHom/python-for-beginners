import pytest
from tasks import is_inn_correct, BankAccount, is_login_correct, is_hex_color_correct

@pytest.mark.parametrize(
    "inn, is_correct",
    [
        ("500100732259", True),
        ("123456789012", True),

        ("12345678901", False),
        ("1234567890123", False),
        ("12345678901a", False),
        ("1234 567890", False),
        (" 1234567890", False),
        ("1234567890 ", False),
        ("", False),
    ]
)
def test_is_inn_correct(inn, is_correct):
    assert is_inn_correct(inn) == is_correct

"""
Напишите тесты, которые проверяют:
1. Начальный баланс — при создании счёта BankAccount() его balance должен быть 0.0.
2. Пополнение счёта — после deposit(100) баланс становится 100.0.
3. Снятие денег — если сначала положить 200, а потом снять 50, баланс должен стать 150.0.
4. Независимость счетов — если создать два счёта, операции над одним не влияют на другой.
"""
def test_init_balance():
    acc = BankAccount()
    assert acc.balance == 0.0

def test_deposit():
    acc = BankAccount()
    acc.deposit(100)
    assert acc.balance == 100.0

def test_deposit_with_withdraw():
    acc = BankAccount()
    acc.deposit(200)
    acc.withdraw(50)
    assert acc.balance == 150.0

def test_bank_acc_independent():
    acc_1, acc_2 = BankAccount(), BankAccount()
    acc_1.deposit(200)
    acc_2.withdraw(50)
    assert acc_1.balance == 200.0; acc_2.balance == -50.0

@pytest.mark.parametrize(
    "login, is_correct",
    [
        ("i_ivanov", True),
        ("i.ivanov", True),

        ("_i.ivanov", False),
        ("i.ivanov_", False),
        ("i..ivanov", False),
        ("i___ivanov", False),
        ("i._ivanov", False),
        ("i.ivanov__", False),
        ("", False),
    ]
)
def test_is_login_correct(login, is_correct):
    assert is_login_correct(login) == is_correct


@pytest.mark.parametrize(
    "color, is_correct",
    [
        ("#00ffff", True),
        ("#5d8aa8", True),
        ("#0ff", True),

        ("00ffff", False),
        ("#00fffi", False),
        ("#00fffff", False),
        ("_00fff", False),
        ("#0f", False),
        ("", False),
    ]
)
def test_is_hex_color_correct(color, is_correct):
    assert is_hex_color_correct(color) == is_correct
