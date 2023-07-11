public class Tile {
    public Pos chunkPos;
    public Pos globalPos;
    
    public String terrainName;
    public float traverseDifficulty;
    public float[] threshold;
    public color clr = color(255);
    
    public boolean wasTerraformed = false;
    
    public ArrayList<Tile> neighbours = new ArrayList<Tile>();
    public float f = 0;
    public float g = 0;
    public float h = 0;
    public Tile previous;
    
    public Tile(Chunk chunk_, int x_, int y_) {
        chunkPos = new Pos(x_, y_);
        globalPos = new Pos(chunk_.pos.x * chunk_.chunkShape.w + x_, chunk_.pos.y * chunk_.chunkShape.h + y_);
    }
    
    public void setTerrain(TerrainType terrain) {
        terrainName = terrain.terrainName;
        traverseDifficulty = terrain.traverseDifficulty;
        clr = terrain.clr;
    }
}
