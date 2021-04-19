import java.util.ArrayList;
import java.util.HashMap;

public class AIFunction {

    public static String[] result = new String[3];

    public static void IDS(Node start, Node goal, Board board) {
        int limit = 0;
        Solution solution =null;
        while (solution!=Solution.SOLUTION || solution!=Solution.FAILURE) {
            DLS(start, goal, limit, board);
            limit++;
        }
    }

    enum Solution {
        SOLUTION,
        FAILURE,
        CUTOFF
    }

    /**
     * DLS _ Depth-Limited Search
     * This algorithm uses depth-first search with a depth cutoff.
     * Depth at which nodes are  not expanded.
     * <p>
     * Three possible results:
     * 1.Solution
     * 2.Failure
     * 3.Cutoff(No solution with cutoff)
     *
     * @param start
     * @param goal
     * @param limit
     */
    public static Solution DLS(Node start, Node goal, int limit, Board board) {
        Solution solution = null;
        Node child;

        for (int i = 0; i < limit; i++) {
            if (goal.row == start.row && goal.col == start.col) {   // Check if robot is in goal state.
                result[2] = limit + "";
                return Solution.SOLUTION;
            } else if (limit == 0) {    // Check if limit is 0
                return Solution.CUTOFF;
            } else {
                boolean cutoffOccurred = false;
                while (!cutoffOccurred & solution != Solution.FAILURE) {
                    child = successor(start, board);
                }
            }
        }
    }

    private static Node successor(Node start, Board board) {
        double min = Double.POSITIVE_INFINITY;
        for (int i = -1; i <= 1; i++) {
            if (board.batteries.containsKey(start.row + "_" + (start.col - 1))) {
                min = board.batteries.get((start.row + "_" + (start.col - 1))); // East
            }
        }
//TODO Node existence : another function for each node

    }
}

