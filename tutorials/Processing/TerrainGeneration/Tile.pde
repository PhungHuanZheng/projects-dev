class Tile {
    public int x;
    public int y;
    public float cellLength;
    
    public String terrainName;
    public float traverseDifficulty;
    public color clr;
    
    public float f;
    public float g;
    public float h;
    public ArrayList<Tile> neighbours = new ArrayList<Tile>();
    public Tile previous;

    public Tile(int x_, int y_, float cellLength_) {
        x = x_;
        y = y_;
        cellLength = cellLength_;
    }

    public void show() {
        rectMode(CORNER); noStroke(); fill(clr == 0 ? color(255) : clr);
        rect(x * cellLength, y * cellLength, cellLength, cellLength);
    }
}
