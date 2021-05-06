import java.util.ArrayList;
import java.util.HashMap;
import java.util.Scanner;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Board {

    public HashMap<String, Integer> batteries = new HashMap<String, Integer>();
    public ArrayList<String> blocks = new ArrayList<String>();
    public ArrayList<String> butters = new ArrayList<String>();
    public ArrayList<String> persons = new ArrayList<String>();
    public Node robot;
    public int row, col;
    public String movement ="";

    public void initial() {

        Scanner scan = new Scanner(System.in);

        row = scan.nextInt();
        col = scan.nextInt();

        // Regex
        Pattern isDigit = Pattern.compile("^\\d+$");
        Pattern isBlock = Pattern.compile("^[x]{1}$");
        Pattern isEntity = Pattern.compile("^(\\d)+([prb])$");

        //TODO implement properly!
        String line = scan.nextLine();
        for (int i = 0; i < row; i++) {

            line = scan.nextLine();
            String[] splitted = line.split("\\t");

            for (int j = 0; j < col; j++) {

                Node newNode = new Node(i, j);

                String position = j + "_" + i;
                Matcher matcher = isDigit.matcher(splitted[j]);
                if (matcher.find())
                    batteries.put(position, Integer.parseInt(splitted[j]));
                else {
                    matcher = isBlock.matcher(splitted[j]);
                    if (matcher.find())
                        blocks.add(position);
                    else {
                        matcher = isEntity.matcher(splitted[j]);
                        if (matcher.find()) {
                            switch (matcher.group(2)) {
                                case "r":
                                    robot = newNode;
                                    break;
                                case "b":
                                    butters.add(position);
                                    break;
                                case "p":
                                    persons.add(position);
                                    break;
                            }
                            batteries.put(position,Integer.parseInt(matcher.group(1)));
                        } else System.out.println("Wrong Input!");
                    }
                }
            }
        }
    }

    public Board clone(){
        Board newBoard = new Board();
        newBoard.batteries = this.batteries;
        newBoard.blocks = this.blocks;
        for (int i = 0; i < butters.size(); i++) {
            newBoard.butters.add(this.butters.get(i));
        }
        newBoard.persons = this.persons;
        newBoard.robot = new Node(this.robot.row,this.robot.col);
        newBoard.row = this.row;
        newBoard.col= this.col;
        newBoard.movement = this.movement;
        return newBoard;
    }
}
