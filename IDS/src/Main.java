public class Main {

    public static void main(String[] args) {
        long startTime = System.currentTimeMillis();
        // Initialization
        Board board = new Board();
        //TODO Initial properly: extract input
        board.initial();
        // IDS Search
        Statistics statistics = AIFunction.searchAlgorithm(board);
        //User Interface
        // GameControler boardGame= new GameControler(board);
        long endTime = System.currentTimeMillis();
        long timeElapsed = endTime - startTime;
        System.out.println("Execution time in milliseconds: " + timeElapsed);
        System.out.println("Expanded Nodes: " + statistics.expandedNode);
        System.out.println("Generated Nodes: " + statistics.generatedNode);
        System.out.println("Depth: " + statistics.depth);

    }

    static class Statistics {
        public long depth=0;
        public long expandedNode=0;
        public long generatedNode=0;
    }
}
