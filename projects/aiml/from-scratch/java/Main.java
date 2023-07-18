public class Main {
    public static void main(String[] args) {
        // load data from text file
        try {
            // LabelledDataset train = new LabelledDataset("../processing/NNFromScratch/data/MNIST_train.txt", ",", 10);
            // LabelledDataset test = new LabelledDataset("../processing/NNFromScratch/data/MNIST_test.txt", ",", 10);
            // LabelledDataset test = new LabelledDataset("../processing/NNFromScratch/data/test.txt", ",", 10, 0);
            LabelledDataset train = new LabelledDataset("../processing/NNFromScratch/data/8x8_train.txt", ",", 10, 64);
            train.normalize();
            // LabelledDataset test = new LabelledDataset("../processing/NNFromScratch/data/8x8_test.txt", ",", 10, 64);


            NeuralNetwork nn = new NeuralNetwork(
                64,
                new int[] { 16, 16, 10 },
                new String[] { "relu", "relu", "softmax" }
            );
                
            nn.print();
            nn.fit(train.data, train.targets, 10);

            

        } catch (Exception e) {
            e.printStackTrace();
        }
        
    }
}
