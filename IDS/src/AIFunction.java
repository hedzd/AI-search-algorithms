import java.util.Collections;
import java.util.HashMap;

import static java.lang.Double.POSITIVE_INFINITY;
import static java.lang.Double.isFinite;

public class AIFunction {

    public static String[] result = new String[3]; // Result = [Action, Cost, Depth]
    public static Board board = null;

    public static void IDS(Node start, Node goal, Board board) {
        this.board = board;
        int limit = 0;
        Solution solution = null;
        while (solution != Solution.SOLUTION || solution != Solution.FAILURE) {//TODO condition
            DLS(start, goal, limit);
            limit++;
        }
    }

    enum Solution {
        SOLUTION,
        FAILURE,
        CUTOFF
    }

    /**
     * DLS (Depth-Limited Search)
     * This algorithm uses depth-first search with a depth cutoff.
     * Depth at which nodes are not expanded.
     * <p>
     * Three possible results:
     * 1.Solution
     * 2.Failure
     * 3.Cutoff(No solution with cutoff)
     *
     * @param robot Robot's node
     * @param goal  Goal's node
     * @param limit Depth cutoff
     */
    public static Solution DLS(Node robot, Node goal, int limit) {
        boolean cutoffOccurred = false;
        Node child;
        if (limit < 0) return Solution.FAILURE;
        for (int i = 0; i <= limit; i++) {
            if (goal.row == robot.row && goal.col == robot.col) {   // Check if robot is in goal state.
                result[2] = limit + "";
                return Solution.SOLUTION;
            } else if (limit == 0) {    // Check if limit is 0
                return Solution.CUTOFF;
            } else {
                Solution solution = null;
                while (!cutoffOccurred & solution != Solution.FAILURE) {
                    child = successor(robot);
                    if (child == null) return Solution.FAILURE;
                    solution = DLS(child, goal, limit - 1);
                    if (solution == Solution.CUTOFF) cutoffOccurred = true;
                    else if (solution == Solution.FAILURE) return Solution.FAILURE;
                }
            }
        }
        if (cutoffOccurred) return Solution.CUTOFF;
        else return Solution.FAILURE;
    }

    private static Node successor(Node robot) {
        HashMap<Double, String> children = new HashMap<>();

        // East
        children.put(nodeExistence(robot, 0, 1), "R");

        // South
        children.put(nodeExistence(robot, 1, 0), "D");

        // West
        children.put(nodeExistence(robot, 0, -1), "L");

        // North
        children.put(nodeExistence(robot, -1, 0), "U");

        double min = Collections.min(children.keySet()); // Optimal child
        Node child = null;
        if (min != POSITIVE_INFINITY) {
            result[0] += children.get(min); // Updating result
            result[1] = Integer.parseInt(result[1]) + min + "";
            switch (children.get(min)) {
                case "R":
                    child = new Node(robot.row, robot.col + 1);
                    break;
                case "D":
                    child = new Node(robot.row + 1, robot.col);
                    break;
                case "L":
                    child = new Node(robot.row, robot.col - 1);
                    break;
                case "U":
                    child = new Node(robot.row - 1, robot.col);
                    break;
            }
        }
        return child;
    }

    public int compare(double d) {
        if (Double.isFinite(d)) return 1;
        else return 0;
    }

    /**
     * Check the position of the child and to see whether if the child is available.
     *
     * @param robot Robot's node
     * @param i
     * @param j
     * @return int
     */
    public static double nodeExistence(Node robot, int i, int j) {
        double batterySize = POSITIVE_INFINITY;
        String childPosition = (robot.row + i) + "_" + (robot.col + j);
        if (!board.blocks.contains(childPosition))              // If it's not block
            if (board.batteries.containsKey(childPosition))     // If it's in batteries arraylist
                if (!board.butters.contains(childPosition))     // And if it is not butter
                    batterySize = board.batteries.get(childPosition);
        return batterySize;
    }
}

