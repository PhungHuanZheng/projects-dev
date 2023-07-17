public class Wave {
    public Shape shape;
    public Tile[][] tiles;

    public ArrayList<Image> tileImages;
    public Shape tileShape = null;

    public Wave(int w, int h, String tileImagesPath, int[] resize) {
        shape = new Shape(w, h);

        // init array list and adjust path
        tileImages = new ArrayList<Image>();
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
            tileImages.add(new Image(image));
        }

        // array of possible state ids
        int[] possibleStates = new int[tileImages.size()];
        for (int i = 0; i < tileImages.size(); i++) {
            possibleStates[i] = i;
        }

        // init 2D array of Tiles
        tiles = new Tile[shape.h][shape.w];
        for (int y = 0; y < shape.h; y++) {
            for (int x = 0; x < shape.w; x++) {
                tiles[y][x] = new Tile(x, y, new Shape(resize[0], resize[1]), possibleStates);
            }
        }

        // init tile neighbours
        int[][] relPos = new int[][]{{0, -1}, {1, 0}, {0, 1}, {-1, 0}};
        for (int y = 0; y < shape.h; y++) {
            for (int x = 0; x < shape.w; x++) {
                Tile tile = tiles[y][x];

                // iterate over neighbouring tiles
                for (int i = 0; i < relPos.length; i++) {
                    try {
                        tile.neighbours[i] = tiles[y + relPos[i][1]][x + relPos[i][0]];
                    }
                    catch (Exception e) {
                        tile.neighbours[i] = null;
                    }
                }
            }
        }
    }

    public Tile tileAt(int x, int y) {
        return tiles[y][x];
    }

    public ArrayList<Integer>[][] generateLookup(int sections, float threshold) {
        // build data structure
        ArrayList[][] lookupTable = new ArrayList[tileImages.size()][4];

        // iterate over image and all other images
        for (int i = 0; i < tileImages.size(); i++) {
            Image image = tileImages.get(i);

            for (int j = 0; j < tileImages.size(); j++) {
                Image other = tileImages.get(j);

                // init pixel borders between main and other image
                int[] mainBorder = null, otherBorder = null;

                // iterate over 4 neighbouring positions
                for (int k = 0; k < 4; k++) {
                    // init lookup array list
                    if (lookupTable[i][k] == null) {
                        lookupTable[i][k] = new ArrayList<Integer>();
                    }

                    // get pixels bordering main and other image
                    switch (k) {
                    case 0:
                        mainBorder = image.getRow(0);
                        otherBorder = other.getRow(other.height - 1);
                        break;
                    case 1:
                        mainBorder = image.getCol(image.width - 1);
                        otherBorder = other.getCol(0);
                        break;
                    case 2:
                        mainBorder = image.getRow(image.height - 1);
                        otherBorder = other.getRow(0);
                        break;
                    case 3:
                        mainBorder = image.getCol(0);
                        otherBorder = other.getCol(other.width - 1);
                        break;
                    }

                    // split border arrays by sections
                    ArrayList<Integer>[] mainBorderSections = splitArray(mainBorder, sections);
                    ArrayList<Integer>[] otherBorderSections = splitArray(otherBorder, sections);
                    boolean toAdd = true;

                    // check element wise equality between pixels in borders
                    for (int g = 0; g < sections; g++) {
                        float sectionError = 0;
                        for (int c = 0; c < mainBorderSections[g].size(); c++) {
                            sectionError += abs(mainBorderSections[g].get(c) - otherBorderSections[g].get(c));
                        }
                        sectionError = (sectionError / mainBorderSections[g].size()) / 255;

                        // if any section goes out of threshold
                        if (sectionError > threshold) {
                            toAdd = false;
                        }
                    }

                    if (toAdd) {
                        lookupTable[i][k].add(j);
                    }
                }
            }
        }
        return lookupTable;
    }

    public void collapseRandom(int count) {
        for (int i = 0; i < count; i++) {
            while (true) {
                // get random position on grid
                int randx = floor(random(shape.w));
                int randy = floor(random(shape.h));
                Tile tile = tileAt(randx, randy);

                // if tile isn't already collapsed, collapse
                if (!tile.isCollapsed) {
                    tile.collapse();
                    break;
                }
            }
        }
    }

    public Tile getLowestEntropy() {
        ArrayList<Tile> lowestEntropyGroup = new ArrayList<Tile>();
        int lowestEntropyValue = (int)Double.POSITIVE_INFINITY;

        // get array of tiles with lowest entropy
        for (int y = 0; y < shape.h; y++) {
            for (int x = 0; x < shape.w; x++) {
                Tile tile = tileAt(x, y);
                int tileEntropy = tile.getEntropy();

                // if tile is already collapsed, ignore
                if (tile.isCollapsed) {
                    continue;
                }

                // if same entropy, add to array
                if (tileEntropy == lowestEntropyValue) {
                    lowestEntropyGroup.add(tile);
                } else if (tile.getEntropy() < lowestEntropyValue) {
                    lowestEntropyValue = tile.getEntropy();
                    lowestEntropyGroup.clear();
                    lowestEntropyGroup.add(tile);
                }
            }
        }

        // pick randomly from group of lowest entropy tiles
        return lowestEntropyGroup.get(floor(random(lowestEntropyGroup.size())));
    }

    public void updateTiles(ArrayList<Integer>[][] lookup) {
        // iterate over tiles
        for (int y = 0; y < shape.h; y++) {
            for (int x = 0; x < shape.w; x++) {
                Tile tile = tileAt(x, y);
                
                if (tile.possibleStates.size() == 1) {
                    tile.collapse();
                }

                if (tile.isCollapsed) {
                    tile.updateNeighbours(lookup);
                }
            }
        }
    }

    public void show(boolean drawBorders) {
        for (int y = 0; y < shape.h; y++) {
            for (int x = 0; x < shape.w; x++) {
                tiles[y][x].show(tileImages, drawBorders);
            }
        }
    }
}

public ArrayList<Integer>[] splitArray(int[] arr, int sections) {
    ArrayList<Integer>[] arrSections = new ArrayList[sections];
    int sectionLength = floor(arr.length / sections);

    for (int i = 0; i < arrSections.length - 1; i++) {
        arrSections[i] = new ArrayList<Integer>();
        for (int j = 0; j < sectionLength; j++) {
            arrSections[i].add(arr[i * sectionLength + j]);
        }
    }

    arrSections[arrSections.length - 1] = new ArrayList<Integer>();
    for (int j = (sections - 1) * sectionLength; j < arr.length; j++) {
        arrSections[arrSections.length - 1].add(arr[j]);
    }

    return arrSections;
}
