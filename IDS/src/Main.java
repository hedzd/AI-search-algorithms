import java.util.Scanner;

public class Main {

    public static void main(String[] args) {

        //Get input
        Scanner scan = new Scanner(System.in);
        int row, col;
        row = scan.nextInt();
        col = scan.nextInt();

        String[][] board = new String[row][col];

        String line;

        for (int i = 0; i < row; i++) {
            line = scan.nextLine();
            String[] splitted = line.split("\\s+");// split by space
            for (int j = 0; j < col; j++) {
                board[i][j] = splitted[j];
            }
        }



    }
}
