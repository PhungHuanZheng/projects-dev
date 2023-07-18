package errors;

public class IncompatibleShapeException extends RuntimeException {
    public IncompatibleShapeException(String errorMessage) {
        super(errorMessage, null);
    }
}