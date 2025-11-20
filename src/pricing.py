def calculate_flat_bill(load_profile_kwh, price_per_kwh):

    total_energy = sum(load_profile_kwh)
    bill = total_energy * price_per_kwh
    return bill
def apply_tou_tariff(customer_load_profile, peak_price, offpeak_price, peak_hours=None):
    # calculates tou cost for each hour of the load profile
    # param:
    # customer_load_profile: discrete customer usage values (kWh)
    # peak_price: price ($/kWh) during peak hours
    # offpeak_price: price ($/kWh) during all other hours
    # peak_hours=None: if the caller does not provide peak hours, default to none
    # returns a list where each entry is the cost for that time interval

    # peak hours: 5pm to 9pm
    if peak_hours is None:
        peak_hours = [17, 18, 19, 20, 21]    # default peak period
                                                                                        # enumerate is a built in python function that returns
                                                                                        # both the index (hour) and value (usage)
    billed = []  # create empty list to store results

    for hour, usage in enumerate(customer_load_profile):  # loop load profile data
        if hour in peak_hours:                   # check if timestep is within defined peak hours
            billed.append(usage * peak_price)    # if so: apply peak pricing
        else:
            billed.append(usage * offpeak_price) # otherwise: apply off-peak pricing

    return billed            # return a list with the cost for each time interval


def apply_reform_tariff(customer_load_profile, system_load_profile, tiers):

    # 3 level inverse capacity factor tou tariff
    # param
    # customer_load_profile: discrete customer usage values (kWh)
    # system_load_profile: list of hourly system demand values (MW or relative index)
    # tiers: list of dicts with keys {threshold, price}

    billed = []     # create empty list to store results

    for hour, usage in enumerate(customer_load_profile):      # loop load profile data
        system_load = system_load_profile[hour]               # determine grid load at each timestep

        # determine which tier applies
        applicable_price = None                       # initialise the variable (no data yet)
        for tier in tiers:                            # loop through tiers
            if system_load <= tier["threshold"]:      # determine if the grid load for this timestep is below or equal to this tier's threshold
                applicable_price = tier["price"]      # if so, apply this tier; otherwise check the next tier. Store the matching price (applicable_price)
                break                                 # stop loop, correct tier found

        # if system load exceeds all thresholds, use highest tier
        if applicable_price is None:
            applicable_price = tiers[-1]["price"]        # tiers[-1] refers to the last tier in the list which has the highest price

        billed.append(usage * applicable_price)          # calculate and store hourly cost

    return billed                                        # return a list of costs for each time interval
