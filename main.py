import matplotlib.pyplot as plt
import json
from math import *
class Person():

    HOUSE_PRICE = 175000
    INIT_SAVINGS_BAL = 5000
    INIT_DEBT = 30100
    INT_ON_REMAINING_DEBT = 1.2
    INT_ON_SAVINGS_FL = 1.07
    INT_ON_SAVINGS_NFL = 1.02
    INT_ON_MORTGAGE_FL = 4.5
    INT_ON_MORTGAGE_NFL = 5.0
    DEBT_PAYMENT_PERC = 0.03
    RENT_PER_MONTH = 850
    SALARY_TO_CHECKING = 18300
    SALARY_TO_SAVINGS = 12200
    
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
        self.savings_balance = Person.INIT_SAVINGS_BAL
        self.debt = Person.INIT_DEBT
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
                "debt":self.debt,
                "total_debt_paid": self.debt_paid,
                "mortgage_loan": self.morgage_loan,
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
        self.checking_balance += Person.SALARY_TO_CHECKING
        self.savings_balance += Person.SALARY_TO_SAVINGS

    def recieve_savings_interest(self):
        '''Increases the amount of money in savings'''
        if self.is_literate:
            self.savings_balance = round(self.savings_balance * Person.INT_ON_SAVINGS_FL,2)
        else:
            self.savings_balance = round(self.savings_balance * Person.INT_ON_SAVINGS_NFL,2)

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
                payment = round((self.debt * Person.DEBT_PAYMENT_PERC) + 15,2)
            else:
                payment = round((self.debt * Person.DEBT_PAYMENT_PERC) + 1,2)
            
            #Ensure payment isn't more than actual debt
            if payment > self.debt: 
                payment = self.debt
                

            #Add debt paid and add interest to remaining debt
            self.debt_paid += payment
            self.debt = round((self.debt - self.debt_paid) * Person.INT_ON_REMAINING_DEBT,2)

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
                if (self.is_literate) and (self.checking_balance >= (Person.HOUSE_PRICE * 0.2)):
                    self.morgage_loan = Person.HOUSE_PRICE - (Person.HOUSE_PRICE * 0.2)
                    self.buy_house()
                elif (not self.is_literate) and (self.checking_balance > (Person.HOUSE_PRICE * 0.05)):
                    self.morgage_loan = Person.HOUSE_PRICE - (Person.HOUSE_PRICE * 0.05)
                    self.buy_house()
                else: #If they can't buy a home, pay rent
                    if months == 0: self.years_renting += 1
                    self.checking_balance -= Person.RENT_PER_MONTH

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
        '''(1. Loan amount calculated in rent or morgage function
            2. Calculuate monthly morgage payment and assigns it to self.morgage_payment()
            3. Update has house to be true)
            4. Pays for first house'''
        if self.is_literate:
            i = (Person.INT_ON_MORTGAGE_FL/100) / 12
        else:
            i = (Person.INT_ON_MORTGAGE_NFL/100) /12
        
        N = 360
        D = ((((i+1)**N) - 1) / (i*((i+1)**N)))      
        self.morgage_payment = round(self.morgage_loan / D,2)
        self.checking_balance -= self.morgage_payment
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
                "debt":self.debt,
                "total_debt_paid": self.debt_paid,
                "mortgage_loan": self.morgage_loan,
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
        for year_num in range((self.years) + 1):
            self.person.age()
            item_to_be_appened = human_stats[year_num]["wealth"]
            wealth_overtime.append(item_to_be_appened)
        return wealth_overtime

    def summary(self)->dict:
        summary_dict = {}
        summary_dict["final_wealth"] = self.person.wealth
        summary_dict["years_in_debt"] = self.person.years_in_debt
        summary_dict["total_debt_paid"] = round(self.person.debt_paid,2)
        summary_dict["total_mortgage_paid"] = round(self.person.morgage_paid,2)
        return summary_dict

def plot_wealth(fl_wealth_history: list, nfl_wealth_history: list, filename: str =
"wealth_over_time.png"):
    #Create num years arrayS
    flyears_arr = []
    for year in range(len(fl_wealth_history)):
        flyears_arr.append(year+1)
    
    nflyears_arr = []
    for year in range(len(nfl_wealth_history)):
        nflyears_arr.append(year+1)

    #Create figures for plotting
    fig,axs = plt.subplots(2, sharex=True)
    fig.suptitle("Financially-literate vs Financially-iliterate wealth over time")
    axs[0].bar(flyears_arr,fl_wealth_history,color="Green")
    axs[0].set_title('Financially literate person')
    axs[0].set(ylabel="wealth (in dollars)")
    axs[1].bar(nflyears_arr,nfl_wealth_history, color="Red")
    axs[1].set_title('Financially iliterate person')
    axs[1].set(ylabel="wealth (in dollars)")

    plt.show()
    plt.savefig(filename)

