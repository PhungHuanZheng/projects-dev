public class LabelledDataset {
    public float[][] data;
    public int[] target;

    public int sampleCount;
    public int datapointLength;
    public ArrayList<Integer> targets = new ArrayList<Integer>();
    public int targetCount;

    public float min = (float)Double.POSITIVE_INFINITY;
    public float max = (float)Double.NEGATIVE_INFINITY;

    public LabelledDataset(String dataPath, String delim, boolean normalize) {
        //parses text data assuming each line is a target, data and line break
        //all separated by the same deliminator

        String[] lines = loadStrings(sketchPath(dataPath));
        this.data = new float[lines.length][lines[0].split(delim).length - 1];
        this.target = new int[lines.length];
        this.sampleCount = lines.length;
        this.datapointLength = lines[0].split(delim).length - 1;

        for (int i = 0; i < lines.length; i++) {
            String[] line = lines[i].split(delim);
            this.target[i] = Integer.parseInt(line[0]);
            
            // track unique targets
            if (!targets.contains(this.target[i])) {
                this.targets.add(this.target[i]);
            }

            for (int j = 1; j < line.length; j++) {
                float datapoint = Integer.parseInt(line[j]);

                // get min max
                if (datapoint < this.min) this.min = datapoint;
                if (datapoint < this.max) this.max = datapoint;
                this.data[i][j - 1] = Integer.parseInt(line[j]);
            }
        }

        if (normalize) {
            for (int y = 0; y < this.sampleCount; y++) {
                for (int x = 0; x < this.datapointLength; x++) {
                    this.data[y][x] = map(this.data[y][x], min, max, 0, 1);
                }
            }
        }
        
        this.targetCount = targets.size();
    }

    public DataTargetPair get(int index) {
        return new DataTargetPair(this.data[index], this.target[index]);
    }

    public Matrix2D getData(int index) {
        Matrix2D matrix = new Matrix2D(1, this.data[index].length, false);
        matrix.data = new float[][]{this.data[index]};
        return matrix;
    }
    
    public int getTarget(int index) {
        return this.target[index];
    }
    
    public Matrix2D getTarget(int index, boolean encode) {
        int target = this.target[index];
        float[] encoded = new float[targetCount];
        Matrix2D matrix = new Matrix2D(1, targetCount, false);
        
        for (int i = 0; i < encoded.length; i++) {
            if (i == target) {
                 encoded[i] = 1;   
                 continue;
            }
            encoded[i] = 0;
        }
        
        matrix.data[0] = encoded;
        return matrix.transpose();
    }

    public void shuffle() {
        // create array of indexes and shuffle
        int[] indexArr = new int[this.data.length];
        for (int i = 0; i < indexArr.length; i++) {
            int randIndex = floor(random(indexArr.length));
            int temp = indexArr[randIndex];
            indexArr[randIndex] = indexArr[i];
            indexArr[i] = temp;
        }

        float[][] tempData = new float[this.data.length][this.data[0].length];
        int[] tempTarget = new int[this.target.length];

        for (int i = 0; i < indexArr.length; i++) {
            tempData[i] = this.data[indexArr[i]];
            tempTarget[i] = this.target[indexArr[i]];
        }
    }

    public Matrix2D asMatrix() {
        Matrix2D matrix = new Matrix2D(this.data.length, this.data[0].length, false);
        for (int y = 0; y < matrix.shape[0]; y++) {
            for (int x = 0; x < matrix.shape[1]; x++) {
                matrix.data[y][x] = this.data[y][x];
            }
        }
        return matrix;
    }

    public float[][] asGrid(int index, int gridWidth, int gridHeight) {
        // get and reshape data
        float[] indexedData = this.data[index];
        float[][] reshapedData = new float[gridHeight][gridWidth];

        for (int y = 0; y < gridHeight; y++) {
            for (int x = 0; x < gridWidth; x++) {
                reshapedData[y][x] = indexedData[y * gridWidth + x];
            }
        }

        return reshapedData;
    }
}
