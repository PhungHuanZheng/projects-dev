int waveWidth = 10;
int waveHeight = 10;
int[] imageSize = new int[]{64, 64};

Wave wave;
ArrayList<Integer>[][] lookup;

void settings() {
    size(waveWidth * imageSize[0], waveWidth * imageSize[1]);
}

void setup() {
    loadPixels();

    wave = new Wave(10, 10, "data/demo", new int[]{64, 64});
    println(wave.shape.w * wave.tileShape.w, wave.shape.h * wave.tileShape.h);

    lookup = wave.generateLookup(0.1);
    displayLookupTable(lookup);
    
    wave.collapseRandomTiles(1);
    wave.updateEntropies(lookup);
}

void draw() {
    wave.show();
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


public class Pos {
    public int x;
    public int y;

    public Pos(int x_, int y_) {
        x = x_;
        y = y_;
    }
}

public class Shape {
    public int w;
    public int h;

    public Shape(int w_, int h_) {
        w = w_;
        h = h_;
    }
}