def run_tests() -> None:
    #Create people and simulations
    financially_lit = Person("Hannah",True)
    financially_unlit = Person("Marcus",False)
    sim_FL = Simulation(financially_lit,40)
    sim_NFL = Simulation(financially_unlit,40)

    person2 = financially_unlit

    #Person(): init()
    fn_name = 'Person constructor'
    person = financially_lit
    result = person.name
    expected = 'Hannah'
    error_message= f"While testing {fn_name}, expected {expected} got {result}"
    assert expected == result,error_message

    result = person.savings_balance
    expected = 5000
    error_message= f"While testing {fn_name}, expected {expected} got {result}"
    assert expected == result,error_message

    result = person.years_renting
    expected = 0
    error_message= f"While testing {fn_name}, expected {expected} got {result}"
    assert expected == result,error_message

    #Person wealth() getter and setter
    fn_name = "Wealth getter"
    result = person.wealth
    expected = -25100
    error_message= f"While testing {fn_name}, expected {expected} got {result}"
    assert expected == result,error_message

    fn_name = "Wealth setter"
    person.wealth = 0
    result = person.wealth
    expected = 0
    error_message= f"While testing {fn_name}, expected {expected} got {result}"
    assert expected == result,error_message
    person.wealth = -25100

    #Person allocate salary
    #Test 1 - Initial allocation correct
    fn_name = "allocate salary"
    person.allocate_salary()
    result = person.checking_balance + person.savings_balance
    expected = 35500.0
    error_message= f"While testing {fn_name}, expected {expected} got {result}"
    assert expected == result,error_message

    #Test 2 - Ensures that correct amounts are in each account
    result = person.checking_balance
    expected = 18300.0
    error_message= f"While testing {fn_name}, expected {expected} got {result}"
    assert expected == result,error_message

    #Test 3 
    result = person.savings_balance
    expected = 17200.0
    result = person.savings_balance
    error_message= f"While testing {fn_name}, expected {expected} got {result}"
    assert expected == result,error_message


   #Person - interest on savings
   #Test 1 - Financially literate person
    fn_name = "receive_savings_interest"
    person.recieve_savings_interest()
    result = person.savings_balance
    expected = 18404.0
    error_message= f"While testing {fn_name}, expected {expected} got {result}"
    assert expected == result,error_message

    #Test 2 - Test if the savings were never increased
    person2.recieve_savings_interest()
    result = person2.savings_balance
    expected = 5100.0
    error_message= f"While testing {fn_name}, expected {expected} got {result}"
    assert expected == result,error_message

    #Test 3 - Financially illerate
    person2.allocate_salary()
    person2.recieve_savings_interest()
    result = person2.savings_balance
    expected = 17646.0
    error_message= f"While testing {fn_name}, expected {expected} got {result}"
    assert expected == result,error_message

    #Person - debt payments and interest
    fn_name = "debt_payment_and_interest"
    person.debt_payment_and_interest()
    result = person.debt_paid
    expected = 918.0
    error_message= f"While testing {fn_name}, expected {expected} got {result}"
    assert expected == result,error_message

    result = person.debt
    expected = 35018.4
    error_message= f"While testing {fn_name}, expected {expected} got {result}"
    assert expected == result,error_message

    result = person.checking_balance
    expected = 17382.0
    error_message= f"While testing {fn_name}, expected {expected} got {result}"
    assert expected == result,error_message

    #Person rent_or_mortgage 
    fn_name = "rent_or_mortgage_payment"
    person.rent_or_morgage_payment()
    result = person.years_renting
    expected = 1
    error_message= f"While testing {fn_name}, expected {expected} got {result}"
    assert expected == result,error_message

    result = person.checking_balance
    expected = 7182.0
    error_message= f"While testing {fn_name}, expected {expected} got {result}"
    assert expected == result,error_message

    result = person.has_a_house
    expected = False
    error_message= f"While testing {fn_name}, expected {expected} got {result}"
    assert expected == result,error_message

    #Person- buy a house
    fn_name = "Buy a house"
    person2.rent_or_morgage_payment()
    person2.buy_house()
    result = person2.has_a_house
    expected = True
    error_message= f"While testing {fn_name}, expected {expected} got {result}"
    assert expected == result,error_message

    result = person2.morgage_payment
    expected = 834.97
    error_message= f"While testing {fn_name}, expected {expected} got {result}"
    assert expected == result,error_message

    result = person2.checking_balance
    expected = 5862.920000000003 #Couldn't find why it wasn't rounding figures up
    error_message= f"While testing {fn_name}, expected {expected} got {result}"
    assert expected == result,error_message

    #Person - save_year_stats and age (They can and should be tested together)
    person3 = Person('Nancy',True)
    
    fn_name = "save_year_stats"
    person3.save_year_stats()
    result = person3.year[0]
    expected = {
                "wealth": -25100,
                "debt": 30100,
                "total_debt_paid": 0.0,
                "mortgage_loan":0.0,
                "total_morgage_paid": 0.0,
                "total_savings": 5000}
    error_message= f"While testing {fn_name}, expected {expected} got {result}"
    assert expected == result,error_message

    fn_name = "save_year_stats and age"
    person3.age()
    result = person3.year[1]
    expected = {'wealth': -25100,
                'debt': 30100,
                'total_debt_paid': 0.0,
                'mortgage_loan': 0.0,
                'total_morgage_paid': 0.0,
                'total_savings': 5000}
    error_message= f"While testing {fn_name}, expected {expected} got {result}"
    assert expected == result,error_message

    person.age()
    result = person.year[1]
    expected = {'wealth': 7320,
                'debt': 39641.82,
                'total_debt_paid': 1983.55,
                'mortgage_loan': 0.0,
                'total_morgage_paid': 0.0,
                'total_savings': 32746.28}
    error_message= f"While testing {fn_name}, expected {expected} got {result}"
    assert expected == result,error_message

    #Simulation tests
    #Simulation - constructor
    fn_name = "Simulation constructor"
    result = sim_FL.person.name
    expected = "Hannah"
    error_message= f"While testing {fn_name}, expected {expected} got {result}"
    assert expected == result,error_message

    result = sim_NFL.person.name
    expected = "Marcus"
    error_message= f"While testing {fn_name}, expected {expected} got {result}"
    assert expected == result,error_message

    result = sim_FL.years
    expected = 40
    error_message= f"While testing {fn_name}, expected {expected} got {result}"
    assert expected == result,error_message

    #Simulation - run
    sim_FL_3 = Simulation(person3,5)
    fn_name = "Simulation run"
    result = sim_FL_3.run()
    expected = [-25100, -25100, -9432, 7320, 25459, -85187]
    error_message= f"While testing {fn_name}, expected {expected} got {result}"
    assert expected == result,error_message

    person4 = Person("Andrew", False)
    sim_Andrew = Simulation(person4,0)
    result = sim_Andrew.run()
    expected = [-25100]
    error_message= f"While testing {fn_name}, expected {expected} got {result}"
    assert expected == result,error_message

    sim_Andrew = Simulation(person4,2)
    result = sim_Andrew.run()
    expected = [-25100, -167237, -141854]
    error_message= f"While testing {fn_name}, expected {expected} got {result}"
    assert expected == result,error_message

    #Simulation - summary
    fn_name = "Simulation summary"
    result = sim_Andrew.summary()
    expected = {'final_wealth': -88975,
                'years_in_debt': 4,
                'total_debt_paid': 4464.6,
                'total_mortgage_paid': 42838.56}
    error_message= f"While testing {fn_name}, expected {expected} got {result}"
    assert expected == result,error_message

if __name__ == "__main__":
    fl = Person("fl", True)
    nfl = Person("nfl", False)

    sim_fl = Simulation(fl, years=40)
    sim_nfl = Simulation(nfl, years=40)
    fl_wealth_history = sim_fl.run()
    nfl_wealth_history = sim_nfl.run()

    plot_wealth(fl_wealth_history, nfl_wealth_history)
    summary_fl = sim_fl.summary()
    summary_nfl = sim_nfl.summary()

    print(
    f"RESULT "
    f"fl_final_wealth={summary_fl['final_wealth']} "
    f"nfl_final_wealth={summary_nfl['final_wealth']} "
    f"fl_years_in_debt={summary_fl['years_in_debt']} "
    f"nfl_years_in_debt={summary_nfl['years_in_debt']} "
    f"fl_total_debt_paid={summary_fl['total_debt_paid']} "
    f"nfl_total_debt_paid={summary_nfl['total_debt_paid']} "
    f"fl_total_mortgage_paid={summary_fl['total_mortgage_paid']} "
    f"nfl_total_mortgage_paid={summary_nfl['total_mortgage_paid']}")



