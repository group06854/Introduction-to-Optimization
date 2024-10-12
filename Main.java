import java.io.InputStream;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Scanner;
import java.util.stream.Collectors;

public class Main {
    public static void main(String[] args) {
        try {
            SimplexMethod method = SimplexMethod.parseStream(System.in);
            method.maximize();
        } catch (Exception error) {
            System.out.println("The method is not applicable!");
        }
    }
}

class SimplexMethod {
    static class SimplexTable {
        static class Row {
            ArrayList<Double> coefs;
            double result;
            int basicIndex;  // from 0!!

            Row(List<Double> coefficients, double result) {
                this.coefs = new ArrayList<>(coefficients);
                this.result = result;
            }
            Row(List<Double> coefficients) {
                this(coefficients, 0);
            }
            Row(Row other) {
                this(other.coefs, other.result);
            }

            void extendWithNVariables(int number) {
                for (int i = 0; i < number; ++i) {
                    coefs.add(0.0d);
                }
            }

            void plus(double coef, Row other) {
                for (int i = 0; i < coefs.size(); ++i) {
                    coefs.set(i, coefs.get(i) + coef * other.coefs.get(i));
                }
                result = coef * other.result;
            }
            void multiplyBy(double coef) {
                for (int i = 0; i < coefs.size(); ++i) {
                    coefs.set(i, coef * coefs.get(i));
                }
            }
            double get(int index) {
                return coefs.get(index);
            }
            void set(int index, double value) {
                coefs.set(index, value);
            }
            public String toString() {
                StringBuilder string = new StringBuilder();
                for (Double coef : coefs) {
                    string.append(coef);
                    string.append(" ");
                }
                string.append(result);
                return string.toString();
            }
        }

        Row z;
        ArrayList<Row> ineqs = new ArrayList<>();

        private SimplexTable() {
        }

        /**
         * Find the least negative coefficient in the objective function. If none was found, its
         * result is considered as the solution.
         *
         * @return Index of the coefficient if found, -1 otherwise.
         */
        int leastNegativeIndex() {
            int index = -1;
            double least = 0d;
            for (int i = 0; i < z.coefs.size(); ++i) {
                double coef = z.coefs.get(i);
                if (coef < least) {
                    index = i;
                    least = coef;
                }
            }
            return index;
        }
        Row getRow(int index) {
            for (Row row : ineqs) {
                if (row.basicIndex == index) {
                    return row;
                }
            }
            return null;
        }
    }

    static final double EPS = 0.000001d;

    int precision;
    Double[] objectiveFunction;
    SimplexTable table = new SimplexTable();

    void maximize() {
        table.z.multiplyBy(-1d);
        int basicEnter = table.leastNegativeIndex();
        while (basicEnter != -1) {
            int basicLeaves = -1;
            double minPositiveRatio = Double.MAX_VALUE;
            for (SimplexTable.Row row : table.ineqs) {
                double ratio = row.result / row.get(basicEnter);
                if (ratio > 0 && ratio < minPositiveRatio) {
                    minPositiveRatio = ratio;
                    basicLeaves = row.basicIndex;
                }
            }
            if (basicLeaves == -1) {
                throw new IllegalArgumentException("no valid ratio found - unbounded");
            }

            double crossNumber = table.getRow(basicLeaves).get(basicEnter);
            table.getRow(basicLeaves).multiplyBy(1/crossNumber);
            table.getRow(basicLeaves).result /= crossNumber;

            table.z.set(basicLeaves, -table.z.get(basicEnter)/crossNumber);
            for (SimplexTable.Row row : table.ineqs) {
                if (row.basicIndex != basicLeaves) {
                    row.set(basicLeaves, -row.get(basicEnter)/crossNumber);
                }
            }

            for (int i = 0; i < table.z.coefs.size(); i++) {
                if (i != basicLeaves) {
                    table.z.set(i, table.getRow(basicLeaves).get(i) * crossNumber * table.z.get(basicLeaves) + table.z.get(i));
                }
            }
            table.z.result = table.getRow(basicLeaves).result * crossNumber * table.z.get(basicLeaves) + table.z.result;
            for (SimplexTable.Row row : table.ineqs) {
                if (row.basicIndex != basicLeaves) {
                    for (int i = 0; i < row.coefs.size(); i++) {
                        if (i != basicLeaves) {
                            row.set(i, table.getRow(basicLeaves).get(i) * crossNumber * row.get(basicLeaves) + row.get(i));
                        }
                    }
                    row.result = table.getRow(basicLeaves).result * crossNumber * row.get(basicLeaves) + row.result;
                }
            }



            table.getRow(basicLeaves).basicIndex = basicEnter;
            basicEnter = table.leastNegativeIndex();
//            for (SimplexTable.Row row : table.ineqs) {
//                System.out.println(row + " " + row.result);
//            }
//            System.out.println(table.z + " " + table.z.result);
        }
        StringBuilder string = new StringBuilder();
        for (int i = 0; i < objectiveFunction.length; i++) {
            SimplexTable.Row row = table.getRow(i);
            if (row != null) {
                string.append(("%." + precision + "f").formatted(row.result));
            } else {
                string.append(("%." + precision + "f").formatted(0d));
            }
            string.append(" ");
//            for (SimplexTable.Row row : table.ineqs) {
//                System.out.printf("x%d = %f\n", row.basicIndex + 1, row.result);
//            }
        }
        string.append("\n");
        string.append(("%." + precision + "f").formatted(table.z.result));
        System.out.println(string);
    }


