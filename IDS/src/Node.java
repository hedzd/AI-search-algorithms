public class Node {
    public int row;
    public int col;

    public Node(int row, int col) {
        this.row = row;
        this.col = col;
    }

    @Override
    public String toString() {
        return col + "_" + row;
    }
}
