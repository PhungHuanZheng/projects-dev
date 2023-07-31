//public class aSponge {
//    float[] origin;
//    float x;
//    float y;
//    float z;
//    float size;

//    public float rotation = 0;
//    public int depth = 0;

//    public Sponge[] children = new Sponge[27];
//    public boolean hasChildren = false;

//    public aSponge(float[] origin, float size) {
//        this.origin = origin;
//        this.x = origin[0];
//        this.y = origin[1];
//        this.z = origin[2];
//        this.size = size;
//    }

//    public void split() {
//        // update booleans
//        this.hasChildren = true;

//        // populate children array
//        int childId = 0;
//        for (int x = -1; x < 2; x++) {
//            for (int y = -1; y < 2; y++) {
//                for (int z = -1; z < 2; z++) {
//                    // if center cubes, ignore
//                    if ((x == 0 && y == 0) || (z == 0 && y == 0) || (x == 0 && z == 0)) {
//                        this.children[childId] = null;
//                        println(1);
//                    } else {
//                        // generate cubes
//                        this.children[childId] = new Sponge(new float[], this.size / 3);
//                    }
//                    childId++;
//                }
//            }
//        }
//        rotateY(this.rotation);
//        noFill();
//        stroke(255);
//        box(width / 2);
//    }

//    public void show(float panSpeed) {
//        this.rotation += panSpeed;
//        translate(origin[0], origin[1], origin[2]);

//        if (!this.hasChildren) {
//            push();
//            rotateY(this.rotation);
//            noFill();
//            stroke(255);
//            box(this.size);
//            pop();
//        } else {
//            for (Sponge child : this.children) {
//                if (child != null) {
//                    child.show(panSpeed);
//                }
//            }
//        }
//    }
//}
