FASTBOX DELIVERY SYSTEM - PYTHON ASSIGNMENT

FILES
-----
main.py          Main Python program
data.json        Main/base input file
test_case_*.json Additional test files
report.json      Created automatically after running the program

HOW TO RUN
----------
1. Open the project folder in VS Code.
2. Open Terminal.
3. Run:

   python main.py

4. To run a test case:

   python main.py test_case_1.json

5. Check report.json after every run.

MAIN LOGIC
----------
1. Read JSON input.
2. Calculate Euclidean distance.
3. Find the nearest agent for each package warehouse.
4. Calculate agent-to-warehouse distance.
5. Calculate warehouse-to-destination distance.
6. Add both distances to the agent's total.
7. Efficiency = total distance / delivered packages.
8. Agent with lowest efficiency is selected as best_agent.
9. Save final output in report.json.
