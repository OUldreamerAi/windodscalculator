from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML = """
<h2>Win Chance Calculator for Scarp</h2>

<form method="post">
    Item cost: <input type="number" step="any" name="item_cost" required><br><br>
    Upgrade cost: <input type="number" step="any" name="upgrade_cost" required><br><br>
    Likelihood of winning (%): <input type="number" step="any" name="likelihood" required><br><br>
    Upgrade increase (% per upgrade): <input type="number" step="any" name="upgrade_amount" required><br><br>
    Hours coded: <input type="number" step="any" name="coded_hours" required><br><br>
    Project tier multiplier: <input type="number" step="any" name="project_tier" required><br><br>
    <input type="submit" value="Calculate">
</form>

{% if results %}
<hr>
<h3>Results</h3>
<p>Total scrap amount: {{ results.scrap_amount }}</p>
<pre>{{ results.iterations }}</pre>
<p><strong>Overall win chance (combined): {{ results.overall_win_chance }}%</strong></p>
<p>Remaining scraps: {{ results.remaining_scraps }}</p>
{% endif %}
"""

@app.route("/", methods=["GET", "POST"])
def home():
    results = None

    if request.method == "POST":
        item_cost = float(request.form["item_cost"])
        upgrade_cost = float(request.form["upgrade_cost"])
        likelihood = float(request.form["likelihood"])
        upgrade_amount = float(request.form["upgrade_amount"])
        coded_hours = float(request.form["coded_hours"])
        project_tier = float(request.form["project_tier"])

        scrap_amount = coded_hours * 1.618033988749 * 10 * project_tier

        iteration = 1
        remaining_scraps = scrap_amount
        overall_lose_chance = 1.0
        iteration_output = ""

        while remaining_scraps >= item_cost:
            remaining_scraps -= item_cost

            upgrade_count = int(remaining_scraps / upgrade_cost)
            iteration_win_chance = likelihood + (upgrade_count * upgrade_amount)

            # Prevent going over 100%
            iteration_win_chance = min(iteration_win_chance, 100)

            iteration_lose_chance = (100 - iteration_win_chance) / 100
            overall_lose_chance *= iteration_lose_chance

            iteration_output += (
                f"Iteration {iteration}: "
                f"{upgrade_count} upgrades → "
                f"{iteration_win_chance}% win chance this round\n"
            )

            iteration += 1

        overall_win_chance = (1 - overall_lose_chance) * 100

        results = {
            "scrap_amount": round(scrap_amount, 2),
            "iterations": iteration_output,
            "overall_win_chance": round(overall_win_chance, 2),
            "remaining_scraps": round(remaining_scraps, 2)
        }

    return render_template_string(HTML, results=results)

application = app

