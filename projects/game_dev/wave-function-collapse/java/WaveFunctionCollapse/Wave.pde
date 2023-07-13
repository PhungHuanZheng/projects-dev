public class Wave {
    public Shape shape;
    public Tile[][] tiles;

    public ArrayList<PImage> tileImages;
    public Shape tileShape = null;

    public Wave(int w, int h, String tileImagesPath, int[] resize) {
        shape = new Shape(w, h);

        // init array list and adjust path
        tileImages = new ArrayList<PImage>();
        File folder = new File(sketchPath(tileImagesPath));

        // load images from directory, push to array list
        for (final File file : folder.listFiles()) {
            String filepath = file.getAbsolutePath();
            PImage image = loadImage(filepath);
            println(filepath);

            // init tileShape attribute or validate image
            if (tileShape == null) {
                tileShape = new Shape(image.width, image.height);
            } else if (image.width != tileShape.w || image.height != tileShape.h) {
                throw new RuntimeException(String.format(
                    "Image \"%s\" has shape (%d, %d), inconsistent with first image with shape (%d, %d).",
                    filepath, image.width, image.height, tileImages.get(0).width, tileImages.get(0).height
                    ));
            }

            // resize and push
            image.resize(resize[0], resize[1]);
            image.loadPixels();
            tileImages.add(image);
        }
        tileShape = new Shape(resize[0], resize[1]);

        // init tiles in 2D array
        tiles = new Tile[h][w];
        for (int y = 0; y < shape.h; y++) {
            for (int x = 0; x < shape.w; x++) {
                tiles[y][x] = new Tile(x, y, tileShape, tileImages);
            }
        }
    }

    public Tile tileAt(int x, int y) {
        return tiles[y][x];
    }

    public ArrayList<Integer>[][] generateLookup(float threshold) {
        // build data structure
        ArrayList[][] lookupTable = new ArrayList[tileImages.size()][4];

        // iterate over image and all other images
        for (int i = 0; i < tileImages.size(); i++) {
            PImage image = tileImages.get(i);

            for (int j = 0; j < tileImages.size(); j++) {
                PImage other = tileImages.get(j);

                // get and reshape pixels of main image and other image
                PixelMatrix mainPixels = new PixelMatrix(image.pixels, tileShape.w, tileShape.h);
                PixelMatrix otherPixels = new PixelMatrix(other.pixels, tileShape.w, tileShape.h);

                int[] mainBorder = null, otherBorder = null;

                // iterate over possible neighbour positions of other ['UP', 'RIGHT', 'DOWN', 'LEFT']
                for (int k = 0; k < 4; k++) {
                    // init lookup array list
                    if (lookupTable[i][k] == null) {
                        lookupTable[i][k] = new ArrayList<Integer>();
                    }

                    // get borders between image and other
                    switch (k) {
                    case 0:
                        mainBorder = mainPixels.getRow(0);
                        otherBorder = otherPixels.getRow(otherPixels.shape.h - 1);
                        break;

                    case 1:
                        mainBorder = mainPixels.getCol(mainPixels.shape.w - 1);
                        otherBorder = otherPixels.getCol(0);
                        break;

                    case 2:
                        mainBorder = mainPixels.getRow(mainPixels.shape.h - 1);
                        otherBorder = otherPixels.getRow(0);
                        break;

                    case 3:
                        mainBorder = mainPixels.getCol(0);
                        otherBorder = otherPixels.getCol(otherPixels.shape.w - 1);
                        break;
                    }

                    //check element-wise equality between pixels on borders
                    if (pixelArrayDifference(mainBorder, otherBorder) < threshold) {
                        lookupTable[i][k].add(j);
                    }
                }
            }
        }

        return lookupTable;
    }

    public void collapseRandomTiles(int count) {
        for (int i = 0; i < count; i++) {
            // keep looping if landed on an already collapsed tile
            while (true) {
                // get random position
                int randx = floor(random(shape.w));
                int randy = floor(random(shape.h));
                Tile tile = tileAt(randx, randy);

                if (!tile.isCollapsed) {
                    tile.collapse();
                    break;
                }
            }
        }
    }

    public void updateEntropies(ArrayList<Integer>[][] lookup) {
        // iterate over tiles
        for (int y = 0; y < shape.h; y++) {
            for (int x = 0; x < shape.w; x++) {
                Tile tile = tileAt(x, y);

                // if tile is collapsed
                if (tile.isCollapsed) {
                    // get state index
                    int stateId = tileImages.indexOf(tile.currentState);

                    // get tile's neighbours
                    int[][] mainToNeighbours = new int[][]{{0, -1}, {1, 0}, {0, 1}, {-1, 0}};
                    for (int i = 0; i < mainToNeighbours.length; i++) {
                        try {
                            Tile neighbour = tileAt(tile.pos.x + mainToNeighbours[i][0], tile.pos.y + mainToNeighbours[i][1]);
                            switch (i) {
                                case
                            }
                        }
                        catch (Exception e) {
                            continue;
                        }
                    }
                }
            }
        }
    }

    public void show() {
        for (int y = 0; y < shape.h; y++) {
            for (int x = 0; x < shape.w; x++) {
                tileAt(x, y).show();
            }
        }
    }
}





public float pixelArrayDifference(int[] A, int[] B) {
    if (A.length != B.length) return 1000;

    PImage imageA  = new PImage(1, A.length, A, false, null);
    PImage imageB  = new PImage(1, B.length, B, false, null);

    float error = 0;
    for (int i = 0; i < A.length; i++) {
        color colourA = imageA.get(0, i);
        color colourB = imageB.get(0, i);

        error += abs(red(colourA) - red(colourB));
        error += abs(blue(colourA) - blue(colourB));
        error += abs(green(colourA) - green(colourB));
    }
    return (error / 255) / (A.length * 3);
}
