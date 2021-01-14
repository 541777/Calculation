import pytest
from calculation import view1


def test_DiscretionarybonusA():
    total =view1.Discretionarybonus(policystartdate='01/08/1983',policynum='A100013',policymember='no')
    assert total == 1000


def test_DiscretionarybonusA1():
    total =view1.Discretionarybonus(policystartdate='01/08/1996',policynum='A100014',policymember='no')
    assert total == 0

def test_DiscretionarybonusB():
    total =view1.Discretionarybonus(policystartdate='10/04/1995',policynum='B100001',policymember='no')
    assert total == 0

def test_DiscretionarybonusB1():
    total =view1.Discretionarybonus(policystartdate='10/04/1995',policynum='B100000',policymember='yes')
    assert total == 1000

def test_DiscretionarybonusC1():
    total =view1.Discretionarybonus(policystartdate='10/04/1995',policynum='C100000',policymember='yes')
    assert total == 1000

def test_DiscretionarybonusC2():
    total =view1.Discretionarybonus(policystartdate='10/04/1982',policynum='C100000',policymember='no')
    assert total == 0



