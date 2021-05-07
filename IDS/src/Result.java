
public class Result {

    enum Solution {
        SUCCESS,
        FAILURE,
        CUTOFF,
        DUPLICATE
    }
    private Board board;
    public Solution statues;
    public String movement="";


    public void setBoard(Board board){
        this.board = board;
    }

    public Board getBoard(){
        return board;
    }
}
