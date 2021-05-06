import java.net.Socket;
import java.util.*;

public class AIFunction {
/*    enum Solution {
        SOLUTION,
        FAILURE,
        CUTOFF,
        DUPLICATE
    }*/

    public static void searchAlgorithm(Board board) {
        Solution solution = null;
        for (int i = 0; i < board.butters.size(); i++) {
            solution = IDSNavigate(board);
            if (solution.statues == "SOLUTION") {
                System.out.println(solution.getBoard().movement + "\n" + (solution.getBoard().movement.length() + 1) + "\n" + solution.getBoard().movement.length());
                clearButter(solution.getBoard());
                board = solution.getBoard();
            } else System.out.println("Can't pass the butter!");
            //printResult(solution, actions, depth);
        }
    }

    private static Solution IDSNavigate(Board board) {
        int limit = -1;
        Solution solution = null;
        do {
            ArrayList<String> explored = new ArrayList<>();
            limit++;
            solution = DLS(board.clone(), limit, board.robot, "", explored);
        } while ((solution.statues != "SOLUTION" || solution.statues != "FAILURE"));
        return solution;
    }

    private static void clearButter(Board board) {
        for (String eachButter : board.butters) {
            if (board.persons.contains(eachButter)) {
                board.persons.remove(eachButter);
                board.butters.remove(eachButter);
                return;
            }
        }
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
     * @param limit Depth cutoff
     * @param board
     */
    public static Solution DLS(Board board, int limit, Node robotMove, String direction, ArrayList<String> explored) {
        Solution solution = new Solution();
        solution.setBoard(board);
        if (explored.contains(robotMove.toString())) {
            solution.statues = "DUPLICATE";
            return solution;
        }
        board.robot = robotMove;
        if (board.butters.contains(board.robot.toString())) {
            board.butters.set(board.butters.indexOf(board.robot.toString()), move(board.robot.toString(), direction));
        }
        explored.add(robotMove.toString());
        boolean cutoffOccurred = false;
        boolean duplicateOccurred = false;
        if (limit < 0) {
            solution.statues = "FAILURE";
            return solution;
        }
        if (positionMatch(board.persons, board.butters)) {
            solution.statues = "SOLUTION";
            return solution;
        }
        if (limit == 0) {      // Check if limit is 0
            solution.statues = "CUTOFF";
            return solution;
        } else {
            HashMap<Node, String> frontier = new HashMap<>();

            if (isMoveAllowed(board, board.robot.toString(), "R"))
                frontier.put(new Node(board.robot.row + 0, board.robot.col + 1), "R");
            if (isMoveAllowed(board, board.robot.toString(), "U"))
                frontier.put(new Node(board.robot.row - 1, board.robot.col + 0), "U");
            if (isMoveAllowed(board, board.robot.toString(), "L"))
                frontier.put(new Node(board.robot.row + 0, board.robot.col - 1), "L");
            if (isMoveAllowed(board, board.robot.toString(), "D"))
                frontier.put(new Node(board.robot.row + 1, board.robot.col + 0), "D");

            for (Node child : frontier.keySet()) {
                if (child == null) {
                    solution.statues = "FAILURE";
                    return solution;
                }
                solution = DLS(board.clone(), limit - 1, child, frontier.get(child),explored);
                if (solution.statues == "CUTOFF") cutoffOccurred = true;
                else if (solution.statues == "DUPLICATE") duplicateOccurred = true;
                else if (solution.statues != "FAILURE") {
                    board.movement += frontier.get(child);
                    return solution;
                }
            }
        }

        if (cutoffOccurred) {
            solution.statues = "CUTOFF";
            return solution;
        } else if (duplicateOccurred) {
            solution.statues = "DUPLICATE";
            return solution;
        } else {
            solution.statues = "FAILURE";
            return solution;
        }
    }


    private static boolean positionMatch(ArrayList<String> persons, ArrayList<String> butters) {
        for (String eachButter : butters) {
            if (persons.contains(eachButter)) {
                return true;
            }
        }
        return false;
    }


    private static boolean isMoveAllowed(Board board, String target, String direction) {
        return isMoveAllowed(board, target, direction, 0);
    }

    private static boolean isMoveAllowed(Board board, String target, String direction, int limit) {
        String childPosition = move(target, direction);
        if (!board.blocks.contains(childPosition))           // If it's not block
            if (board.batteries.containsKey(childPosition))     // If it's in batteries arraylist
                if (board.butters.contains(childPosition)) {
                    if (limit >= 2) return false;
                    return isMoveAllowed(board, childPosition, direction, limit + 1);
                } else return true;
        return false;
    }

    private static String move(String target, String direction) {
        int column = 0, row = 0;
        switch (direction.toUpperCase()) {
            case "R":
                column = 1;
                row = 0;
                break;
            case "U":
                column = 0;
                row = -1;
                break;
            case "L":
                column = -1;
                row = 0;
                break;
            case "D":
                column = 0;
                row = 1;
                break;
        }
        String[] splittedPosition = target.split("_");
        return (Integer.parseInt(splittedPosition[0]) + column) + "_" + (Integer.parseInt(splittedPosition[1])  + row);
    }

}

