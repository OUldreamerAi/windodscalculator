print("Win Chance Calculator")

item_cost = float(input("Item cost: "))
upgrade_cost = float(input("Upgrade cost: "))
likelihood = float(input("Likelihood of winning (%): "))
upgrade_amount = float(input("By how many percentage does buying the upgrade increase the odds of winning: "))
coded_hours = float(input("How many hours have you coded: "))
project_tier = float(input("What tier is your project tier multiplier: "))


scrap_amount = coded_hours * 1.618033988749 * 10 * project_tier
print(f"\nTotal scrap amount: {scrap_amount}")

iteration = 1
remaining_scraps = scrap_amount
overall_lose_chance = 1.0  

while remaining_scraps >= item_cost:

    remaining_scraps -= item_cost
    
    upgrade_count = int(remaining_scraps / upgrade_cost)
    
    iteration_win_chance = likelihood + (upgrade_count * upgrade_amount)
    iteration_lose_chance = (100 - iteration_win_chance) / 100
    
    overall_lose_chance *= iteration_lose_chance
    
    print(f"Iteration {iteration}: Bought item (-{item_cost} scraps), {upgrade_count} upgrades → {iteration_win_chance}% win chance this round")
    
    iteration += 1

overall_win_chance = (1 - overall_lose_chance) * 100

print(f"\nOverall win chance (combined): {overall_win_chance}%")
print(f"Remaining scraps: {remaining_scraps}")