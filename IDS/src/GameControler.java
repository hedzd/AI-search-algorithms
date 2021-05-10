import java.awt.*;
import java.util.ArrayList;
import javax.swing.*;

public class GameControler {

    private View.Model model;
    private View view;

    public GameControler(Board board) {
        model = new View.Model(board);
        view = new View(model);
    }

    //Move robot or butter to the given position
    private void movePlayer(String position) {
        String[] splitted = position.split("_");
        model.setPlayerX(Integer.parseInt(splitted[0]));
        model.setPlayerY(Integer.parseInt(splitted[1]));
        view.refresh();
    }


    static class View {
        private final static int GAP = 2;
        Model model;
        private MainPanel mainPanel;

        View(Model model) {
            this.model = model;
            createAndShowGUI();
        }

        void refresh() {
            mainPanel.repaint();
        }

        private void createAndShowGUI() {
            JFrame f = new JFrame("Passing butter!");
            f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            mainPanel = new MainPanel();
            f.add(mainPanel);
            f.pack();
            f.setVisible(true);
        }

        class MainPanel extends JPanel {
            MainPanel() {
                setLayout(new BorderLayout(GAP, GAP));
                add(new TopPanel(), BorderLayout.PAGE_START);
                add(new BoardPanel(), BorderLayout.CENTER);
            }
        }

        class TopPanel extends JPanel {
            TopPanel() {
                setLayout(new FlowLayout(FlowLayout.LEADING));
                add(new JLabel("This is the game board "));
            }
        }

        class BoardPanel extends JPanel {
            Player robot;
            BoardPanel() {
                setBorder(BorderFactory.createLineBorder(Color.BLACK, GAP));
                GridLayout layout = new GridLayout(model.getBoardRows(),
                        model.getBoardCols());
                setLayout(layout);
                for (int i = 0; i < model.getBoardRows(); i++) {
                    for (int j = 0; j < model.getBoardCols(); j++) {
                        add(new Tile());
                    }
                }
                ImageIcon imageIcon =new ImageIcon("Robot.png");
                robot = new Player(imageIcon);
                robot.setBounds(new Rectangle(100, 100, 100, 100));
            }
        }

        class Tile extends JLabel {
            Tile() {
                setPreferredSize(new Dimension(model.getSquareSize(), model.getSquareSize()));
                setBorder(BorderFactory.createLineBorder(Color.BLACK, GAP));
            }
        }


        class Player extends JLabel {
            ImageIcon imageIcon;
            public Player(ImageIcon imageIcon) {
                this.imageIcon = imageIcon;
            }
        }

        static class Model {

            private int boardRows, boardCols, squareSize = 100;
            private int playerX, playerY;

            public Model(Board board) {
                boardRows = board.row;
                boardCols = board.col;
                playerX = board.robot.col;
                playerY = board.robot.row;
            }

            int getPlayerX() {
                return playerX;
            }

            void setPlayerX(int playerX) {
                this.playerX = playerX;
            }

            int getPlayerY() {
                return playerY;
            }

            void setPlayerY(int playerY) {
                this.playerY = playerY;
            }

            int getBoardRows() {
                return boardRows;
            }

            int getBoardCols() {
                return boardCols;
            }

            int getSquareSize() {
                return squareSize;
            }
        }
    }

}