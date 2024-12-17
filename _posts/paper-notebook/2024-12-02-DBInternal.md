# Structure

1. `tcop` (Top-level Control Program) 

2. **`postgres.c`**: main entry point for query execution. It handles the query lifecycle:
   accepts the query from the client (via the frontend-backend protocol), and coordinates the entire process:
   - Parses the query using the parser.
   - Uses the planner to generate an execution plan.
   - Sends the plan to the executor for actual execution.
   - Returns the results to the client.

# Some important variables

A `QueryDesc` structure represents the state and details of the query being executed. It contains information like the query **plan, execution context, snapshots, and parameters.**

