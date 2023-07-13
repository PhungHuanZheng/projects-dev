public class Tile {
    public Pos pos;
    public Shape tileShape;

    public Tile[] neighbours = new Tile[4];

    public int finalState = -1;
    public ArrayList<Integer> possibleStates = new ArrayList<Integer>();
    private ArrayList<Integer> _possibleStates = new ArrayList<Integer>();

    public boolean isCollapsed = false;

    public Tile(int x, int y, Shape tileShape_, int[] possibleStates_) {
        pos = new Pos(x, y);
        tileShape = tileShape_;

        for (int i = 0; i < possibleStates_.length; i++) {
            possibleStates.add(possibleStates_[i]);
            _possibleStates.add(possibleStates_[i]);
        }
    }

    public int getEntropy() {
        return possibleStates.size();
    }

    public void reset() {
        finalState = -1;
        isCollapsed = false;
        possibleStates = _possibleStates;
    }

    public void collapse() {
        // if no possible states
        if (possibleStates.size() == 0) {
            // go into neighbours and roll back
            for (Tile neighbour : neighbours) {
                if (neighbour != null) {
                    neighbour.reset();
                }
            }
            reset();
            return;
        }

        isCollapsed = true;
        finalState = possibleStates.get(floor(random(possibleStates.size())));

        possibleStates.clear();
        possibleStates.add(finalState);
    }

    public void updateNeighbours(ArrayList<Integer>[][] lookup) {
        int dir = -1;

        // iterate over neighbours
        for (int i = 0; i < neighbours.length; i++) {
            if (neighbours[i] == null || neighbours[i].isCollapsed) continue;

            // get neighbour's direction from main tile
            if (neighbours[i].pos.y - pos.y == -1) dir = 0;
            if (neighbours[i].pos.x - pos.x == 1) dir = 1;
            if (neighbours[i].pos.y - pos.y == 1) dir = 2;
            if (neighbours[i].pos.x - pos.x == -1) dir = 3;

            try {
                ArrayList<Integer> currentPossibleStates = lookup[finalState][dir];

                // get common values between current possible states and neighbour's possible states
                ArrayList<Integer> commonPossibleStates = new ArrayList<Integer>();
                for (int j = 0; j < currentPossibleStates.size(); j++) {
                    if (neighbours[i].possibleStates.contains(currentPossibleStates.get(j))) {
                        commonPossibleStates.add(currentPossibleStates.get(j));
                    }
                }
                neighbours[i].possibleStates = commonPossibleStates;

                //if neighbour's entropy is becomes 1, update it's neighbours
                if (neighbours[i].possibleStates.size() == 1) {
                    neighbours[i].collapse();
                    neighbours[i].updateNeighbours(lookup);
                }
            }
            catch (Exception e) {
                continue;
            }
        }
    }

    public void show(ArrayList<Image> allStates, boolean drawBorders) {
        // if collapsed, final state initialized
        if (isCollapsed && finalState != -1) {
            image(allStates.get(finalState).asPImage(), pos.x * tileShape.w, pos.y * tileShape.h);
        } else {
            // else get average pixel value of all current possible states
            Image averageImage = new Image(createImage(tileShape.w, tileShape.h, RGB));
            for (int i = 0; i < averageImage.pixels.length; i++) {
                float pixelAverage = 0;

                // iterate over all possible states
                for (int j = 0; j < possibleStates.size(); j++) {
                    pixelAverage += allStates.get(possibleStates.get(j)).pixels[i];
                }
                // set pixel
                averageImage.pixels[i] = (int)(pixelAverage / possibleStates.size());
            }
            image(averageImage.asPImage(), pos.x * tileShape.w, pos.y * tileShape.h);
        }

        if (drawBorders) {
            noFill();
            stroke(255, 0, 0);
            rect(pos.x * tileShape.w, pos.y * tileShape.h, tileShape.w, tileShape.h);
        }
    }
}
