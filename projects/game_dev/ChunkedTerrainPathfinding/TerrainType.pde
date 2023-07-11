public class TerrainType {
    public String terrainName;
    public float traverseDifficulty;
    public float[] threshold;
    public color clr;
    
    public TerrainType(String terrainName_, float traverseDifficulty_, float[] threshold_, color clr_) {
        terrainName = terrainName_;
        traverseDifficulty = traverseDifficulty_;
        threshold = threshold_;
        clr = clr_;
    }
}
