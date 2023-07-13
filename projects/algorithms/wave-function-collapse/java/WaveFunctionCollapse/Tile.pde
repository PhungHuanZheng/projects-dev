public class Tile {
    public Pos pos;
    public Shape tileShape;

    public boolean isCollapsed = false;
    public ArrayList<PImage> possibleStates;
    public PImage currentState = null;

    public Tile(int x, int y, Shape tileShape_, ArrayList<PImage> possibleStates_) {
        pos = new Pos(x, y);
        tileShape = tileShape_;

        possibleStates = possibleStates_;
    }

    public void collapse() {
        // if only one possible state left, set as it
        if (possibleStates.size() == 1) {
            currentState = possibleStates.get(0);
        } else {
            currentState = possibleStates.get(floor(random(possibleStates.size())));
        }
        isCollapsed = true;
    }
    
    public int getEntropy() {
        return possibleStates.size();
    }

    public void show() {
        // if tile not collapsed
        if (!isCollapsed) {
            // overlay possible states with reduced opacity
            for (PImage state : possibleStates) {
                tint(255, 255 / possibleStates.size());
                image(state, pos.x * tileShape.w, pos.y * tileShape.h);
            }
        } else {
            image(currentState, pos.x * tileShape.w, pos.y * tileShape.h);
        }


        // draw tile borders
        noFill();
        stroke(255, 0, 0);
        rect(pos.x * tileShape.w, pos.y * tileShape.h, tileShape.w, tileShape.h);
    }
}
