import java.util.*;

public class AIFunction {
    public static long expand = 0, generate = 0, depth = 0;
    public static ArrayList<String> history = new ArrayList<>();

    /**
     * Repeat the IDS function for number of butters.
     *
     * @param board
     */
    public static Main.Statistics searchAlgorithm(Board board) {
        Result solution = null;
        Main.Statistics statistics = new Main.Statistics();
        int number = board.butters.size();
        for (int i = 0; i < number; i++) {
            board.explored = new ArrayList<>();
            solution = IDSNavigate(board);
            if (solution.statues == Result.Solution.SUCCESS) {
                System.out.println(solution.movement + "\n" + (solution.movement.replaceAll("\\s+", "").length() + 1) + "\n" + solution.movement.replaceAll("\\s+", "").length());
                clearButter(solution.getBoard());
                board = solution.getBoard();
            } else System.out.println("Can't pass the butter!");
        }
        statistics.expandedNode = generate;
        statistics.generatedNode = expand;
        statistics.depth = depth;
        return statistics;
    }

    /**
     * Repeat DLS algorithm until it reaches success or failure!
     *
     * @param board
     * @return
     */
    private static Result IDSNavigate(Board board) {
        int limit = -1;
        Result solution = null;
        do {
            //ArrayList<String> explored = new ArrayList<>();
            limit++;
            Board tempBoard = board.clone();
            solution = DLS(tempBoard, limit, board.robot, "");
            //if (solution.statues.equals("CUTOFF")) System.out.println(limit+": "+board.explored);
        } while (solution.statues.equals(Result.Solution.CUTOFF));
        depth += limit;
        return solution;
    }

    /**
     * Delete visited butters and persons!
     *
     * @param board
     */
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
     * Four possible results:
     * 1.Solution
     * 2.Failure
     * 3.Cutoff(No solution with cutoff)
     * 4.Duplicate
     *
     * @param board
     * @param limit
     * @param robotMove
     * @param direction
     * @return
     */
    public static Result DLS(Board board, int limit, Node robotMove, String direction) {
        expand++;
        Result solution = new Result();
        solution.setBoard(board);
        if (board.explored.contains(robotMove.toString())) {
            solution.statues = Result.Solution.DUPLICATE;
            return solution;
        }
        board.robot = robotMove;
        if (board.butters.contains(board.robot.toString())) {
            int index = board.butters.indexOf(board.robot.toString());
            board.butters.set(index, move(board.robot.toString(), direction));
            if (positionMatch(board.persons, board.butters)) {
                solution.statues = Result.Solution.SUCCESS;
                return solution;
            }
            if (!isMoveAllowed(board, board.butters.get(index), "U") || !isMoveAllowed(board, board.butters.get(index), "D")) {
                if (!isMoveAllowed(board, board.butters.get(index), "R") || !isMoveAllowed(board, board.butters.get(index), "L")) {
                    solution.statues = Result.Solution.FAILURE;
                    return solution;
                }
            }
            board.explored = new ArrayList<>();
        }
        board.explored.add(robotMove.toString());
        boolean cutoffOccurred = false;
        boolean duplicateOccurred = false;
        if (limit < 0) {
            solution.statues = Result.Solution.FAILURE;
            return solution;
        }

        if (limit == 0) {      // Check if limit is 0
            Collections.sort(board.explored);
            if (history.contains(board.explored.toString())) {
                solution.statues = Result.Solution.FAILURE;
            } else {
                history.add(board.explored.toString());
                solution.statues = Result.Solution.CUTOFF;
            }
            return solution;
        } else {
            HashMap<Node, String> frontier = new HashMap<>();
            if (isMoveAllowed(board, board.robot.toString(), "R")) {
                frontier.put(new Node(board.robot.row + 0, board.robot.col + 1), "R");
            }
            if (isMoveAllowed(board, board.robot.toString(), "U")) {
                frontier.put(new Node(board.robot.row - 1, board.robot.col + 0), "U");
            }
            if (isMoveAllowed(board, board.robot.toString(), "L")) {
                frontier.put(new Node(board.robot.row + 0, board.robot.col - 1), "L");
            }
            if (isMoveAllowed(board, board.robot.toString(), "D")) {
                frontier.put(new Node(board.robot.row + 1, board.robot.col + 0), "D");
            }

            generate += frontier.size();
            for (Node child : frontier.keySet()) {
                if (child == null) {
                    solution.statues = Result.Solution.FAILURE;
                    return solution;
                }
                solution = DLS(board.clone(), limit - 1, child, frontier.get(child));
                if (solution.statues == Result.Solution.CUTOFF) cutoffOccurred = true;
                else if (solution.statues == Result.Solution.DUPLICATE) duplicateOccurred = true;
                else if (solution.statues != Result.Solution.FAILURE) {
                    solution.movement = frontier.get(child) + " " + solution.movement;
                    return solution;
                }
            }
        }

        if (cutoffOccurred) {
            solution.statues = Result.Solution.CUTOFF;
            return solution;
        } else if (duplicateOccurred) {
            solution.statues = Result.Solution.DUPLICATE;
            return solution;
        } else {
            solution.statues = Result.Solution.FAILURE;
            return solution;
        }
    }

    /**
     * Goal testing - Check if we reach to the goal.
     *
     * @param persons
     * @param butters
     * @return
     */
    private static boolean positionMatch(ArrayList<String> persons, ArrayList<String> butters) {
        for (String eachButter : butters) {
            if (persons.contains(eachButter)) {
                return true;
            }
        }
        return false;
    }

    /**
     * Check if it is ok to move or not.
     *
     * @param board
     * @param target
     * @param direction
     * @return boolean
     */
    private static boolean isMoveAllowed(Board board, String target, String direction) {
        return isMoveAllowed(board, target, direction, 0);
    }

    private static boolean isMoveAllowed(Board board, String current, String direction, int limit) {
        String childPosition = move(current, direction);
        if (!board.blocks.contains(childPosition))           // If it's not block
            if (board.batteries.containsKey(childPosition))     // If it's in batteries arraylist
                if (board.butters.contains(childPosition)) {
                    if (limit >= 2) return false;
                    return isMoveAllowed(board, childPosition, direction, limit + 1);
                } else return true;
        return false;
    }

    /**
     * Map the direction to position.
     *
     * @param current
     * @param direction
     * @return
     */
    private static String move(String current, String direction) {
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
        String[] splittedPosition = current.split("_");
        return (Integer.parseInt(splittedPosition[0]) + column) + "_" + (Integer.parseInt(splittedPosition[1]) + row);
    }

}

