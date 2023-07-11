public class TileLookupTable {
    public int[] tileStates;
    private ArrayList<TileDirectionData> tileData = new ArrayList<TileDirectionData>();

    public void set(int[][] data) {
        tileData.add(new TileDirectionData(data[0], data[1], data[2], data[3]));
    }
    
    public int[] get(int index, int dir) {
        return tileData.get(index).get(dir);
    }
}

private class TileDirectionData {
    public ArrayList<int[]> data = new ArrayList<int[]>();

    public TileDirectionData(int[] UP_, int[] RIGHT_, int[] DOWN_, int[] LEFT_) {
        data.add(UP_);
        data.add(RIGHT_);
        data.add(DOWN_);
        data.add(LEFT_);
    }
    
    public int[] get(int index) {
        return data.get(index);
    }
}
