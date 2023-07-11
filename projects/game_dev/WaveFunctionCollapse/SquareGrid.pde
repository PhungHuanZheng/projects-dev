public class SquareGrid {
    public int dim;
    public float tileLength;
    public Tile[][] tiles;

    public SquareGrid(int dim_, int[] tileOptions) {
        dim = dim_;
        tileLength = width / dim;

        // resize images
        for (int i = 0; i < tileImages.size(); i++) {
            while (tileImages.get(i).width == 0) continue;
            tileImages.get(i).resize((int)tileLength, (int)tileLength);
        }

        // init tile data
        tiles = new Tile[dim][dim];
        for (int y = 0; y < dim; y++) {
            for (int x = 0; x < dim; x++) {
                tiles[y][x] = new Tile(x, y, tileLength, tileOptions);
            }
        }
    }

    public void setTileStates(int x, int y, int[] stateSet) {
        tiles[y][x].setStates(stateSet);
    }

    public Tile getLowestEntropy() {
        int minEntropy = (int)Double.POSITIVE_INFINITY;
        ArrayList<Tile> minEntropyTiles = new ArrayList<Tile>();

        // get value of lowest entropy
        for (int y = 0; y < dim; y++) {
            for (int x = 0; x < dim; x++) {
                // if tile is collapsed, ignore
                if (tiles[y][x].isCollapsed) continue;

                int tileEntropy = tiles[y][x].availableStates.length;
                if (tileEntropy < minEntropy) {
                    minEntropy = tileEntropy;
                }
            }
        }

        // get tiles with the same lowest entropy
        for (int y = 0; y < dim; y++) {
            for (int x = 0; x < dim; x++) {
                if (tiles[y][x].availableStates.length == minEntropy) {
                    minEntropyTiles.add(tiles[y][x]);
                }
            }
        }
        
        // if no more empty tiles
        if (minEntropyTiles.size() == 0) 
            return null;
        return minEntropyTiles.get(floor(random(minEntropyTiles.size())));
    }

    public void collapseRandom() {
        // get random tile
        Tile tile = tiles[floor(random(dim))][floor(random(dim))];
        tile.collapse();
    }

    public void updateTiles(TileLookupTable lookup) {
        // iterate over tiles
        for (int y = 0; y < dim; y++) {
            for (int x = 0; x < dim; x++) {
                // if tile is collapsed, ignore
                if (tiles[y][x].isCollapsed) continue;

                // else access it's neighbours
                int[][] relPos = new int[][]{{-1, 0}, {0, 1}, {1, 0}, {0, -1}};
                ArrayList<Tile> collapsedNeighbours = new ArrayList<Tile>();
                for (int i = 0; i < relPos.length; i++) {
                    try {
                        Tile neighbour = tiles[y + relPos[i][0]][x + relPos[i][1]];
                        if (neighbour.isCollapsed) {
                            collapsedNeighbours.add(neighbour);
                        } else {
                            collapsedNeighbours.add(null);
                        };
                    }
                    catch (Exception e) {
                        collapsedNeighbours.add(null);
                        continue;
                    }
                }

                // if any collapsed neighbours
                if (collapsedNeighbours.size() > 0) {
                    ArrayList<Integer> availableStates = new ArrayList<Integer>();
                    // get all available states
                    for (int i = 0; i < collapsedNeighbours.size(); i++) {
                        if (collapsedNeighbours.get(i) == null) continue;
                        int[] neighbourStates = lookup.get(collapsedNeighbours.get(i).currentState, i);

                        // create unique set of available states
                        for (int state : neighbourStates) {
                            if (!availableStates.contains(state)) {
                                availableStates.add(state);
                            }
                        }
                    }
                    
                    // update tile's available states
                    int[] availableStatesArr = new int[availableStates.size()];
                    for (int i = 0; i < availableStates.size(); i++) {
                        availableStatesArr[i] = availableStates.get(i);
                    }
                    tiles[y][x].setStates(availableStatesArr);
                }
            }
        }
    }

    public void show() {
        for (int y = 0; y < dim; y++) {
            for (int x = 0; x < dim; x++) {
                tiles[y][x].show();
            }
        }
    }
}