    static SimplexMethod parseStream(InputStream stream) {
        Scanner input = new Scanner(stream);
        SimplexMethod method = new SimplexMethod();
        method.objectiveFunction =
                Arrays.stream(input.nextLine().strip().split(" "))
                        .map(Double::parseDouble)
                        .toArray(Double[]::new);
        ArrayList<Double> row;
        ArrayList<Double> nextRow =
                Arrays.stream(input.nextLine().strip().split(" "))
                        .map(Double::parseDouble)
                        .collect(Collectors.toCollection(ArrayList::new));
        while (true) {
            row = nextRow;
            nextRow =
                    Arrays.stream(input.nextLine().strip().split(" "))
                            .map(Double::parseDouble)
                            .collect(Collectors.toCollection(ArrayList::new));
            if (nextRow.size() <= 1) {
                input.close();
                if (nextRow.isEmpty()) {
                    throw new IllegalArgumentException("no epsilon was provided");
                }
                int varNumber = method.table.ineqs.size();
                if (row.size() < varNumber) {
                    throw new IllegalArgumentException("not enough results");
                }
                method.table.z = new SimplexTable.Row(List.of(method.objectiveFunction));
                method.table.z.extendWithNVariables(varNumber);
                for (int i = 0; i < varNumber; ++i) {
                    SimplexTable.Row ineq = method.table.ineqs.get(i);
                    ineq.extendWithNVariables(varNumber);
                    ineq.coefs.set(varNumber + i, 1d);
                    ineq.basicIndex = varNumber + i;
                    ineq.result = row.get(i);
                }
                method.precision = nextRow.get(0).intValue();
                return method;
            } else if (nextRow.size() != method.objectiveFunction.length) {
                input.close();
                throw new IllegalArgumentException(
                        "wrong inequality, does not match the number of variables in objective function - redundancy");
            }
            method.table.ineqs.add(new SimplexTable.Row(row));
        }
    }

    @Override
    public String toString() {
        StringBuilder string = new StringBuilder("f =");
        for (int i = 0; i < objectiveFunction.length; ++i) {
            string.append(objectiveFunction[i] + EPS >= 0 ? (i == 0 ? " " : " + ") : " - ");
            string.append(("%." + precision + "fx%d").formatted(Math.abs(objectiveFunction[i]), i + 1));
        }
        string.append("\nConstraints:\n");
        for (SimplexTable.Row ineq : table.ineqs) {
            for (int i = 0; i < ineq.coefs.size(); ++i) {
                string.append(ineq.coefs.get(i) + EPS >= 0 ? (i == 0 ? "" : "+ ") : "- ");
                string.append(("%." + precision + "fx%d ").formatted(Math.abs(ineq.coefs.get(i)), i + 1));
            }
            string.append(("<= %." + precision + "f").formatted(ineq.result));
            string.append("\n");
        }
        return string.toString();
    }
}
