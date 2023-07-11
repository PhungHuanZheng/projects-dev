public class ChunkedTerrainMap {
    public Shape shapeInChunks;
    public Shape shapeInTiles;
    public Shape chunkShape;
    public float tileLength;

    public Chunk[][] chunks;

    public ArrayList<TerrainType> terrainTypes = new ArrayList<TerrainType>();

    public ChunkedTerrainMap(Shape chunkShape_, float tileLength_, boolean initNeighbours) {
        // basic init and assignment
        tileLength = tileLength_;
        chunkShape = chunkShape_;

        // calculate and round shape in tiles and round again to chunks
        shapeInTiles = new Shape(round(width / tileLength), round(height / tileLength));
        shapeInTiles.w -= shapeInTiles.w % chunkShape.w;
        shapeInTiles.h -= shapeInTiles.h % chunkShape.h;
        shapeInChunks = new Shape(shapeInTiles.w / chunkShape.w, shapeInTiles.h / chunkShape.h);

        // init chunk data as 2D array of Chunks
        chunks = new Chunk[shapeInChunks.h][shapeInChunks.w];
        for (int y = 0; y < shapeInChunks.h; y++) {
            for (int x = 0; x < shapeInChunks.w; x++) {
                chunks[y][x] = new Chunk(chunkShape, tileLength, x, y);
            }
        }

        // prep map for pathfinding
        if (initNeighbours) {
            for (int y = 0; y < shapeInChunks.h; y++) {
                for (int x = 0; x < shapeInChunks.w; x++) {
                    // iterate over 4 neighbours of chunks
                    for (int j = -1; j <= 1; j++) {
                        for (int i = -1; i <= 1; i++) {
                            if (abs(i) == abs(j)) continue;

                            // try catch to ignore invalid positions
                            try {
                                chunks[y][x].neighbours.add(chunks[y + j][x + i]);
                            }
                            catch (Exception e) {
                                continue;
                            }
                        }
                    }
                }
            }
        }
    }

    public Chunk chunkAt(int x, int y) {
        return chunks[y][x];
    }

    public Tile tileAt(int globalX, int globalY) {
        Chunk chunk = chunkAt(floor(globalX / chunkShape.w), floor(globalY / chunkShape.h));
        Tile tile = chunk.tileAt(globalX % chunkShape.w, globalY % chunkShape.h);
        return tile;
    }

    public Chunk chunkWith(Tile tile) {
        return chunkAt(floor(tile.globalPos.x / chunkShape.w), floor(tile.globalPos.y / chunkShape.h));
    }

    public void addTerrain(String terrainName, float traverseDifficulty, float[] threshold, color clr) {
        terrainTypes.add(new TerrainType(terrainName, traverseDifficulty, threshold, clr));
    }

    public void generateTerrain(float seed, float smoothness) {
        noiseSeed((long)seed);

        // normalize traverse difficulty values to between 0 and 1
        double minVal = Double.POSITIVE_INFINITY;
        double maxVal = Double.NEGATIVE_INFINITY;
        for (TerrainType terrain : terrainTypes) {
            if (terrain.traverseDifficulty < minVal) minVal = terrain.traverseDifficulty;
            else if (terrain.traverseDifficulty > maxVal) maxVal = terrain.traverseDifficulty;
        }
        for (TerrainType terrain : terrainTypes) {
            terrain.traverseDifficulty = map(terrain.traverseDifficulty, (float)minVal, (float)maxVal, 0, 100);
        }
        

        // iterate over tiles in map
        for (int y = 0; y < shapeInTiles.h; y++) {
            for (int x = 0; x < shapeInTiles.w; x++) {

                // get noise value for tile at position
                Tile tile = tileAt(x, y);
                float tileNoise = noise(x / smoothness, y / smoothness);

                // map tile noise values to terrain types
                for (int i = 0; i < terrainTypes.size(); i++) {
                    TerrainType terrain = terrainTypes.get(i);
                    if (tileNoise >= terrain.threshold[0] && tileNoise < terrain.threshold[1]) {
                        tile.setTerrain(terrain);
                        break;
                    }
                }
            }
        }

        // calculate traverse difficulty by chunks
        for (int y = 0; y < shapeInChunks.h; y++) {
            for (int x = 0; x < shapeInChunks.w; x++) {
                Chunk chunk = chunkAt(x, y);

                for (int j = 0; j < chunk.chunkShape.h; j++) {
                    for (int i = 0; i < chunk.chunkShape.w; i++) {
                        chunk.traverseDifficulty += chunk.tileAt(i, j).traverseDifficulty;
                    }
                }
            }
        }
    }

    public void regenerateTerrainAt(Tile[] tiles, float seed, float smoothness, float radius, String mode) {
        noiseSeed((long)seed);

        for (int i = 0; i < tiles.length; i++) {
            Tile tile = tiles[i];
            float tileNoise = noise(tile.globalPos.x / smoothness, tile.globalPos.y / smoothness);

            if (mode != "none") {
                float d = dist(mouseX, mouseY, tile.globalPos.x * tileLength, tile.globalPos.y * tileLength);
                float multiplier = map(d, 0, radius, 0.05, 0);

                if (mode == "elevate") tileNoise += tileNoise * multiplier;
                if (mode == "depress") tileNoise -= tileNoise * multiplier;

                tileNoise = constrain(tileNoise, 0, 1);
            }

            // map tile noise values to terrain types
            for (int j = 0; j < terrainTypes.size(); j++) {
                TerrainType terrain = terrainTypes.get(j);
                if (tileNoise >= terrain.threshold[0] && tileNoise < terrain.threshold[1]) {
                    tile.setTerrain(terrain);
                    break;
                }
            }
        }
    }

    public ArrayList<Chunk> pathfindChunks(Tile start, Tile end) {
        // get chunks containing start and end tile
        Chunk startChunk = chunkWith(start);
        Chunk endChunk = chunkWith(end);

        // init A* stuff
        ArrayList<Chunk> path = new ArrayList<Chunk>();
        ArrayList<Chunk> openSet = new ArrayList<Chunk>();
        ArrayList<Chunk> closedSet = new ArrayList<Chunk>();
        openSet.add(startChunk);

        // A* loop
        while (openSet.size() > 0) {
            // get chunk with lowest cost
            int lowestCostIndex = 0;
            for (int i = 0; i < openSet.size(); i++) {
                if (openSet.get(i).f < openSet.get(lowestCostIndex).f) {
                    lowestCostIndex = i;
                }
            }
            Chunk currentChunk = openSet.get(lowestCostIndex);

            // if end goal reached, break out of loop
            if (currentChunk == endChunk) break;

            // preemptively move current chunk from open to closed set
            openSet.remove(currentChunk);
            closedSet.add(currentChunk);

            // iterate over and evaluate chunk neighbours
            ArrayList<Chunk> neighbours = currentChunk.neighbours;
            for (int i = 0; i < neighbours.size(); i++) {
                Chunk neighbour = neighbours.get(i);

                // if neighbour in closed set, ignore, else get step count to neighbour
                if (closedSet.contains(neighbour)) continue;
                float tempG = currentChunk.g + neighbour.traverseDifficulty;

                // if neighbour in open set and the reevaluated g is smaller than its current g
                if (openSet.contains(neighbour)) {
                    if (tempG < neighbour.g) {
                        neighbour.g = tempG;
                    }
                } else {
                    neighbour.g = tempG;
                    openSet.add(neighbour);
                }

                // calculate total cost to move to neighbouring chunk
                neighbour.h = heuristic(neighbour, endChunk);
                neighbour.f = neighbour.g + neighbour.h;

                // chain current chunk as neighbour's previous to get path
                neighbour.previous = currentChunk;
            }
        }

        // build path by working backwards
        Chunk tempChunk = endChunk;
        path.add(endChunk);
        while (tempChunk.previous != null) {
            path.add(tempChunk.previous);
            tempChunk = tempChunk.previous;
        }
        return path;
    }

    public void show(boolean drawChunks) {
        // iterate over chunks
        for (int y = 0; y < shapeInChunks.h; y++) {
            for (int x = 0; x < shapeInChunks.w; x++) {
                Chunk chunk = chunkAt(x, y);

                // iterate over tiles in chunk
                for (int j = 0; j < chunk.chunkShape.h; j++) {
                    for (int i = 0; i < chunk.chunkShape.w; i++) {
                        Tile tile = chunk.tileAt(i, j);

                        fill(tile.clr);
                        noStroke();
                        rect(tile.globalPos.x * tileLength, tile.globalPos.y * tileLength, tileLength, tileLength);
                    }
                }

                // if want to draw chunks over tiles
                if (drawChunks) {
                    noFill();
                    stroke(chunk.clr);
                    rect(x * chunkShape.w * tileLength, y * chunkShape.h * tileLength, chunkShape.w * tileLength, chunkShape.h * tileLength);
                    fill(0);
                    text(chunk.f, x * chunkShape.w * tileLength + (chunkShape.w * tileLength) / 4, y * chunkShape.h * tileLength + (chunkShape.h * tileLength) / 2);
                }
            }
        }
    }
}


public float heuristic(Chunk A, Chunk B) {
    return (float)((abs(A.pos.x - B.pos.x) + abs(A.pos.y - B.pos.y)));
}
