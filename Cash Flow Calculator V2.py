#####Cash Flow Calculator#####
########Jeremy Dawkins########
##############################
#Details
#1) Everything is calculated month by month. Interest is compounded monthly based on the annual rate / 12
#2) Certain values are updates every n months (like appraisal for property tax, or new interest rate or rent increase
#3)

#Interpretation:
#-Top left graph: shows cumulative amount you will have spent on interest, property tax and your principal
#over the entire loan term

#-Top right graph: shows your monthly mortgage payments (including property tax) and your tenant income. Also
#shows the difference of the two which represents cash flow. If net cash flow is positive, you are making money
#every month. Cash flow should be positive each month in a good property. Shaded black area shows what ROIs
#would be from the min interest rate to max interest rate selected.

#-Bottom left graph: shows cumulative returns in cash flow vs cumulative returns if you had invested the down
#payment + fees + renovation costs. This is misleading because you are also getting "free" equity in the home
#from the principal being paid off AND increase in home value. The last line represents the monthly cash flow +
#the gain in equity. An amazing investment has cash flow beating market returns. This will be rare. At a minimum,
#cash flow + total equity built must be larger than stock returns. This does NOT include tax effects, which will
#favour the house in the case your stocks are in a taxable account. Finally, the model does NOT consider
#continued monthly investments into the market. This would give extra compounding interest. Instead,
#the total equity + cash flow line somewhat takes this into consideration by substracting the amounts invested
#in the house from the profits of that invest. It is possible to factor in erosion of the market returns
#from having to pay rent (which the homeowner does not have to pay) by changing houseType to 'home'.
#Shaded green area shows total equity + cash flow from the min interest to max interest environments

#-Bottom right graph: show the return on investment relative to the total cash invested (down payment,
#fees and renovations). This is calculated as an annual % (i.e what percentage of the total cash
#invested would you gain per year given the returns of that month). A great property has 10-15%
#initial ROI, but this will fluctuate with rent, interest and property tax increase/decrease.
#This is compared to the ROI for the market (so % of total cash invested that the market would
#return in one year based on the profits (price increase) made that month MINUS the fund erosion
#from paying rent when the homeowner doesn't have that expense. Also added is the
#ROI calculated with the additional 'income' in the form of total equity in home, even if this
#is not liquid. Home equity is ownership % * current price Ideally the cash flow ROI beats the market ROI.


#import packages
import numpy as np
import scipy
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.cm as cm

