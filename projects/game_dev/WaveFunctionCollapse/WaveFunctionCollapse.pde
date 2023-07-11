final ArrayList<PImage> tileImages = new ArrayList<PImage>();
final int[] states = new int[]{0, 1, 2, 3, 4};

public SquareGrid grid;
public TileLookupTable lookupTable;


void setup() {
    size(400, 400);

    tileImages.add(requestImage("data/demo/blank.png"));
    tileImages.add(requestImage("data/demo/down.png"));
    tileImages.add(requestImage("data/demo/left.png"));
    tileImages.add(requestImage("data/demo/right.png"));
    tileImages.add(requestImage("data/demo/up.png"));

    lookupTable = new TileLookupTable();
    lookupTable.set(new int[][]{{0, 4}, {0, 3}, {0, 1}, {0, 2}});
    lookupTable.set(new int[][]{{0, 4}, {1, 2, 4}, {2, 3, 4}, {1, 3, 4}});
    lookupTable.set(new int[][]{{1, 3, 4}, {0, 3}, {2, 3, 4}, {1, 3, 4}});
    lookupTable.set(new int[][]{{1, 2, 3}, {1, 2, 4}, {2, 3, 4}, {0, 2}});
    lookupTable.set(new int[][]{{1, 2, 3}, {1, 2, 4}, {0, 1}, {1, 3, 4}});

    grid = new SquareGrid(10, states);
    grid.tiles[0][0].collapse();
    grid.updateTiles(lookupTable);


    println(grid.tiles[1][0].availableStates.length);
    printArray(grid.tiles[1][0].availableStates);

    windowResize(width + 1, height + 1);
}

void draw () {
    background(140);

    // get tile with lowest entropy
    Tile minEntropyTile = grid.getLowestEntropy();

    if (minEntropyTile == null) {
        grid.show();
        println(grid.tiles[1][0].currentState);
        noLoop();
        return;
    }

    minEntropyTile.collapse();
    grid.updateTiles(lookupTable);

    grid.show();
}
