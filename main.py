import matplotlib.pyplot as plt
import json
class Person():
    def __init__(self,name: str, is_literate: bool):
        ''''
        Person class

        Attributes:
        - name: Name of person
        - Is_literate: Stores whether person is literate or iliterate
        - Simulation_year: Tracks current year of simulation


        - year_stats(list of {}): Each index corresponding to year number
            - Library keys: Wealth, total_debt_paid, total_morgage_paid, total_savings
        - years_in_debt: The time person carried credit card and student loan debt only
        - total_debt_paid : Total payments toward credit card / student loan debt only
        '''
        
        self.name = name
        self.is_literate = is_literate
        self.has_a_house = False
        self.morgage_payment = 0.0

        self.checking_balance = 0.0
        self.savings_balance = 5000
        self.debt = 30100
        self.morgage_loan = 0.0

        self.debt_paid = 0.0
        self.morgage_paid = 0.0
        
        self.years_in_debt = 0
        self.years_renting = 0
        self._wealth = int(self.savings_balance + self.checking_balance - self.debt - self.morgage_loan)
        
        #List of libraries containitng stats for each year
        self.year = []
        year_stats = {
                "wealth": self.wealth,
                "total_debt_paid": self.debt_paid,
                "total_morgage_paid": self.morgage_paid,
                "total_savings": self.savings_balance}
        self.year.append(year_stats)

    @property
    def wealth(self) -> int:
        return self._wealth

    @wealth.setter
    def wealth(self,value):
        self._wealth = value

    def allocate_salary(self):
        '''Increase the amount in savings and checking'''
        self.checking_balance += 18300
        self.savings_balance += 12200

    def recieve_savings_interest(self):
        '''Increases the amount of money in savings'''
        if self.is_literate:
            self.savings_balance = self.savings_balance * 1.07
        else:
            self.savings_balance = self.savings_balance * 1.02

    def debt_payment_and_interest(self):
        '''
        (Increases the years_in_debt by one.
        Reduce the amount of debt, then increase with percent of remaining debt.
        Add the debt  paid  to debt_paid, have a for loop that continues until debt for given year is 0)
        '''
        if self.debt != 0.0:
            payment = 0.0
            self.years_in_debt += 1

            #Determine debt payment for year
            if self.is_literate:
                payment = (self.debt * 0.03) + 15
            else:
                payment = (self.debt * 0.03) + 1
            
            #Ensure payment isn't more than actual debt
            if payment > self.debt: payment = self.debt

            #Add debt paid and add interest to remaining debt
            self.debt_paid += payment
            self.debt = (self.debt - self.debt_paid) * 1.2

            #Reduce savings or checking account? 
            if payment > self.checking_balance:
                self.savings_balance -= payment
            else:
                self.checking_balance -= payment
    
    def rent_or_morgage_payment(self):
        '''
        (If not has_a_house(), run a for loop until they buy a house.
        If they don't have a house charge rent from checkings or savings)
        '''

        for months in range(12):
            if not self.has_a_house:
                #Check if they can buy a home
                if (self.is_literate) and (self.checking_balance >= (175000 * 0.2)):
                    self.morgage_loan = 175000 - (175000 * 0.2)
                    self.buy_house()
                elif (not self.is_literate) and (self.checking_balance > (175000 * 0.05)):
                    self.morgage_loan = 175000 - (175000 * 0.05)
                    self.buy_house()
                else: #If they can't buy a home, pay rent
                    if months == 0: self.years_renting += 1
                    self.checking_balance -= 850

            if self.has_a_house:   
                #Pay morgage
                if self.morgage_loan != 0: #If there is still a morgage to pay
                    if self.morgage_payment > self.morgage_loan: self.morgage_payment = self.morgage_loan
                    if self.morgage_payment > self.checking_balance:
                        self.savings_balance -= self.morgage_payment
                        self.morgage_loan -= self.morgage_payment
                        self.morgage_paid += self.morgage_payment
                    else: #If there is enough money in checking remove them there
                        self.checking_balance -= self.morgage_payment
                        self.morgage_loan -= self.morgage_payment
                        self.morgage_paid += self.morgage_payment

                #Increase years in debr (for if other debt is paid off)
                if self.debt == 0.0:
                    self.years_in_debt += 1

    def buy_house(self):
        '''(1. Calculuate loan amount
            2. Calculuate monthly morgage payment and assigns it to self.morgage_payment()
            3. Update has house to be true)
            4. Pays for first house'''
        if self.is_literate:
            i = (4.5/100) / 12
        else:
            i = (5/100) /12
        
        N = 360
        D = ((((i+1)**N) - 1) / (i*((i+1)**N)))      
        self.morgage_payment = (self.morgage_loan / D)
        self.savings_balance -= self.morgage_payment
        self.has_a_house =True
        

    def save_year_stats(self):
        '''
        Adds a new libabry at year number of simulation to track the welth, total_debt_paid, total_morgage_paid and total_savings
        paid year by year by person. 

        Result: 
        Adds a new libabry to with stats for the current year
        Ex: self.year[3][wealth] will give the person's wealth for year 3
        '''
        self._wealth = int(self.savings_balance + self.checking_balance - self.debt - self.morgage_loan)
        year_stats = {
                "wealth": self.wealth,
                "total_debt_paid": self.debt_paid,
                "total_morgage_paid": self.morgage_paid,
                "total_savings": self.savings_balance}
        self.year.append(year_stats)
        
    def age(self):
        self.allocate_salary()
        self.recieve_savings_interest()
        self.debt_payment_and_interest()
        self.rent_or_morgage_payment()
        self.save_year_stats()

        #-------
        '''
        Wealth Grapth
        - x: The year number
        - y: Networth at the end of the year
        '''
