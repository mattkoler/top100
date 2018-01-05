def tax_brackets(gross_income, deduc=12700):
    # married only
    # deduc is for itemizing in 2017 (majority would be from income tax)
    brackets_17 = (
        (18650, 0.1),
        (75900-18650, 0.15),
        (153100-75900, 0.25),
        (233350-153100, 0.28),
        (416700-233350, 0.33),
        (470700-416700, 0.35),
        (1e100, 0.393)
    )

    tax_17 = 0.0
    gross_income_17 = gross_income - deduc
    for bracket in brackets_17:
        if gross_income_17 <= bracket[0]:
            tax_17 += gross_income_17 * bracket[1]
            break
        tax_17 += bracket[0] * bracket[1]
        gross_income_17 -= bracket[0]

    #print('2017 total tax ${:,.0f} with tax rate of {:.2f}%. (Assumes deduction of ${:,.0f})'.format(tax_17,(tax_17/gross_income)*100,deduc))

    brackets_s18 = (
        (19050, 0.1),
        (77400-19050, 0.12),
        (140000-77400, 0.22),
        (320000-140000, 0.24),
        (400000-320000, 0.32),
        (1000000-400000, 0.35),
        (1e100, 0.385)
        )

    tax_s18 = 0.0
    gross_income_s18 = gross_income - 12700 # standard deduction
    for bracket in brackets_s18:
        if gross_income_s18 <= bracket[0]:
            tax_s18 += gross_income_s18 * bracket[1]
            break
        tax_s18 += bracket[0] * bracket[1]
        gross_income_s18 -= bracket[0]

    #print("Senate 2018 total tax ${:,.0f} with tax rate of {:.2f}%. (Assumes standard deduction of $12.7k)".format(tax_s18,(tax_s18/gross_income)*100))

    brackets_r18 = (
        (24000, 0.0),
        (90000-24000, 0.12),
        (260000-90000, 0.25),
        (1000000-260000, 0.35),
        (1e100, 0.396)
        )

    tax_r18 = 0.0
    gross_income_r18 = gross_income # standard deduction built in above
    for bracket in brackets_r18:
        if gross_income_r18 <= bracket[0]:
            tax_r18 += gross_income_r18 * bracket[1]
            break
        tax_r18 += bracket[0] * bracket[1]
        gross_income_r18 -= bracket[0]

    #print("House 2018 total tax ${:,.0f} with tax rate of {:.2f}%. (Assumes standard deduction of $24k)".format(tax_r18,(tax_r18/gross_income)*100))
    print(tax_17)

def california_tax(gross_income):
    brackets_ca = (
        (15700, 0.01),
        (37220-15700, 0.02),
        (58744-37220, 0.04),
        (81546-58744, 0.06),
        (103060-81546, 0.08),
        (526444-103060, 0.093),
        (631732-526444, .103),
        (1052886-631732, 0.113),
        (1e100, 0.123)
    )

    tax_ca = 0.0
    for bracket in brackets_ca:
        if gross_income <= bracket[0]:
            tax_ca += gross_income * bracket[1]
            break
        tax_ca += bracket[0] * bracket[1]
        gross_income -= bracket[0]
    return max(12700, tax_ca+10000)

        
for income in range(100000,500001,10000):
    #print('Taxes at ${:,}'.format(income))
    tax_brackets(income,california_tax(income))
    #print('')
    
