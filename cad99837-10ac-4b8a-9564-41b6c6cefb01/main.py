from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log

class TradingStrategy(Strategy):

    @property
    def assets        return ["TQQQ"]  # Setting TQQQ as the asset of interest

    @property
    def interval(self):
        return "1day"  # Using daily interval for moving average calculations

    def run(self, data):
        # Fetch the daily closing prices for TQQQ for calculating SMA
        d = data["ohlcv"]  # Access historical OHLCV data

        # Calculate 10-day and 50-day simple moving averages (SMA)
        sma10 = SMA("TQQQ", d, 10)  # 10-day SMA
        sma50 = SMA("TQQQ", d, 50)  # 50-day SMA

        # Initialize allocation with no position
        allocation = {"TQQQ": 0}

        # Check if we have enough data to compute SMAs
        if sma10 is not None and sma50 is not None and len(sma10) > 0 and len(sma50) > 0:
            # Condition to buy: 10-day SMA goes above 50-day SMA
            if sma10[-1] > sma50[-1]:
                allocation["TQQQ"] = 1.0  # Allocate 100% to TQQQ
                log("Buying TQQQ - 10-day SMA is above 50-day SMA")

            # Condition to sell: 10-day SMA drops below 50-day SMA
            elif sma10[-1] < sma50[-1]:
                allocation["TQQQ"] = 0.0  # Sell entire position of TQQQ
                log("Selling TQQQ - 10-day SMA is below 50-day SMA")

        return TargetAllocation(allocation)