class Simulation():
    def __init__(self,person: Person,years:int = 40):
        self.person = person
        self.years = years
    
    def run(self)-> list:
        wealth_overtime = []
        human_stats = self.person.year
        for year_num in range(self.years):
            self.person.age()
            item_to_be_appened = human_stats[year_num]["wealth"]
            wealth_overtime.append(item_to_be_appened)
        return wealth_overtime

    def summary(self)->dict:
        summary_dict = {}
        summary_dict["wealth"] = self.person.wealth
        summary_dict["years_in_debt"] = self.person.years_in_debt
        summary_dict["total_debt_paid"] = self.person.debt_paid
        summary_dict["total_mortgage_paid"] = self.person.morgage_paid
        return summary_dict

def plot_wealth(fl_wealth_history: List, nfl_wealth_history: List, filename: str =
"wealth_over_time.png"):
    #Create num years array
    flyears_arr = []
    for year in range(len(fl_wealth_history)):
        flyears_arr.append(year+1)
    
    plt.subplot(1,2,1)
    plt.bar(flyears_arr,fl_wealth_history, color = "Green")
    plt.xlabel("Years")
    plt.ylabel("Wealth (dollars)")
    plt.grid(True)
    plt.title("Financially literate person versus ")
    plt.tight_layout()

    
    nflyears_arr = []
    for year in range(len(nfl_wealth_history)):
        nflyears_arr.append(year+1)
    plt.subplot(1,2,2)
    plt.bar(nflyears_arr,nfl_wealth_history,color = "Red")
    plt.xlabel("Years")
    plt.ylabel("Wealth (dollars)")
    plt.grid(True)
    plt.title("Non-financially literate over time")
    plt.tight_layout()

    plt.show()
    plt.savefig(filename)


nisema = Person("nisema", True)
sim_fl = Simulation(nisema,10)
wealth_fl = sim_fl.run()
summary_fln = sim_fl.summary()
print(wealth_fl)
print(summary_fln)

holly = Person("holly",False)
sim_nfl = Simulation(holly,10)
wealth_nfl = sim_nfl.run()
summary_nfl = sim_nfl.summary()
print(wealth_nfl)
print(summary_nfl)

with open("fl_yearly_stats.txt", "w") as file:
    for dict in nisema.year:
        json.dump(dict,file,indent=4)

plot_wealth(wealth_fl,wealth_nfl)


'''
holly = Person("holly", False)

for people in (nisema,holly):
    
    print(f"Savings {people.savings_balance}")
    print(f"Checking {people.checking_balance}")
    print(f"Debt: {people.debt}")
    print(f"Years in Debt {people.years_in_debt}")
    print(f"Rent or morgage info: Loan: {people.morgage_loan} Years renting: {people.years_renting}")

    people.age()
    people.age()
    people.age()

    print(f"Savings {people.savings_balance}")
    print(f"Checking {people.checking_balance}")
    print(f"Debt: {people.debt}")
    print(f"Years in Debt {people.years_in_debt}")
    print(f"Rent or morgage info: Loan: {people.morgage_loan} Years renting: {people.years_renting}")
'''

