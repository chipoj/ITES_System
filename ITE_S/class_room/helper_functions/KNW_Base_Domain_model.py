#from pyknow import KnowledgeEngine, Fact, Rule
# from experta import *
from experta import KnowledgeEngine, Fact, Rule

import pymysql


class TaxationRuleEngine(KnowledgeEngine):  # Inherit from KnowledgeEngine
    def __init__(self):
        super().__init__()  # Initialize KnowledgeEngine
        self.dynamic_rules = []  # List to store dynamically added rules
        self.rule_fired = False
        self.correct = False
        self.feedback_tax = "" 

    def add_feedback(self, message):
        """Add a feedback message to the feedback list."""
        # Method to add feedback (optional implementation)
        print(f"Feedback: {message}")
        self.feedback_tax += f"Feedback: {message}\n"  # Concatenate the new message to the feedback
    
    def get_feedback(self):
        """Return all collected feedback."""
        return self.feedback_tax  # Return the list of feedback messages  # This can be customized based on how you want to manage feedback
    
    def add_rule(self, rule):
        """Method to add dynamically created rules"""
        self.dynamic_rules.append(rule)
        print(f"Rule added: {rule}")

    def run(self, *args, **kwargs):
        """Override the run method to execute dynamic rules as well as static rules."""
        # Execute dynamic rules
        for rule in self.dynamic_rules:
            rule(self)  # Apply each dynamic rule to the engine instance
        
        # Run the regular engine rules
        super().run(*args, **kwargs)  # Ensure super() is called here to run rules    

    @Rule(Fact(concept='dividend'), Fact(source='foreign'), Fact(residency='ordinarily_resident'))
    def foreign_dividends_gross_income(self):
        self.correct = True
        self.rule_fired = False
        
        message = "Student correctly identified the rule: Foreign dividend is part of gross income because the taxpayer is ordinarily resident."
        self.add_feedback(message)
        print (message)
    
    @Rule(Fact(concept='dividend'), Fact(source='Non'), Fact(residency='Non'))
    def foreign_dividends_gross_income2(self):
        self.correct = True
        self.rule_fired = True
        
        message= """The student did not identify the rule: 
        The foreign dividend is part of gross income because the taxpayer is ordinarily resident."""
        self.add_feedback(message)
        print (message)

    @Rule(Fact(concept='dividend'), Fact(tax_rate=20), Fact(source='foreign'))
    def foreign_dividends_tax_rate(self):
        self.correct = True
        self.rule_fired = True
        
        message="Student correctly identified the rule: The foreign dividend is taxed at 20%."
        self.add_feedback(message)
        print (message)

    @Rule(Fact(concept='dividend'), Fact(tax_rate='Non'), Fact(source='Non'))
    def foreign_dividends_tax_rate2(self):
        self.correct = True
        self.rule_fired = True
       
        message= "The student did not identify the correct rule:  tax rate of 20%."
        self.add_feedback(message)
        print (message)
    
    @Rule(Fact(concept='dividend_capital'), Fact(nature='capital'))
    def capital_nature_dividend(self):
        self.correct = True
        self.rule_fired = True
        
        message="Student correctly identified the rule: The dividend is capital in nature and not part of gross income."
        self.add_feedback(message)
        print (message)

    @Rule(Fact(concept='dividend_capital'), Fact(nature='capital'))
    def capital_nature_dividend2(self):
        self.correct = True
        self.rule_fired = True
        
        message= "Student correctly identified the rule: The dividend is capital in nature and not part of gross income."
        self.add_feedback(message)
        print (message)

    
    @Rule(Fact(concept='local_source'), Fact(location='Zimbabwe'))
    def local_source(self):
        self.correct = True
        self.rule_fired = True
        
        message= ("""Student correctly identified the rule: Where the process of manufacturing and selling goods or services happens across two 
        jurisdictions, the determination of the true source involves considering where the dominant
        activity has taken place.. or Where the process of manufacturing and selling goods or services happens across two
        jurisdictions, the determination of the true source involves considering where the dominant
        activity has taken place.""")
        self.add_feedback(message)
        print (message)

    @Rule(Fact(concept='local_source'), Fact(location='Non'))
    def local_source2(self):
        self.correct = True
        self.rule_fired = True
        
        message=("""The student did not correctly identify the rule: Where the process of manufacturing and 
        selling goods or services happens across two 
        jurisdictions, the determination of the true source involves considering where the dominant
        activity has taken place.. or Where the process of manufacturing and selling goods or services happens across two
        jurisdictions, the determination of the true source involves considering where the dominant
        activity has taken place.""")
        self.add_feedback(message)
        print (message)
    
    @Rule(Fact(concept='gross_income_capital'), Fact(capital_nature='False'))
    def capital_nature_grossincome(self):
        self.correct = True
        self.rule_fired = True
        
        message= """Student correctly identified the rule: Amounts which are capital in nature are excluded from gross income or
        An amount received
        by way of damages or compensation for the loss surrender or sterilization of a fixed
        capital asset or of the taxpayer’s income-producing machine is a receipt of a capital
        nature."""
        self.add_feedback(message)
        print (message)

    @Rule(Fact(concept='gross_income_capital'), Fact(capital_nature='Non'))
    def capital_nature_grossincome2(self):
        self.correct = True
        self.rule_fired = True
        
        message= """The student did not correctly identify the rule:  Amounts that are capital in nature are excluded from gross income or
        An amount received
        by way of damages or compensation for the loss surrender or sterilization of a fixed
        capital asset or of the taxpayer’s income-producing machine is a receipt of a capital
        nature."""
        self.add_feedback(message)
        print (message)

    @Rule(Fact(concept='gross_income_capital'), Fact(amount_accrued=True), Fact(amount_received=True) )
    def capital_nature_grossincome(self):
        self.correct = True
        self.rule_fired = True
        
        message = "Student correctly identified the rule: The amount to be brought into gross income is the gross amount accrued or received"
        self.add_feedback(message)
        print (message)


    @Rule(Fact(concept='gross_income_capital'), Fact(amount_accrued='Non'), Fact(amount_received='Non') )
    def capital_nature_grossincome2(self):
        self.correct = True 
        self.rule_fired = True
        
        message= """The student did not correctly identify the rule: The amount to be brought into gross 
        income is the gross amount accrued or received"""
        self.add_feedback(message)
        print (message)
        
    @Rule(Fact(concept='deductions_type_amount'), Fact(type_amount_trade="trade"))
    def deduction_trade_amount(self):
        self.correct = True
        self.rule_fired = True
        
        message= """Student correctly identified the rule: Amounts incurred for the purposes of trade and in the production of income are 
        deductible or deduction is allowed on the expenditure or losses to the extend to which they are
                    incurred for the purpose of trade"""
        self.add_feedback(message)
        print (message)

    @Rule(Fact(concept='deductions_type_amount'), Fact(type_amount_trade="Non"))
    def deduction_trade_amount2(self):
        self.correct = True
        self.rule_fired = True
        
        message= """The student did not correctly identify the rule: 
        Amounts incurred for the purposes of trade and in the production of 
        income are deductible or deduction is allowed on the expenditure or losses to the extend to which they are
                    incurred for the purpose of trade"""
        self.add_feedback(message)
        print (message)
  
    @Rule(Fact(concept='deductions_expenditure_type'), Fact(expenditure_type="voluntary"),  Fact(expenditure_type="loss") )
    def deduction_expenditure(self):
        self.correct = True
        self.rule_fired = True
        
        message= "Student correctly identified the rule: expenditure tends to be voluntary whereas losses tend to be involuntary (joff &CIR)"
        self.add_feedback(message)
        print (message)

    @Rule(Fact(concept='deductions_expenditure_type'), Fact(expenditure_type="Non"),  Fact(expenditure_type="Non") )
    def deduction_expenditure2(self):
        self.correct = True
        self.rule_fired = True
        
        message= """The student did not correctly identify the rule: expenditure tends to be voluntary whereas 
        losses tend to be involuntary (joff &CIR)"""
        self.add_feedback(message)
        print (message)
      
    @Rule(Fact(concept='deductions_expenditure'), Fact(expenditure=True) )
    def deduction_expenditure_condition(self):
        self.correct = True
        self.rule_fired = True
        
        message= "Student correctly identified the rule: expenditure is allowed as a deduction when incurred (sec 15(2)"
        self.add_feedback(message)
        print (message)
         
    @Rule(Fact(concept='deductions_expenditure'), Fact(expenditure="Non") )
    def deduction_expenditure_condition2(self):
        self.correct = True
        self.rule_fired = True
        
        message= "The student did not correctly identify the rule: expenditures are allowed as a deduction when incurred (sec 15(2)"
        self.add_feedback(message)
        print (message)
    
    @Rule(Fact(concept='deductions_type_amount'), Fact(type_amount_deductions="capital"))
    def deduction_type_amount(self):
        self.correct = True
        self.rule_fired = True
        
        message= """Student correctly identified the rule: Expenditure incurred is allowed as a 
        deduction to the extent that its not of capital    nature section 15(2)"""
        self.add_feedback(message)
        print (message)


    @Rule(Fact(concept='deductions_type_amount'), Fact(type_amount_deductions="Non"))
    def deduction_type_amount2(self):
        self.correct = True
        self.rule_fired = True
        
        message= """The student did not correctly identify the rule: Expenditure incurred is allowed as deduction to 
        the extent that its not of capital nature section 15(2)"""
        self.add_feedback(message)
        print (message)

   
    # # Fallback rule that fires if no other rule was triggered
    # def fallback_rule(self):
    #     self.correct = False
        
    #     message= "No specific rule was identified based on the given facts. Please review your inputs."
    #     self.add_feedback(message)
    #     print (message)

    # Override the run method to check if any rule was fired
    # def run(self, *args, **kwargs):
    #     super().run(*args, **kwargs)  # Execute all rules
    #     if not self.rule_fired:  # If no rule was fired, trigger the fallback rule
    #         self.fallback_rule()
    

    @Rule(Fact(concept='vat'), Fact(vat_registration='Non'))
    def registration_non(self):
        self.correct = True
        self.rule_fired = True

        message = "Student identified the rule with non-specific facts."
        self.add_feedback(message)
        print(message)
        
    @Rule(Fact(concept='vat'), Fact(vat_registration='submitt_form'))
    def registration(self):
        self.correct = True
        self.rule_fired = True

        message = """The student did not identify the rule:Imported goods attract Import VAT which increases the output tax. 
                The tax is chargeable to all imported goods that are taxable i.e., standard rated supplies. 
                The identity of the taxpayer acquiring these goods is not the key i.e., 
                it is chargeable whether the taxpayer is a registered operator or not.  
                The time of supply is the time the goods enter Zimbabwe for home consumption. 
                The value of supply is the value for duty purposes plus duty"""
        self.add_feedback(message)
        print(message)
        
    @Rule(Fact(concept='input_tax'), Fact(taxable_supplies='Non'))
    def clained_input_tax_non(self):
        self.correct = True
        self.rule_fired = True
        message = """The student did not identify the rule:Input tax is generally claimed on all goods/services provided 
        they are utilised in the production of taxable supplies. """
        self.add_feedback(message)
        print(message)
        
    @Rule(Fact(concept='input_tax'), Fact(taxable_supplies='True'))
    def clained_input_tax(self):
        self.correct = True
        self.rule_fired = True
        message = "Input tax is generally claimed on all goods/services provided they are utilised in the production of taxable supplies."
        self.add_feedback(message)
        print(message)
        
    
    @Rule(Fact(concept='VAT'), Fact(adjustments='output_vat_adjustment'))
    def value_of_supply(self):
        self.correct = True
        self.rule_fired = True
        message = """where goods were acquired to make taxable supplies and are subsequently utilized to make non-taxable supplies an output VAT adjustment is done."""
        self.add_feedback(message)
        print(message)
        
    @Rule(Fact(concept='VAT'), Fact(fringe_benefits='True'))
    def out_put_tax(self):
        self.correct = True
        self.rule_fired = True
        message = "n employer who provides fringe benefits to employees is deemed to have supplied goods or services on which output tax should be accounted for value of supply will be the value determined"
        self.add_feedback(message)
        print(message)
        
    @Rule(Fact(concept='Vat'), Fact(import_goods='Non'))
    def imported_good_taxation_non(self):
        self.correct = True
        self.rule_fired = True
        message = "Student identified the rule with non-specific facts."
        self.add_feedback(message)
        print(message)
        
    @Rule(Fact(concept='Vat'), Fact(import_goods='True'))
    def imported_good_taxation(self):
        self.correct = True
        self.rule_fired = True
        message = "All imported goods to pay 15% VAT"
        self.add_feedback(message)
        print(message)
        
    @Rule(Fact(concept='VAT'), Fact(rated_supplies='True'))
    def standard_rated_supplies(self):
        self.correct = True
        self.rule_fired = True
        
        message = "Any supply by a registered operator which is not specifically identified as either exempt or zero rated is standard rated. Standard rated supplies attract VAT at a rate of 15%."
        self.add_feedback(message)
        print(message)
        


    @Rule(Fact(concept='VAT'), Fact(supply_of_Goods='True'))
    def imported_goods(self):
        self.correct = True
        self.rule_fired = True
        message = "All imported goods shall be charged 15% VAT"
        self.add_feedback(message)
        print(message)
        
    @Rule(Fact(concept='gross_income'), Fact(accrued='True'))
    def accrued_by_taxpayer(self):
        self.correct = True
        self.rule_fired = True
        message = """Section 8 of the Income Tax Act requires that an amount has to have been received by or accrued
to or in favour of a person for it to be included in Gross Income. an amount received that constitutes a prepayment for goods or
services that will be used or delivered in any subsequent year, shall not form part of gross income
until the goods are delivered or services are performed."""
        self.add_feedback(message)
        print(message)
        
