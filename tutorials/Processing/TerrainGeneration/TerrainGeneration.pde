final boolean frameByFrame = true;

TerrainMap map;
Tile start, end;

Tile currentTile;
ArrayList<Tile> path = new ArrayList<Tile>();
ArrayList<Tile> openSet = new ArrayList<Tile>();
ArrayList<Tile> closedSet = new ArrayList<Tile>();

void setup() {
    // set up map and canvas
    size(1600, 900); 
    map = generateMap(9, (long)(random(width) * random(height)), 50);
    map.initNeighbours(4);
    printArray(map.shape);
    windowResize(map.canvasWidth, map.canvasHeight);

    start = map.tileAt(0, 0);
    end = map.tileAt(map.shape[0] - 1, map.shape[1] - 1);
    start.clr = color(0, 255, 0);
    end.clr = color(255, 0, 0);

    if (!frameByFrame) path = map.pathfind(start, end);
    currentTile = end;
    openSet.add(start);
}

void draw() {
    background(0);
    println(frameRate);
    map.show();

    // if path found in setup
    if (!frameByFrame) {
        for (int i = 1; i < path.size() - 1; i++) {
            path.get(i).clr = color(255);
        }
        noLoop();
    }

    if (openSet.size() > 0) {
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
            return;
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
            neighbour.h = heuristic(neighbour, end, map.neighbourCount);
            neighbour.f = neighbour.g * 2 + neighbour.h;

            // set previous of neighbour to current (current's next tile)
            neighbour.previous = currentTile;
        }
        
        // get path during loop
        Tile temp = currentTile;
        path.add(currentTile);

        // recursive-ish loop to get path
        while (temp.previous != null) {
            path.add(temp.previous);
            temp = temp.previous;
        }
        
        // set colouring
        for (int i = 0; i < closedSet.size(); i++) {
            Tile tile = closedSet.get(i);
            noStroke(); fill(255, 0, 0, 100);
            rect(tile.x * map.cellLength, tile.y * map.cellLength, map.cellLength, map.cellLength);
        }
        for (int i = 0; i < openSet.size(); i++) {
            Tile tile = openSet.get(i);
            noStroke(); fill(0, 255, 0, 100);
            rect(tile.x * map.cellLength, tile.y * map.cellLength, map.cellLength, map.cellLength);
        }
        for (int i = 0; i < path.size(); i++) {
            Tile tile = path.get(i);
            noStroke(); fill(255, 255, 0);
            rect(tile.x * map.cellLength, tile.y * map.cellLength, map.cellLength, map.cellLength);
        }
        path.clear();
        
    } else {
        // get path once open set empty/end found
        Tile temp = currentTile;
        path.add(currentTile);

        // recursive-ish loop to get path
        while (temp.previous != null) {
            path.add(temp.previous);
            temp = temp.previous;
        }
    }
}

TerrainMap generateMap(float cellLength, long seed, float smoothness) {
    TerrainMap map = new TerrainMap(cellLength);
    noiseSeed(seed);

    map.addTerrain("deepWater", 10, new float[]{0, 0.25}, color(28, 163, 236));
    map.addTerrain("water", 5, new float[]{0.25, 0.3}, color(28, 163, 150));
    map.addTerrain("waterBank", 2.5, new float[]{0.3, 0.36}, color(246, 215, 176));
    map.addTerrain("plains", 1, new float[]{0.36, 0.53}, color(98, 188, 47));
    map.addTerrain("marsh", 1.5, new float[]{0.53, 0.65}, color(138, 133, 40));
    map.addTerrain("mountainEdge", 3, new float[]{0.65, 0.68}, color(101, 83, 83));
    map.addTerrain("mountain", 5, new float[]{0.68, 0.8}, color(155, 118, 83));
    map.addTerrain("mountainPeak", 10, new float[]{0.8, 1}, color(127, 131, 134));

    map.initTerrain(smoothness);
    return map;
}
