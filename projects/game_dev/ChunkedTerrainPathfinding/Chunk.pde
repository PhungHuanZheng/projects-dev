public class Chunk {
    public Pos pos;
    public Shape chunkShape;
    public float tileLength;

    public Tile[][] tiles;

    public color clr = color(255, 0, 0);

    public ArrayList<Chunk> neighbours = new ArrayList<Chunk>();
    public float traverseDifficulty = 0;
    public float f = 0;
    public float g = 0;
    public float h = 0;
    public Chunk previous;

    public Tile startTile;
    public Tile endTile;

    public Chunk(Shape chunkShape_, float tileLength_, int x_, int y_) {
        pos = new Pos(x_, y_);
        chunkShape = chunkShape_;
        tileLength = tileLength_;

        // init tiles in chunk with local and global pos
        tiles = new Tile[chunkShape.h][chunkShape.w];
        for (int y = 0; y < chunkShape.h; y++) {
            for (int x = 0; x < chunkShape.w; x++) {
                tiles[y][x] = new Tile(this, x, y);
            }
        }
    }

    public Tile tileAt(int localX, int localY) {
        return tiles[localY][localX];
    }

    public Tile[] getRow(int index) {
        return tiles[index];
    }

    public Tile[] getColumn(int index) {
        Tile[] column = new Tile[chunkShape.h];
        for (int i = 0; i < tiles.length; i++) {
            column[i] = tiles[i][index];
        }
        return column;
    }

    public void initNeighbours() {
        // iterate over tiles
        for (int y = 0; y < chunkShape.h; y++) {
            for (int x = 0; x < chunkShape.w; x++) {
                // iterate over 4 neighbours of chunks
                for (int j = -1; j <= 1; j++) {
                    for (int i = -1; i <= 1; i++) {
                        if (abs(i) == abs(j)) continue;

                        // try catch to ignore invalid positions
                        try {
                            tiles[y][x].neighbours.add(tiles[y + j][x + i]);
                        }
                        catch (Exception e) {
                            continue;
                        }
                    }
                }
            }
        }
    }

    public ArrayList<Tile> pathfindTiles() {
        // init A* stuff
        ArrayList<Tile> path = new ArrayList<Tile>();
        ArrayList<Tile> openSet = new ArrayList<Tile>();
        ArrayList<Tile> closedSet = new ArrayList<Tile>();
        openSet.add(startTile);

        // A* loop
        while (openSet.size() > 0) {
            // get chunk with lowest cost
            int lowestCostIndex = 0;
            for (int i = 0; i < openSet.size(); i++) {
                if (openSet.get(i).f < openSet.get(lowestCostIndex).f) {
                    lowestCostIndex = i;
                }
            }
            Tile currentTile = openSet.get(lowestCostIndex);

            // if end goal reached, break out of loop
            if (currentTile == endTile) break;

            // preemptively move current chunk from open to closed set
            openSet.remove(currentTile);
            closedSet.add(currentTile);

            // iterate over and evaluate chunk neighbours
            ArrayList<Tile> neighbours = currentTile.neighbours;
            for (int i = 0; i < neighbours.size(); i++) {
                Tile neighbour = neighbours.get(i);

                // if neighbour in closed set, ignore, else get step count to neighbour
                if (closedSet.contains(neighbour)) continue;
                float tempG = currentTile.g + neighbour.traverseDifficulty;

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
                neighbour.h = heuristic(neighbour, endTile);
                neighbour.f = neighbour.g + neighbour.h;

                // chain current chunk as neighbour's previous to get path
                neighbour.previous = currentTile;
            }
        }
        
        // build path by working backwards
        Tile tempTile = endTile;
        path.add(endTile);
        while (tempTile.previous != null) {
            path.add(tempTile.previous);
            tempTile = tempTile.previous;
        }
        return path;
    }
}

public float heuristic(Tile A, Tile B) {
    return (float)(abs(A.chunkPos.x - B.chunkPos.x) + abs(A.chunkPos.y - B.chunkPos.y));
}
