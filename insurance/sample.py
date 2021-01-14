from django.shortcuts import render
from django.http import HttpResponse
from datetime import date
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="project1"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM student1")

myresult = mycursor.fetchall()

for x in myresult:
    print(x)


def cal(request):
    return render(request, 'calculation\index.html')


def add(request):
    a = request.POST['num1']

    policynumber = a
    policystart = '10/01/1988'
    policypermium = 10000
    policymembership = 'no'
    policyuplift = 40

    def calmanagement(polmanagementfee, polpermium):
        return polmanagementfee * polpermium

    def Discretionarybonus(policystartdate, policynum, policymember):
        policydetails = policynum
        date_str2 = '12/1/1988'
        Apoldate = date_str2
        policymem = policymember
        if (policydetails[0] == "A" and (Apoldate >= policystartdate)):
            Discretionary = 1000
        elif policydetails[0] == "B" and (policymem == "yes"):
            Discretionary = 1000
        elif policydetails[0] == "C" and (((Apoldate >= policystartdate)) and (policymem == "yes")):
            Discretionary = 1000
        else:
            Discretionary = 0

        return Discretionary

    def caluplift(policyup):
        upamt = (policyup / 100) + 1
        return upamt

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

    return render(request, 'calculation\output.html',
                  {'result': a, 'result2': policystart, 'result3': policypermium, 'result4': policymembership,
                   'result5': policyuplift, 'result6':policy_maturity})