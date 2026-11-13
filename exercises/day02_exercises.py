#Exercise 1 (Conditions)
tonnes_received = 50.0
tonnes_recovered_total = 39.5
recovery_rate = (tonnes_recovered_total/tonnes_received) * 100
print("Recovery rate: ", recovery_rate, "%")
if recovery_rate >= 80:
    print("Status: On Target")
else:
    print("Status: Below Target")

#Exercise 2 : My first function
def efficiency_ratio (expenses, revenue):
    return (expenses/revenue) * 100
print(round(efficiency_ratio(7900,15000), 1))

#exercise 3: loop + function + conditions
#Simulated Figures in C$ millions
revenue = {
    "Alder Bank": 15000,
    "Birch Trust": 12000,
    "Juniper Bank": 10000,
    "Maple Harbour Bank": 8000,
    "Cedar Bank": 9000,
    "Spruce Financial": 11000,
}

expenses = {
    "Alder Bank": 7900,
    "Birch Trust": 6500,
    "Juniper Bank": 5500,
    "Maple Harbour Bank": 4500,
    "Cedar Bank": 5000,
    "Spruce Financial": 6000,
}

for bank in revenue:
    ratio = efficiency_ratio(expenses[bank], revenue[bank])

    if ratio < 55:
        status = "Strong"
    elif ratio < 65:
        status = "Acceptable"
    else:
        status = "Needs Attention"

    print(bank, "->", round(ratio, 1), "%", "|", status)

#Exercise 4: Practice

def profit_margin(sales,cost):
    return ((sales-cost)/ sales) * 100
margin = profit_margin(1000, 700)
print(round(margin, 1))

if margin >= 25:
    print("Status = Healthy")
elif margin >= 10:
    print("Status = Can Improve")
else:
    print("Status = Thin Margin")

