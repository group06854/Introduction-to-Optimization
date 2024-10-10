import java.io.InputStream;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Scanner;
import java.util.stream.Collectors;

public class Main {
  public static void main(String[] args) {}

  static class SimplexMethod {
    static class SimplexTable {
      static class Row {
        ArrayList<Double> coefs;
        double result;

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
          coefs.ensureCapacity(coefs.size() + number);
          for (int i = coefs.size(); i < coefs.size() + number; ++i) {
            coefs.add(0d);
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
      }

      Row z;
      ArrayList<Row> ineqs = new ArrayList<>();

      private SimplexTable() {}

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
    }

    static final double EPS = 0.000001d;

    int precision;
    Double[] objectiveFunction;
    SimplexTable table = new SimplexTable();

    Double maximize() {
      // TODO: implement simplex maximization
      return 0d;
    }

    static SimplexMethod parseStream(InputStream stream) {
      Scanner input = new Scanner(stream);
      SimplexMethod method = new SimplexMethod();
      method.objectiveFunction =
          Arrays.stream(input.nextLine().strip().split(" "))
              .map(it -> Double.parseDouble(it))
              .toArray(Double[]::new);
      ArrayList<Double> row;
      ArrayList<Double> nextRow =
          Arrays.stream(input.nextLine().strip().split(" "))
              .map(it -> Double.parseDouble(it))
              .collect(Collectors.toCollection(ArrayList::new));
      while (true) {
        row = nextRow;
        nextRow =
            Arrays.stream(input.nextLine().strip().split(" "))
                .map(it -> Double.parseDouble(it))
                .collect(Collectors.toCollection(ArrayList::new));
        if (nextRow.size() <= 1) {
          input.close();
          if (nextRow.size() == 0) {
            throw new IllegalArgumentException("no epsilon was provided");
          }
          int ineqNumber = method.table.ineqs.size();
          if (row.size() < ineqNumber) {
            throw new IllegalArgumentException("not enough results");
          }
          method.table.z.extendWithNVariables(ineqNumber);
          for (int i = 0; i < ineqNumber; ++i) {
            SimplexTable.Row ineq = method.table.ineqs.get(i);
            ineq.extendWithNVariables(ineqNumber);
            ineq.result = row.get(i);
          }
          method.precision = nextRow.get(0).intValue();
          return method;
        } else if (nextRow.size() != method.objectiveFunction.length) {
          input.close();
          throw new IllegalArgumentException(
              "wrong inequality, does not match the number of variables in objective function");
        }
        method.table.ineqs.add(new SimplexTable.Row(row));
      }
    }

    @Override
    public String toString() {
      String string = "z =";
      for (int i = 0; i < objectiveFunction.length; ++i) {
        string += objectiveFunction[i] + EPS >= 0 ? (i == 0 ? " " : " + ") : " - ";
        string += ("%." + precision + "fx%d").formatted(Math.abs(objectiveFunction[i]), i + 1);
      }
      string += "\n";
      System.out.println("Constraints:\n");
      for (SimplexTable.Row ineq : table.ineqs) {
        for (int i = 0; i < ineq.coefs.size(); ++i) {
          string += ineq.coefs.get(i) + EPS >= 0 ? (i == 0 ? "" : "+ ") : "- ";
          string += ("%." + precision + "fx%d").formatted(Math.abs(ineq.coefs.get(i)), i + 1);
        }
        string += "<= %." + precision + "f".formatted(ineq.result);
        string += "\n";
      }
      return string;
    }
  }
}
