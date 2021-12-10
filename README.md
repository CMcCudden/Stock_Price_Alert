Using the Alpha Vantage API, the program compares yesterday's and the day before's closing prices of a given stock. In 
this case, the company is Tesla/ TSLA. 

Whenever a percent change of +/- 5% is detected, I'd receive 3 texts from Twilio- alerting me of the change in price as well as
linking me 3 recent articles relating to the company (using NEWS API). With the way it's currently written, it could be 
repurposed for essentially any publicly traded asset.