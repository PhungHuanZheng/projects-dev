public class Sponge {
    final public float[] origin = new float[]{CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2, 0};
    
    public float[] pos;
    public float size = CANVAS_WIDTH / 2;
    public float rotation = 0;
    public Sponge[] children = new Sponge[27];
    
    public Sponge(float x, float y, float z, float size) {
        this.pos = new float[] {x, y, z};
    }

    public void split() {
        int childId = 0;
        for (int x = -1; x < 2; x++) {
            for (int y = -1; y < 2; y++) {
                for (int z = -1; z < 2; z++) {
                    // if center cubes, ignore
                    if ((x == 0 && y == 0) || (z == 0 && y == 0) || (x == 0 && z == 0)) {
                        children[childId] = null;
                    } else {
                        children[childId] = new Sponge(this.pos[0], this.pos[1], this.pos[2], this.size / 3);
                    }
                    childId++;
                }
            }
        }
    }

    public void show(float panSpeed) {
        translate(this.pos[0], this.pos[1], this.pos[2]);
        noFill();
        stroke(255);
        box(this.size);
        
        translate(this.origin[0], this.origin[1], this.origin[2]);
        this.rotation += panSpeed;
        rotateY(rotation);
        
        
    }
}
