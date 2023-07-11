public class TerrainType {
    public String name;
    public float traverseDifficulty;
    public float[] threshold;
    public color clr;

    public TerrainType(String name_, float traverseDifficulty_, float[] threshold_, color clr_) {
        name = name_;
        traverseDifficulty = traverseDifficulty_;
        threshold = threshold_;
        clr = clr_;
    }
}
