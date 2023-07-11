public class TerrainMap {
    public float cellLength;
    public int[] shape = {0, 0};
    public Tile[][] data;

    public int canvasWidth;
    public int canvasHeight;

    public ArrayList<TerrainType> terrainTypes = new ArrayList<TerrainType>();

    public int neighbourCount = 0;

    public TerrainMap(float cellLength_) {
        cellLength = cellLength_;

        // get closest integer to current width and height
        int widthInTiles = (int)(width / cellLength_);
        int heightInTiles = (int)(height / cellLength_);

        // define shape as array of width and height, redefine data array
        shape[0] = widthInTiles;
        shape[1] = heightInTiles;
        data = new Tile[heightInTiles][widthInTiles];

        // build grid data
        for (int y = 0; y < shape[1]; y++) {
            for (int x = 0; x < shape[0]; x++) {
                data[y][x] = new Tile(x, y, cellLength);
            }
        }

        // define new size for canvas to fit grid created
        canvasWidth = (int)(shape[0] * cellLength);
        canvasHeight = (int)(shape[1] * cellLength);
    }

    public void addTerrain(String name, float traverseDifficulty, float[] threshold, color clr) {
        TerrainType terrain = new TerrainType(name, traverseDifficulty, threshold, clr);
        terrainTypes.add(terrain);
    }

    public void initTerrain(float smoothness) {
        // iterate over tiles in map
        for (int y = 0; y < shape[1]; y++) {
            for (int x = 0; x < shape[0]; x++) {

                // get noise values for all tiles
                Tile tile = data[y][x];
                float tileNoise = noise(x / smoothness, y / smoothness);

                // map noise to terrain type thresholds
                for (int i = 0; i < terrainTypes.size(); i++) {
                    TerrainType terrain = terrainTypes.get(i);

                    //check noise value against terrain's threshold
                    if (tileNoise >= terrain.threshold[0] && tileNoise < terrain.threshold[1]) {
                        tile.terrainName = terrain.name;
                        tile.traverseDifficulty = terrain.traverseDifficulty;
                        tile.clr = terrain.clr;
                        break;
                    }
                }
            }
        }
    }

    public Tile tileAt(int x, int y) {
        return data[y][x];
    }

    public void initNeighbours(int neighbourCount_) throws InvalidNeighboursInitializer {
        // validate neighbourCount param
        if (!(neighbourCount_ == 4 || neighbourCount_ == 8)) {
            throw new InvalidNeighboursInitializer(String.format("Expecting 4 or 8 for parameter neighbourCount, got %d.", neighbourCount));
        }
        neighbourCount = neighbourCount_;

        // iterate over all cells
        for (int y = 0; y < shape[1]; y++) {
            for (int x = 0; x < shape[0]; x++) {
                Tile tile = data[y][x];

                // iterate over neighbours of cell;
                for (int j = -1; j <= 1; j++) {
                    for (int i = -1; i <= 1; i++) {

                        // skip if self or 4 neighbour mode
                        if (i == 0 && j == 0) continue;
                        if (neighbourCount_ == 4 && !(i == 0 || j == 0)) continue;

                        // if out of bounds
                        if (y + j < 0 || y + j >= shape[1] || y + j >= shape[1]) continue;
                        if (x + i < 0 || x + i >= shape[0] || x + i >= shape[0]) continue;
                        if (data[y + j] == null || data[y + j][x + i] == null) continue;

                        // append tiles around to tile's neighbours
                        tile.neighbours.add(data[y + j][x + i]);
                    }
                }
                
                if (tile.neighbours.size() == 0) {
                    println(111);
                }
            }
        }
    }

    public ArrayList<Tile> pathfind(Tile start, Tile end) {
        Tile currentTile = end;
        ArrayList<Tile> path = new ArrayList<Tile>();
        ArrayList<Tile> openSet = new ArrayList<Tile>();
        ArrayList<Tile> closedSet = new ArrayList<Tile>();
        openSet.add(start);

        // loop till open set is empty
        while (openSet.size() > 0) {
            // get tile with the lowest cost (f), set as next to be checked
            int lowestCostIndex = 0;
            for (int i = 1; i < openSet.size(); i++) {
                // if lower cost than current lowest cost, set
                if (openSet.get(i).f < openSet.get(lowestCostIndex).f) {
                    lowestCostIndex = i;
                }
            }
            currentTile = openSet.get(lowestCostIndex);

            // if end tile reached, break loop
            if (currentTile.x == end.x && currentTile.y == end.y) {
                break;
            }

            // premeptively move tile from open set to closed set
            openSet.remove(currentTile);
            closedSet.add(currentTile);

            // iterate over tile neighbours
            for (int i = 0; i < currentTile.neighbours.size(); i++) {
                Tile neighbour = currentTile.neighbours.get(i);

                // if neighbour in closed set, ignore
                if (closedSet.contains(neighbour)) continue;

                // store temp value for neighbour's step cost
                float tempG = currentTile.g + 1;

                // if neighbour in open set, reevaluate and set new step cost if lower
                if (openSet.contains(neighbour)) {
                    if (tempG < neighbour.g) {
                        neighbour.g = tempG;
                    }
                } else {
                    // else append to open set
                    neighbour.g = tempG;
                    openSet.add(neighbour);
                }

                // get heuristic (grid distance) between neighbour and end
                neighbour.h = heuristic(neighbour, end, neighbourCount);
                neighbour.f = neighbour.g + neighbour.h;

                // set previous of neighbour to current (current's next tile)
                neighbour.previous = currentTile;
            }
        }

        // once loop ended/end reached, current tile already set to end
        Tile temp = currentTile;
        path.add(currentTile);

        // recursive-ish loop to get path
        while (temp.previous != null) {
            path.add(temp.previous);
            temp = temp.previous;
        }

        return path;
    }


    public void show() {
        for (int y = 0; y < shape[1]; y++) {
            for (int x = 0; x < shape[0]; x++) {
                data[y][x].show();
            }
        }
    }
}


public float heuristic(Tile tile1, Tile tile2, int neighbourCount) {
    float h;
    if (neighbourCount == 4) {
        h = abs(tile1.x - tile2.x) + abs(tile1.y - tile2.y);
        h *= (tile1.traverseDifficulty / 2 + tile2.traverseDifficulty / 2);
        return h;
    }

    h = dist(tile1.x, tile1.y, tile2.x, tile2.y);
    if (tile1.x == tile2.x || tile1.y == tile2.y)
        h *= (tile1.traverseDifficulty / 2 + tile2.traverseDifficulty / 2);
    else
        h *= (tile1.traverseDifficulty / sqrt(2) + tile2.traverseDifficulty / sqrt(2));
    return h;
}


private class InvalidNeighboursInitializer extends RuntimeException {
    public InvalidNeighboursInitializer(String error) {
        super(error);
    }
}
