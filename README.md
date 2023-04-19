# RealEstate-CashFlow
Script used to compare a potential real estate investment to the opportunity cost of investing the down payment and mortgage payments in the stock market. Will also calculate net cash flow ROIs under different interest rate regimes.

#####Cash Flow Calculator#####
########Jeremy Dawkins########
##############################
#Details
#1) Everything is calculated month by month. Interest is compounded monthly based on the annual rate / 12
#2) Certain values are updates every n months (like appraisal for property tax, or new interest rate or rent increase

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
