from flask import Flask, request, jsonify
from jug_riddle import JugRiddle, solve, UnsolvableRiddle

app = Flask(__name__)


@app.get("/solve")
def solve_water_jug():
    """
    Automatic solver for the Water Jug Riddle.

    This endpoint takes three parameters from the query string:
    - jug1_capacity (int): The capacity of the first jug.
    - jug2_capacity (int): The capacity of the second jug.
    - goal (int): The desired amount of water to measure in one of the jugs.

    Returns:
    - JSON response containing the solution steps if solvable or indicating 'Unsolvable'
      if the riddle cannot be solved.

    Example:
    GET /solve?jug1_capacity=3&jug2_capacity=2&goal=1

    Response:
    {
        "response": [
            {"jug": "Jug1", "action": "FILL"},
            {"jug": "Jug2", "action": "TRANSFER"},
            {"jug": "Jug2", "action": "EMPTY"}
        ],
        "status": "Solved"
    }

    If the riddle is unsolvable, the 'status' field will be 'Unsolvable'.

    Raises:
    - BadRequest: If the parameters are missing or not valid integers.
    """
    try:
        # Get parameters from the query string
        jug1_capacity = int(request.args.get("jug1_capacity"))
        jug2_capacity = int(request.args.get("jug2_capacity"))
        goal = int(request.args.get("goal"))
    except Exception as e:
        return jsonify({"error": str(e)})

    riddle = JugRiddle(jug1_capacity, jug2_capacity, goal)
    try:
        riddle = solve(riddle)
    except UnsolvableRiddle:
        ret = "Unsolvable Riddle"
        status = "Unsolvable"
    else:
        ret = []
        for action, jug in riddle._actions:
            ret.append({"jug": jug.value, "action": action.name})
        status = "Solved"

    return jsonify({"response": ret, "status": status})


def run_flask_app():
    app.run(host="0.0.0.0", port=5000)



