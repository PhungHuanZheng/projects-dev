final int waveWidth = 34;
final int waveHeight = 17;
final int[] imageSize = new int[]{32, 32};
final boolean drawBorders = false;

Wave wave;
ArrayList<Integer>[][] lookup;

void settings() {
    size(waveWidth * imageSize[0], waveHeight * imageSize[1]);
}

void setup() {
    wave = new Wave(waveWidth, waveHeight, "data/demo-alter", imageSize);

    lookup = wave.generateLookup(3, 0.01);
    displayLookupTable(lookup);

    wave.collapseRandom(0);
    wave.updateTiles(lookup);
}

void draw() {
    background(0);
    
    Tile tile;
    try {
        tile = wave.getLowestEntropy();
        tile.collapse();
    }
    catch (Exception e) {
        noLoop();
    }

    

    wave.updateTiles(lookup);
    wave.show(drawBorders);

    //try {
    //    Tile tile = wave.getLowestEntropy();
    //    tile.collapse();

    //    wave.updateTiles(lookup);
    //    wave.show(drawBorders);
    //}
    //catch (IndexOutOfBoundsException e) {
    //    print(e);

    //    wave.updateTiles(lookup);
    //    wave.show(drawBorders);

    //    //for (int y = 0; y < wave.shape.h; y++) {
    //    //    println();
    //    //    for (int x = 0; x < wave.shape.w; x++) {
    //    //        print(wave.tileAt(x, y).getEntropy());
    //    //    }
    //    //}
    //    noLoop();
    //}

    saveFrame(sketchPath("frames/#####.png"));
}

void displayLookupTable(ArrayList<Integer>[][] lookup) {
    println();
    for (int i = 0; i < lookup.length; i++) {
        for (int j = 0; j < lookup[i].length; j++) {
            print(lookup[i][j]);
        }
        println();
    }
}
