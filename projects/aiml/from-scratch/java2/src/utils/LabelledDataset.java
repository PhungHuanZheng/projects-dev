package utils;

import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Arrays;

public class LabelledDataset {
	private Matrix2D data;
	private Matrix2D targets;
	
	public int classCount;
	public float min = (float) Double.POSITIVE_INFINITY;
	public float max = (float) Double.NEGATIVE_INFINITY;

	public LabelledDataset(String filepath, String delim, int classIndex) {
		float[][] data_ = null;
		float[] targets_ = null;

		try {
//			get lines in text file
			Path path = Paths.get(filepath);
			Object[] lines_ = Files.lines(path).toArray();
			String[] lines = Arrays.copyOf(lines_, lines_.length, String[].class);

//			extract data and targets
			for (int i = 0; i < lines.length; i++) {
				String[] line = lines[i].split(delim);
				if (data_ == null || targets_ == null) {
					data_ = new float[lines.length][line.length - 1];
					targets_ = new float[lines.length];
				}

				targets_[i] = Integer.parseInt(line[classIndex]);
				for (int j = 0; j < line.length; j++) {
					if (j == classIndex) {
						continue;
					}
					float num = Float.parseFloat(line[j]);
					data_[i][j] = num;
					
//					compare num against min and max
					this.min = num < min ? num : min;
					this.max = num > max ? num : max;
				}
			}

//			convert to matrices and set
			this.data = new Matrix2D(data_.length, data_[0].length);
			this.targets = new Matrix2D(1, data_.length);

			this.data.data = data_;
			this.targets.data[0] = targets_;
			this.targets.T();
			
			this.classCount = this.targets.unique().length;

		} catch (Exception e) {
			e.printStackTrace();
			return;
		}
	}

	public Matrix2D getData() {
		return this.data;
	}

	public Matrix2D getTargets() {
		return this.targets;
	}

	public LabelledDataset encodeTargets() {
//		update targets shape and size
		this.targets.shape[1] = this.classCount;
		this.targets.size *= this.classCount;
		
//		iterate over all targets
		for (int i = 0; i < this.targets.shape[0]; i++) {
//			build empty array of 0s, set class index in arr to 1
			float[] targetArr = new float[classCount];
			for (int j = 0; j < classCount; j++) {
				targetArr[j] = 0;
			}
			targetArr[(int)this.targets.data[i][0]] = 1;
			this.targets.data[i] = targetArr;
		}
		
		return this;
	}

	public LabelledDataset scale(float minVal, float maxVal) {
//		iterate over data, scale between passed min and max
		for (int y = 0; y < this.data.shape[0]; y++) {
			for (int x = 0; x < this.data.shape[1]; x++) {
//				get ratio of original num in original min max
				float ratio = (this.data.data[y][x] - this.min) / (this.max - this.min);
				this.data.data[y][x] = minVal + (ratio * (maxVal - minVal));
			}
		}
		
//		update min and max
		this.min = minVal;
		this.max = maxVal;
		
		return this;
	}

	public LabelledDataset shuffle() {
//		get array of indexes and shuffle
		int[] indexArr = new int[this.data.shape[0]];
		for (int i = 0; i < indexArr.length; i++) {
			indexArr[i] = i;
		}
		for (int i = 0; i < indexArr.length; i++) {
			int index1 = (int) Math.floor(Math.random() * indexArr.length);
			int index2 = (int) Math.floor(Math.random() * indexArr.length);
			
			int temp = indexArr[index1];
			indexArr[index1] = indexArr[index2];
			indexArr[index2] = temp;
		}
		
//		update matrix data with new shuffled data
		Matrix2D newData = new Matrix2D(this.data.shape[0], this.data.shape[1]);
		Matrix2D newTargets = new Matrix2D(this.targets.shape[0], this.targets.shape[1]);
		
		for (int i = 0; i < indexArr.length; i++) {
			newData.data[i] = this.data.data[indexArr[i]];
			newTargets.data[i] = this.targets.data[indexArr[i]];
		}
		this.data = newData;
		this.targets = newTargets;
		
		return this;
	}

	public LabelledDataset tranpose() {
//		this should be the last step if needed else any operations after this
//		might result in non-related data being put together.
		this.data.T();
		this.targets.T();
		
		return this;
	}
}