class Main:
	#parameters
	# mortgage params
	houseType = 'investment' #investment or home. If only an investment, I don't substract rent from the market returns.
	interestRateIncrease = 0 / 100 / 12 #Calculate a fluctuating interest rate
	priceInitial = 1000000
	appreciation = 5 / 100 #amount house appreciates per year. Influences property tax paid.
	downPayment = 20/100
	loanTerm = 30
	propertyTax = 0.85/100
	propertyTaxIncreaseTerm = 36 #after how many months are property taxes increased
	principalInitial = (1-downPayment) * priceInitial
	purchasingFees = 15000 #misc fees for lawyers, eskrows, land transfer tax, inspections etc. This affects ROI
	totalCash = downPayment * priceInitial + purchasingFees
	marketReturn = 7 / 100 #assumed yearly return from market investment of downpayment + fees
	interestRateTerm = 60 #in how many months do interest rates change
	# rental params
	numUnits = 3 #number of units that are rentable
	rentalPrice = 1200 #dollars per unit
	rentalIncrease = 2 / 100 #amount rent increased per year both for tenants and for the renting scenario
	rentalIncomeInitial = numUnits * rentalPrice
	rentalIncreaseTerm = 12 #how many months before you increase rent or rent is increased on you
	rentErosionInitial = 1050 #amount you would otherwise pay on rent per month
	# monthly params
	monthlyLoanTerm = loanTerm * 12
	monthlyMarketReturn = marketReturn / 12
	monthlyAppreciation = appreciation / 12


	#calculate mortgage payment and total payment including  property tax payment
	def mortgage_payment(self, principal, monthlyInterestRate, monthlyLoanTerm, propertyTax, priceAppraised):
		mortgagePaymentCoefficient = ((monthlyInterestRate)*(1+monthlyInterestRate) ** monthlyLoanTerm) / (((1+monthlyInterestRate) ** monthlyLoanTerm) - 1)
		mortgagePayment = principal * mortgagePaymentCoefficient
		propertyTaxPayment = ((propertyTax * priceAppraised) / 12) # factor in the appraised price appreciation's influence on property tax
		totalPayment = mortgagePayment + propertyTaxPayment  #include property tax payments
		return mortgagePayment, totalPayment #Monthly payment due on mortgage and total payment due (with property tax)

	def monthly_calculation(self, interestRate): #run loan calculation for each month in loan term
		self.monthlyInterestRate = interestRate / 12
		self.result = []
		self.price = self.priceInitial #Actual price used to calculate your total equity
		self.priceAppraised = self.priceInitial #Appraised price (only re-appraised every few years)
		self.rentErosion = self.rentErosionInitial
		self.rentalIncome = self.rentalIncomeInitial
		self.principal = self.principalInitial

		for month in range(self.monthlyLoanTerm, 0, -1): #calculate payment for each month during term
			if month in range(self.monthlyLoanTerm, 0, -self.interestRateTerm)[1:]: #every 5 years increase interest rate. [1:] ignores the first mont
				self.monthlyInterestRate = self.monthlyInterestRate + self.interestRateIncrease
			if month in range(self.monthlyLoanTerm, 0, -self.rentalIncreaseTerm)[1:]: #every 1 year increase the rent. [1:] ignores the first mont
				self.rentalIncome = self.rentalIncome * (1 + self.rentalIncrease)
				self.rentErosion = self.rentErosion * (1 + self.rentalIncrease)
			if month in range(self.monthlyLoanTerm, 0, -self.propertyTaxIncreaseTerm)[1:]: #every 3 years increase the property tax. [1:] ignores the first month
				self.priceAppraised = self.price # Update the appraisal price to factor in the price appreciation's influence on property tax
			else:
				pass
			self.mortgagePayment, self.totalPayment = self.mortgage_payment(self.principal, self.monthlyInterestRate, month, self.propertyTax, self.priceAppraised)
			self.principalPaid = self.mortgagePayment - (self.principal * self.monthlyInterestRate)
			self.principal = self.principal - self.principalPaid
			self.opportunityCostCumulative = (self.totalCash * (1 + self.monthlyMarketReturn) ** (self.monthlyLoanTerm - month)) - self.totalCash # Calculate cumulative market returns (just the profit) if you had invested the downpayment and fees
			self.opportunityCost = self.opportunityCostCumulative - ((self.totalCash * (1 + self.monthlyMarketReturn) ** (self.monthlyLoanTerm - month - 1)) - self.totalCash) #substract previous month to get only the monthly profit (non-cumulative)
			self.result.append((self.mortgagePayment, self.totalPayment, self.principalPaid, self.principal, self.rentalIncome, self.opportunityCost, self.price, self.rentErosion))
			self.price = self.price * (1 + self.monthlyAppreciation)  # factor in the price appreciation

		#Get results in separate lists
		self.mortgagePaymentResults, self.totalPaymentResults, self.principalPaidResults, self.principalResults, self.rentalIncomeResults, self.opportunityCostResults, self.priceResults, self.rentErosionResults = \
			[i[0] for i in self.result], \
			[i[1] for i in self.result], \
			[i[2] for i in self.result], \
			[i[3] for i in self.result], \
			[i[4] for i in self.result], \
			[i[5] for i in self.result], \
			[i[6] for i in self.result], \
			[i[7] for i in self.result]

		self.interestPaidResults = np.array(self.mortgagePaymentResults) - np.array(self.principalPaidResults)
		self.netCashFlow = np.array(self.rentalIncomeResults) - np.array(self.totalPaymentResults) #Net income (or payment) due/received per month
		if self.houseType == 'home':
			self.netOpportunityCostResults = np.array(self.opportunityCostResults) - np.array(self.rentErosionResults) #Get net monthly market returns by substracting what you have to pay in rent
		if self.houseType == 'investment':
			self.netOpportunityCostResults = np.array(self.opportunityCostResults) #If its an investment, don't substract rent because both parties will be paying rent

		#Get cumulative sums of results
		self.mortgagePaymentCumSum, self.totalPaymentCumSum, self.principalPaidCumSum, self.interestPaidCumSum, self.netOpportunityCostCumSum = \
			np.cumsum(np.array(self.mortgagePaymentResults)), \
			np.cumsum(np.array(self.totalPaymentResults)), \
			np.cumsum(np.array(self.principalPaidResults)), \
			np.cumsum(np.array(self.interestPaidResults)), \
			np.cumsum(np.array(self.netOpportunityCostResults))

		self.totalPropertyTaxCumSum = self.totalPaymentCumSum - self.mortgagePaymentCumSum #Cumulative sum of property tax paid per month
		self.netCashFlowCumSum = np.cumsum(self.netCashFlow) #Cumulative sum of net income (or payment) due/received per month
		self.homeOwnership = (self.principalPaidCumSum + (self.downPayment * self.priceInitial)) / self.priceInitial #percentage of home that is owned based on % principal paid off. Includes down payment
		self.homeEquityCumSum = (self.homeOwnership * self.priceResults) - (self.downPayment * self.priceInitial)  #this is the fraction of the home owned times the current price as per that month minus the down payment you contributed. Current value of equity at month n.
		self.homeEquityGained = np.diff(np.insert(self.homeEquityCumSum, 0, 0)) #this the amount of home equity $ you have gained per month. Counts as income for ROI calculation. Taken as delta of Equity cumulative sum so I add a 0 value in beginning to get correct values.
		self.netCashFlowAndEquityCumSum = self.homeEquityCumSum + self.netCashFlowCumSum #Cumulative sum of net income + monthly added house equity based on current valuation
		self.netCashFlowAndEquity = self.netCashFlow + self.homeEquityGained

		#Calculate ROIs (for real estate and for similar market investment)
		self.ROIrealestate = ((self.netCashFlow * 12) / self.totalCash) * 100 #calculate annual cash on cash ROI (%) for monthly house income relative to initial payment
		self.ROIrealestateWithEquity = (((self.netCashFlowAndEquity) * 12) / self.totalCash) * 100 # includes the equity that is being paid in by tenants
		self.ROImarket = ((np.array(self.netOpportunityCostResults) * 12) / self.totalCash) * 100 #calculate annual cash on cash ROI (%) for monthly market return relative to initial payment

		return self.ROIrealestate, self.netCashFlow, self.netCashFlowAndEquityCumSum

	def plot_results(self):
		#Plot results
		## Setup Figure
		fig, ((axCumPaid, self.axPayments), (self.axOpportunityCost, self.axROI)) = plt.subplots(2, 2, sharex=True)
		self.months = range(self.monthlyLoanTerm)

		## Cumulative payments plot
		axCumPaid.plot(self.months, self.totalPaymentCumSum, 'k-', linewidth = 3)
		axCumPaid.plot(self.months, self.principalPaidCumSum, 'g-', linewidth = 3)
		axCumPaid.plot(self.months, self.interestPaidCumSum, 'm-', linewidth = 3)
		axCumPaid.plot(self.months, self.totalPropertyTaxCumSum, 'r-', linewidth = 3)
		## Mortgage payments plot
		self.axPayments.plot(self.months, self.totalPaymentResults, 'r-', linewidth = 3)
		self.axPayments.plot(self.months, self.rentalIncomeResults, 'g-', linewidth = 3)
		self.axPayments.plot(self.months, self.netCashFlow, 'k-', linewidth = 3)
		self.axPayments.axhline(0, color='r', linestyle='--')
		## Opportunity cost plot (relative to expected market returns)
		self.axOpportunityCost.plot(self.months, self.netCashFlowCumSum, 'k-', linewidth = 3) #cumulative liquid profits (cash) received per month.
		self.axOpportunityCost.plot(self.months, self.netCashFlowAndEquityCumSum, 'g-', linewidth = 3) #includes home equity. Pertinent because tenants are paying your mortgage which is $ that must be accounted for
		self.axOpportunityCost.plot(self.months, self.netOpportunityCostCumSum, 'r--', linewidth = 3) #cumulative monthly profit made from stock market investment
		self.axOpportunityCost.axhline(self.totalCash, color = 'r', linestyle = '--') #Total initial investment reference
		## Return of investment (% cash on cash)
		self.axROI.plot(self.months, self.ROIrealestate, 'g-', linewidth = 3)
		#axROI.plot(months, ROIrealestateWithEquity, 'g-', linewidth = 3)
		self.axROI.plot(self.months, self.ROImarket, 'r--', linewidth = 3) #reference line for market ROI
		self.axROI.axhline(0, color='r', linestyle = '--') #reference line for market ROI

		# Format plot
		## Cumulative amounts format
		axCumPaid.set_title('Cumulative Amount Paid for Property')
		legend1 = ['Total Paid', 'Principal Paid', 'Interest Paid', 'Property Tax Paid']
		axCumPaid.set_ylabel('Dollars ($)', fontsize = 22)
		axCumPaid.tick_params(axis='both', labelsize=16)
		## Monthly payments format
		self.axPayments.set_title('Cash Flow Analysis (in $/month)')
		legend2 = ['Total Owed Monthly', 'Paid by Tenants', 'Net Cash Flow']
		self.axPayments.set_ylabel('Dollars ($)', fontsize = 22)
		self.axPayments.tick_params(axis='both', labelsize=16)
		## Opportunity cost format
		self.axOpportunityCost.set_title('Opportunity Cost vs. Downpayment Market Returns')
		legend3 = ['Cumulative Net Cash Flow', 'Cumulative Net Cash Flow + Home Equity', 'Cumulative Market Returns - Rent)', 'Initial Investment']
		self.axOpportunityCost.set_ylabel('Dollars ($)', fontsize = 22)
		self.axOpportunityCost.set_xlabel('Months Since Purchase', fontsize = 22)
		self.axOpportunityCost.tick_params(axis='both', labelsize=16)
		## ROI format
		self.axROI.set_title('Cash Flow Analysis (in % Return Relative to Initial Investment)')
		legend4 = ['Annual % Return', 'Annual % Return Including Equity', 'Annual % Return on Market - Rent']
		self.axROI.set_ylabel('Monthly Return on Investment (%)', fontsize = 22)
		self.axROI.set_xlabel('Months Since Purchase', fontsize = 22)
		self.axROI.tick_params(axis='both', labelsize=16)


		## Change legend depending on investment type
		if self.houseType == 'home':
			legend3 = ['Cumulative Net Cash Flow', 'Cumulative Net Cash Flow + Home Equity', 'Cumulative Market Returns - Rent)', 'Initial Investment']
			legend4 = ['Annual % Return on Cash Flow', 'Annual % Return on Market - Rent']
		if self.houseType == 'investment':
			legend3 = ['Cumulative Net Cash Flow', 'Cumulative Net Cash Flow + Home Equity', 'Cumulative Market Returns)', 'Initial Investment']
			legend4 = ['Annual % Return on Cash Flow', 'Annual % Return on Market']

		## Set legends
		axCumPaid.legend(legend1)
		self.axPayments.legend(legend2)
		self.axOpportunityCost.legend(legend3)
		self.axROI.legend(legend4)
		## adjust plots
		fig.subplots_adjust(hspace=0.2, wspace=0.23)
		#fig.tight_layout()

	def plot_cash_flow_range(self, colour):
		## Return of investment (% cash on cash)
		#self.axROI.plot(self.months, self.ROIrealestate, color=colour, linewidth = 3)
		#axROI.plot(months, ROIrealestateWithEquity, 'g-', linewidth = 3)
		ROImin, cashFlowmin, cashFlowCumSummin = m.monthly_calculation(interestRateMin)
		ROImax, cashFlowmax, cashFlowCumSummax = m.monthly_calculation(interestRateMax)
		self.axROI.fill_between(x = self.months, y1 = ROImin, y2 = ROImax, alpha=0.3, facecolor='g')
		self.axPayments.fill_between(x=self.months, y1=cashFlowmin, y2=cashFlowmax, alpha=0.3, facecolor='k')
		self.axOpportunityCost.fill_between(x=self.months, y1=cashFlowCumSummin, y2=cashFlowCumSummax, alpha=0.3, facecolor='g')

# Choose interest rates and # of curves
interestRateMin, interestRateMax, curveNum = 2 / 100, 7 / 100, 20 #interestRateMin is plotted, values up to max are shaded
interestRange = np.linspace(interestRateMin, interestRateMax, curveNum)  # List of interest rates to plot
# Choose colors
#colour_subsection = np.linspace(0.1, 0.9,curveNum)  # Splits colourmap an equal # of sections related to # of curves
#coloursList = [cm.spring_r(x) for x in colour_subsection]

m = Main()
m.monthly_calculation(interestRateMin)
m.plot_results()
m.plot_cash_flow_range(colour='g')


plt.show()