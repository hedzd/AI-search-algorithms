public class Main {

    public static void main(String[] args) {
        // Initialization
        Board board = new Board();
        //TODO Initial properly: extract input
        board.initial();
        // IDS Search
        AIFunction.searchAlgorithm(board);
    }
}
