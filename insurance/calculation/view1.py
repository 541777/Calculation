from django.shortcuts import render
from django.http import HttpResponse
from datetime import date
import mysql.connector
import pytest


def cal(request):
    return render(request, 'calculation\index.html')



def add(request):
    a = request.POST['num1']

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="project1"
    )

    sql_Query = "SELECT * FROM policyvalues where policy_no= '%s'" %a

    mycursor = mydb.cursor()
    mycursor.execute(sql_Query)
    policydetails = mycursor.fetchone()

    if policydetails:
        policynumber = policydetails[0]
        policystart = policydetails[1]
        policypermium = policydetails[2]
        policymembership = policydetails[3]
        policyuplift = policydetails[4]

        policy_managementfee = 0
        if (policynumber[0] == "A"):
            policy_managementfee = calmanagement(0.03, policypermium)
        elif (policynumber[0] == "B"):
            policy_managementfee = calmanagement(0.05, policypermium)
        elif (policynumber[0] == "C"):
            policy_managementfee = calmanagement(0.07, policypermium)

        polstartdate = policystart
        policy_discretionary = Discretionarybonus(polstartdate, policynumber, policymembership)

        policy_uplift_percentage = caluplift(policyuplift)

        policy_maturity = ((policypermium - policy_managementfee) + policy_discretionary) * policy_uplift_percentage
        return render(request, 'calculation\index.html',
                      {'result': a, 'result2': policystart, 'result3': policypermium, 'result4': policymembership,
                       'result5': policyuplift, 'result6': policy_maturity})
    else:

        print("else part")
        m = "policy is not found"
        return render(request, 'calculation\index.html',
                      {'result': a,'result15': m})


def calmanagement(polmanagementfee, polpermium):
    return polmanagementfee * polpermium

def Discretionarybonus(policystartdate, policynum, policymember):
        policydetails = policynum
        policymem = policymember
        if ((policydetails[0] == "A") and (policystartdate[6:10] < '1990')):
            Discretionary = 1000
        elif ((policydetails[0] == "B") and (policymem == "yes")):
            Discretionary = 1000
        elif ((policydetails[0] == "C") and (('1990' <= policystartdate[6:10]) and (policymem == "yes"))):
             Discretionary = 1000
        else:
             Discretionary = 0

        return Discretionary

def caluplift(policyup):
    upamt = (policyup / 100) + 1
    return upamt




