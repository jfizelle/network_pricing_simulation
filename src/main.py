from src.config_loader import load_config
from src.pricing import calculate_flat_bill
from src.pricing import apply_tou_tariff, apply_reform_tariff

def main():
    config = load_config("config/base_config.yaml")             # load param

    example_load_profile = [1.0] * 24                           # example load profile

    system_load_profile = [                                     # example load profile for 3 tier tariff
        40, 45, 48, 50, 55, 60, 65, 70, 80, 85, 90, 95,
        40, 45, 48, 50, 55, 60, 65, 70, 80, 85, 90, 95
    ]

    # flat tariff
    flat_price = config["tariffs"]["baseline_flat"]["price"]                # get flat price from config
    flat_bill = calculate_flat_bill(example_load_profile, flat_price)       # compute cost under flat tariff

    # tou tariff
    tou_config = config["tariffs"]["baseline_tou"]                          # get tou prices from config
    tou_costs = apply_tou_tariff(                                           # compute tou cost for each hour of the profile
        example_load_profile,
        tou_config["peak_price"],
        tou_config["offpeak_price"]
    )
    tou_bill = sum(tou_costs)                                               # sum to get total tou bill

    # 3 tier tariff
    reform_config = config["tariffs"]["reform_capacity_tiers"]              # load 3 tier tariff from config
    tiers = reform_config["tiers"]                                          # get list of tier thresholds and prices

    reform_costs = apply_reform_tariff(                                     # compute hourly cost of 3 tier tariff
        example_load_profile,
        system_load_profile,                                                # system wide load determines which tier applies
        tiers                                                               # pricing rules based on system load thresholds
    )

    reform_bill = sum(reform_costs)                                         # total cost under 3 tier tariff


    print("\n=== BILL RESULTS ===")
    print("Flat tariff bill:", flat_bill)
    print("TOU tariff bill:", tou_bill)
    print(f"Reform tariff bill (3-tier): ${reform_bill:.2f}")
    print("====================\n")

if __name__ == "__main__":                      # ensures main() is only run when script is executed directly
    main()                                      # run the main script
