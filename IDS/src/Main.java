import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Scanner;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Main {

    public static void main(String[] args) {

        // Initialization
        Board board = new Board();
        board.initial();

        // IDS Search
        AIFunction.IDS(board);
    }
}
