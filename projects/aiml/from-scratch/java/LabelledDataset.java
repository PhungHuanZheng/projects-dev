import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Arrays;

public class LabelledDataset {
    public Matrix2D data;
    public Matrix2D targets;
    public int classCount;

    public LabelledDataset(String filepath, String delim, int classCount) {
        float[][] data_ = null;
        int[] targets_ = null;

        this.classCount = classCount;

        try {
            // get lines in text file
            Path path = Paths.get(filepath);
            Object[] lines_ = Files.lines(path).toArray();
            String[] lines = Arrays.copyOf(lines_, lines_.length, String[].class);

            for (int i = 0; i < lines.length; i++) {
                String[] line = lines[i].split(delim);
                if (data_ == null || targets_ == null) {
                    data_ = new float[lines.length][line.length - 1];
                    targets_ = new int[lines.length];
                }

                targets_[i] = Integer.parseInt(line[0]);
                for (int j = 0; j < line.length - 1; j++) {
                    float num = Float.parseFloat(line[j + 1]);
                    data_[i][j] = num;
                }
                System.out.println(i);
            }

        } catch (Exception e) {
            System.out.println("An error occurred.");
            e.printStackTrace();
        }

        // comvert data and encoded targets to matrices
        this.data = new Matrix2D(data_.length, data_[0].length);
        this.data.data = data_;
        this.data.transpose();

        float[][] targetsData = new float[data_.length][classCount];
        for (int i = 0; i < data_.length; i++) {
            for (int j = 0; j < classCount; j++) {
                if (j == targets_[i]) {
                    targetsData[i][j] = 1;
                } else {
                    targetsData[i][j] = 0;
                }
            }
        }   
        this.targets = new Matrix2D(data_.length, classCount);
        this.targets.data = targetsData;
    }
}
