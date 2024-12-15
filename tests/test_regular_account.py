import pytest
from app.models import RegularAccount




class TestRegularAccount:

    def test_deposit_with_value_positive(self):
        account = RegularAccount(1234,"Milosz",1234,0)
        account.deposit(100)
        assert account.balance == 100

    def test_deposit_with_value_negative(self):
        account = RegularAccount(1234,"Milosz",1234,0)
        with pytest.raises(ValueError):
            account.deposit(-100)

    def test_withdraw_with_value_positive(self):
        account = RegularAccount(1234,"Milosz",1234,100)
        account.withdraw(100)
        assert account.balance == 0

    def test_withdraw_with_value_negative(self):
        account = RegularAccount(1234,"Milosz",1234,100)
        with pytest.raises(ValueError):
            account.withdraw(-100)

    def test_withdraw_with_too_big_amount(self):
        account = RegularAccount(1234,"Milosz",1234,100)
        with pytest.raises(ValueError):
            account.withdraw(1000)

    def test_to_dict(self):
        account = RegularAccount(1234,"Milosz",1234,100)
        dic = account.to_dict()
        assert dic["name"] == "Milosz"
        assert dic["balance"] == 100
        assert dic["user_id"] == 1234
        assert dic["type"] == "RegularAccount"


