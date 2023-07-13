class Main {
    // global variables
    static int staticInt = 3;
    public float publicFloat = 2.3f;

    // main script
    public static void main(String[] args) {
        System.out.println("Hello World");

        /**
         * Java is a strongly typed language, every variable
         * needs a specific type, e.g.: int, float
         */
        int age = 38;
        float weight = 78.2f;
        double largeNum = 555555555;
        long veryLargeNum = 999999999999999999L;

        System.out.println("age: " + age + "\nweight: " + weight);
        System.out.println("largeNum: " + largeNum + "\nveryLargeNum: " + veryLargeNum);
        System.out.println(myStaticInt());
    }

    static void javaVariables() {
        // integer types increasing from 2^7 to 2^63
        byte byte_ = 100; 
        short short_ = 20000; 
        int int_ = 39287327;
        long long_ = 8974902794222233L;

        // decimal types 
        double double_ = 1.398837;
        float float_ = 12901209.189f;

        // booleans
        boolean isMan = false;
        boolean isSaturday = true;

        // char types
        char char_ = 'a';
        String string_ = "oiascjoa";
    }

    // only static methods can access static variables
    static int myStaticInt() {
        return staticInt;
    }
}