public class Tile {
    public int x;
    public int y;
    public float tileLength;

    public boolean isCollapsed = false;
    public int[] availableStates;
    public int currentState = -1;
    
    public Tile(int x_, int y_, float tileLength_, int[] availableStates_) {
        x = x_;
        y = y_;
        tileLength = tileLength_;
        
        availableStates = availableStates_;
    }
    
    public void setStates(int[] stateSet) {
        availableStates = stateSet;
        if (stateSet.length == 1) {
            isCollapsed = true;
            currentState = stateSet[0];
        }
    }
    
    public void collapse() {
        setStates(new int[]{floor(random((float)availableStates.length))});
    }
    
    public void show() {
        if (currentState == -1) {
            noFill();
            stroke(255);
            rect(x * tileLength, y * tileLength, tileLength, tileLength);
            return;
        }
        
        // get image by index of state in states array
        image(tileImages.get(currentState), x * tileLength, y * tileLength);
    }
}
