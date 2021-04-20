import java.util.ArrayList;
import java.util.HashMap;
import java.util.Scanner;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Board {

    public HashMap<String, Integer> batteries = new HashMap<String, Integer>();
    public ArrayList<String> blocks = new ArrayList<String>();
    public ArrayList<Node> butters = new ArrayList<Node>();
    public ArrayList<Node> persons = new ArrayList<Node>();
    public Node robot;
    public int row, col;

    public void initial() {

        Scanner scan = new Scanner(System.in);

        row = scan.nextInt();
        col = scan.nextInt();

        // Regex
        Pattern isDigit = Pattern.compile("^\\d+$");
        Pattern isBlock = Pattern.compile("^[x]{1}$");
        Pattern isEntity = Pattern.compile("^\\d+([prb])$");

        //TODO implement properly!
        String line = scan.nextLine();
        for (int i = 0; i < row; i++) {

            line = scan.nextLine();
            String[] splitted = line.split("\\t");

            for (int j = 0; j < col; j++) {

                Node newNode = new Node(i,j);

                Matcher matcher = isDigit.matcher(splitted[j]);
                if (matcher.find())
                    batteries.put(i+"_"+j, Integer.parseInt(splitted[j]));
                else {
                    matcher = isBlock.matcher(splitted[j]);
                    if (matcher.find())
                        blocks.add(i+"_"+j);
                    else {
                        matcher = isEntity.matcher(splitted[j]);
                        if (matcher.find()) {
                            switch (matcher.group(1)) {
                                case "r":
                                    robot = newNode;
                                    break;
                                case "b":
                                    butters.add(newNode);
                                    break;
                                case "p":
                                    persons.add(newNode);
                                    break;
                            }
                        } else System.out.println("Wrong Input!");
                    }
                }
            }
        }
    }
}
