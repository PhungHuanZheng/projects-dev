public class DynamicGrid {
    public float cellLength;
    public int[] shape = {0, 0};
    public Tile[][] data;

    int canvasWidth;
    int canvasHeight;

    public DynamicGrid(float cellLength_) {
        cellLength = cellLength_;

        // get closest integer to current width and height
        int widthInTiles = (int)(width / cellLength_);
        int heightInTiles = (int)(height / cellLength_);

        // define shape as array of width and height, redefine data array
        shape[0] = widthInTiles;
        shape[1] = heightInTiles;
        data = new Tile[heightInTiles][widthInTiles];

        // build grid data
        for (int y = 0; y < shape[1]; y++) {
            for (int x = 0; x < shape[0]; x++) {
                data[y][x] = new Tile(x, y);
            }
        }

        // define new size for canvas to fit grid created
        canvasWidth = (int)(shape[0] * cellLength);
        canvasHeight = (int)(shape[1] * cellLength);
    }

    public void show() {
        for (int y = 0; y < shape[1]; y++) {
            for (int x = 0; x < shape[0]; x++) {
                fill(map(noise(x / 15, y / 15), 0, 1, 0, 255));
                rect(x * cellLength, y * cellLength, cellLength, cellLength);
            }
        }
    }
}

public class Tile {
    int x;
    int y;

    public Tile(int x_, int y_) {
        x = x_;
        y = y_;
    }
}
