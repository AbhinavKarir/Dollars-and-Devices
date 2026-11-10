def add_tax(price, tax_rate):
    total = price * (1 + tax_rate)
    return total
print(add_tax(100, 0.13))

def percent_change(old,new):
    number_changed = new - old
    percent_change = (number_changed / old) * 100
    return percent_change
print(percent_change(50,75))
print(percent_change(75,50))
print(percent_change(52.7,52.0))
